import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def predict_demand(file_path):
    # Read data
    df = pd.read_excel(file_path)

    # Keep only needed columns
    df = df[['Item_Code', 'Item_Description', 'Patient_Footfall', 'Last_Week_Usage',
             'Public_Holiday', 'Rain_Impact', 'Quantity_used']]

    # Group by item (in case multiple items exist)
    item_code = df['Item_Code'].iloc[0]
    item_name = df['Item_Description'].iloc[0]

    # Prepare features and target
    X = df[['Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact']]
    y = df['Quantity_used']

    # Split into train/test: First 148 for training, next 8 for prediction
    X_train, X_test = X[:148], X[148:156]
    y_train, y_test = y[:148], y[148:156]

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict on test (week 149–156)
    y_pred = model.predict(X_test)

    # Evaluation
    mae = mean_absolute_error(y_test, y_pred)

    # Build results
    results = []
    for week in range(149, 157):
        results.append({
            'Week': f'Week {week}',
            'Actual': y_test.values[week - 149],
            'Predicted': round(y_pred[week - 149], 2)
        })

    return {
        'item_code': item_code,
        'item_name': item_name,
        'results': results,
        'mae': round(mae, 2)
    }
