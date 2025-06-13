# views.py in forecast app
import pandas as pd
import numpy as np
from django.shortcuts import render
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os
import matplotlib.pyplot as plt
import uuid
from django.conf import settings

def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def upload_and_forecast(request):
    context = {}

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        ext = os.path.splitext(file.name)[1]

        try:
            if ext in ['.xls', '.xlsx']:
                df = pd.read_excel(file)
            elif ext == '.csv':
                df = pd.read_csv(file)
            else:
                context['error'] = 'Unsupported file format. Use .csv or .xlsx'
                return render(request, 'upload.html', context)

            # Normalize column headers
            df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

            # Rename to match expected names if needed
            if 'quantity_used' not in df.columns:
                raise ValueError("Missing required column: quantity_used")

            # Check if required columns exist
            required_columns = ['patient_footfall', 'last_week_usage', 'public_holiday', 'rain_impact', 'quantity_used']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")

            # Prepare features and labels
            df = df.reset_index(drop=True)
            features = df[['patient_footfall', 'last_week_usage', 'public_holiday', 'rain_impact']]
            labels = df['quantity_used']

            # Train-test split
            X_train = features[:148]
            y_train = labels[:148]
            X_test = features[148:156]
            y_test = labels[148:156]

            # Train model
            model = RandomForestRegressor(random_state=42)
            model.fit(X_train, y_train)

            # Predict
            predictions = model.predict(X_test)

            # Evaluation
            mae = mean_absolute_error(y_test, predictions)
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            mape_score = mape(np.array(y_test), predictions)

            # Save plot
            plt.figure(figsize=(10, 5))
            plt.plot(range(149, 157), y_test.values, marker='o', label='Actual')
            plt.plot(range(149, 157), predictions, marker='x', label='Predicted')
            plt.title('Actual vs Predicted (Weeks 149–156)')
            plt.xlabel('Week')
            plt.ylabel('Quantity Used')
            plt.legend()
            plot_filename = f"plot_{uuid.uuid4().hex}.png"
            plot_path = os.path.join(settings.MEDIA_ROOT, plot_filename)
            plt.savefig(plot_path)
            plt.close()

            # Prepare context
            forecast_table = zip(range(149, 157), y_test, predictions)
            context = {
                'mae': round(mae, 2),
                'rmse': round(rmse, 2),
                'mape': round(mape_score, 2),
                'forecast_table': forecast_table,
                'plot_url': settings.MEDIA_URL + plot_filename,
            }

        except Exception as e:
            context['error'] = str(e)

    return render(request, 'upload.html', context)
