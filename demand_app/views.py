# demand_app/views.py

import pandas as pd
from django.shortcuts import render
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        df = pd.read_excel(request.FILES['file'])

        sku_groups = df.groupby("Item_Code")
        forecast_results = []

        for sku, group in sku_groups:
            group = group.reset_index(drop=True)

            # Ensure all required columns exist
            required_columns = ['Week', 'Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact', 'Quantity_Used', 'Item_Description']
            if not all(col in group.columns for col in required_columns):
                continue

            features = ['Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact']
            target = 'Quantity_Used'

            # Use first 148 rows for training, 149–156 for testing
            if len(group) < 156:
                continue

            train = group.iloc[:148]
            test = group.iloc[148:156]

            model = RandomForestRegressor()
            model.fit(train[features], train[target])
            predictions = model.predict(test[features])
            actuals = test[target].values

            error = mean_absolute_error(actuals, predictions)

            item_description = group['Item_Description'].iloc[0]

            forecast_results.append({
                'sku': sku,
                'description': item_description,
                'actual': actuals.tolist(),
                'predicted': predictions.tolist(),
                'error': round(error, 2),
                'weeks': list(range(149, 157))
            })

        return render(request, 'results.html', {'results': forecast_results})

    return render(request, 'upload.html')
