import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def random_forest_forecast(df):
    df = df.copy()
    df = df.dropna()
    df['Week'] = np.arange(1, len(df) + 1)
    
    # Split
    train = df[df['Week'] <= 148]
    test = df[df['Week'] > 148]

    # Features
    X_train = train[['Week']]
    y_train = train['Quantity_used']
    X_test = test[['Week']]
    y_test = test['Quantity_used']

    # Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    # Combine
    results = pd.DataFrame({
        'Week': test['Week'],
        'Actual': y_test.values,
        'Predicted': y_pred
    })

    return results, {'MAE': mae, 'RMSE': rmse, 'MAPE': mape}