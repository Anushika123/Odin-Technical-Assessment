import sys
import pandas as pd
import json
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt

# Load the Excel file
file_path = sys.argv[1]
data = pd.read_excel(file_path)

features = ['Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact']
results = {}

# Loop over each Item_Code
for item_id, group in data.groupby('Item_Code'):
    group = group.reset_index(drop=True)

    if len(group) < 156:
        continue  # skip if not enough data

    # Prepare dataframe for Prophet
    df_prophet = pd.DataFrame()
    df_prophet['ds'] = pd.date_range(start='2020-01-01', periods=len(group), freq='W')
    df_prophet['y'] = group['Quantity_Used']

    train_df = df_prophet.iloc[:148]
    test_df = df_prophet.iloc[148:156]

    model = Prophet()
    model.fit(train_df)


    # Forecast next 8 weeks
    future = model.make_future_dataframe(periods=8, freq='W')
    forecast = model.predict(future)
    predicted = forecast[['ds', 'yhat']].iloc[-8:]['yhat'].tolist()
    actual = test_df['y'].tolist()

    
    # Evaluation
    mae = mean_absolute_error(actual, predicted)
    mape = (abs((pd.Series(actual) - predicted) / pd.Series(actual)).mean()) * 100
    rmse = sqrt(mean_squared_error(actual, predicted))

    results[item_id] = {
        'mae': round(mae, 2),
        'mape': round(mape, 2),
        'rmse': round(rmse, 2),
        'actual': actual,
        'predicted': [round(p, 2) for p in predicted]
    }

# Print JSON output
print(json.dumps(results, indent=4))
