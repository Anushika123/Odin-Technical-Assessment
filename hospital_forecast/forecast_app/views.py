import pandas as pd
import os
from django.shortcuts import render
from django.conf import settings
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def upload_and_forecast(request):
    context = {}

    if request.method == 'POST' and request.FILES.get('data_file'):
        try:
            # Read uploaded CSV file
            data_file = request.FILES['data_file']
            df = pd.read_excel(data_file)
            print("Columns:", df.columns)  # Optional debug

            # Preprocessing
            df.fillna(0, inplace=True)
            df = df.reset_index(drop=True)

            # Define features and target
            features = ['Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact']
            target = 'Quantity_Used'

            # Train-test split
            train_df = df.iloc[:148]
            test_df = df.iloc[148:156]

            X_train = train_df[features]
            y_train = train_df[target]
            X_test = test_df[features]
            y_test = test_df[target]

            # Model training
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)

            # Evaluation metrics
            mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            mae = mean_absolute_error(y_test, predictions)

             # Forecast next 8 weeks (157–164)
            future_input = pd.DataFrame({
                'Patient_Footfall': [X_test['Patient_Footfall'].mean()] * 8,
                'Last_Week_Usage': [y_test.values[-1]] * 8,
                'Public_Holiday': [0] * 8,
                'Rain_Impact': [0] * 8
            })
            future_predictions = model.predict(future_input)


            # Plot actual vs predicted
            plt.figure(figsize=(10, 4))
            plt.plot(range(149, 157), y_test.values, label='Actual', marker='o')
            plt.plot(range(149, 157), predictions, label='Predicted', marker='o')
            plt.xlabel('Week')
            plt.ylabel('Quantity Used')
            plt.title('Hospital Supply Forecast')
            plt.legend()
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()

            # Send to template
            context = {
                'mape': round(mape, 2),
                'rmse': round(rmse, 2),
                'mae': round(mae, 2),
                'predictions': zip(range(149, 157), y_test.values, predictions),
                'future': zip(range(157, 165), future_predictions),
                'graph': graph,
            }

        except Exception as e:
            context['error'] = f"Something went wrong: {e}"

    return render(request, 'forecast.html', context)
