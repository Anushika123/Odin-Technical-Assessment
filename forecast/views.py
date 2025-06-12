
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt
import plotly.graph_objs as go
from plotly.offline import plot

def index(request):
    return render(request, 'index.html')
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import pandas as pd
import os
from .models import ForecastData

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('data_file'):
        uploaded_file = request.FILES['data_file']

        
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                return render(request, 'upload.html', {'message': 'Unsupported file format.'})
        except Exception as e:
            return render(request, 'upload.html', {'message': f"Error reading file: {str(e)}"})

        
        for _, row in df.iterrows():
            ForecastData.objects.create(
                item_code=row['Item_Code'],
                item_description=row['Item_Description'],
                week=row['Week'],  
                patient_footfall=row['Patient_Footfall'],
                last_week_usage=row['Last_Week_Usage'],
                public_holiday=bool(row['Public_Holiday']),
                rain_impact=bool(row['Rain_Impact']),
                quantity_used=row['Quantity_Used']
            )

        
        request.session['uploaded_file_path'] = file_path
        return redirect('forecast_view')  

    return render(request, 'upload.html')
def forecast_view(request):
    file_path = None
   
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    files = sorted([f for f in os.listdir(upload_dir) if f.endswith(('.csv', '.xlsx'))], reverse=True)
    if files:
        file_path = os.path.join(upload_dir, files[0])
    else:
        return render(request, 'forecast.html', {'message': 'No uploaded file found.'})

    
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        return render(request, 'forecast.html', {'message': f"Error reading file: {str(e)}"})

    
    df['Week'] = pd.to_datetime(df['Week'])
    df = df.sort_values('Week')

    df = df.dropna()

    
    item_df = df[df['Item_Code'] == df['Item_Code'].iloc[0]].copy()
    item_df.reset_index(drop=True, inplace=True)

    features = ['Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact']
    target = 'Quantity_Used'

    
    train = item_df.iloc[:-8]
    test = item_df.iloc[-8:]

   
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train[features], train[target])

    
    preds = model.predict(test[features])
    actuals = test[target].values

    mae = mean_absolute_error(actuals, preds)
    rmse = sqrt(mean_squared_error(actuals, preds))
    mape = np.mean(np.abs((actuals - preds) / actuals)) * 100

    
    last_row = test.iloc[-1]
    future_weeks = pd.date_range(start=item_df['Week'].max() + pd.Timedelta(weeks=1), periods=8, freq='W')

    future_df = pd.DataFrame([last_row[features]] * 8)
    future_preds = model.predict(future_df)

    
    forecast_df = pd.DataFrame({
        'Week': future_weeks,
        'Predicted_Quantity': future_preds
    })

  
    trace1 = go.Scatter(x=test['Week'], y=actuals, mode='lines+markers', name='Actual')
    trace2 = go.Scatter(x=test['Week'], y=preds, mode='lines+markers', name='Predicted')
    last8_plot = plot([trace1, trace2], output_type='div')

    trace3 = go.Scatter(x=forecast_df['Week'], y=forecast_df['Predicted_Quantity'], mode='lines+markers', name='Forecast')
    forecast_plot = plot([trace3], output_type='div')

    return render(request, 'forecast.html', {
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'mape': round(mape, 2),
        'actual_pred_table': test.assign(Predicted=preds).to_html(index=False),
        'future_table': forecast_df.to_html(index=False),
        'last8_plot': last8_plot,
        'forecast_plot': forecast_plot
    })
