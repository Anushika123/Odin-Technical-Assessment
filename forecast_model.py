import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

def forecast_demand(df):
    df = df.copy()
    df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace

    # Optional: lowercase for uniformity (you'll need to use lowercase column names below)
    # df.columns = df.columns.str.strip().str.lower()

    expected_columns = ['Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact', 'Quantity_Used']

    # Check if required columns exist
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        raise KeyError(f"The following required columns are missing from the data: {missing}")

    df = df.dropna()

    df['Week'] = range(1, len(df) + 1)
    features = ['Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact']
    target = 'Quantity_Used'

    train_df = df[df['Week'] <= 148]
    test_df = df[(df['Week'] > 148) & (df['Week'] <= 156)]

    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    result_df = test_df[['Item_Code', 'Item_Description']].copy() if 'Item_Code' in df.columns and 'Item_Description' in df.columns else pd.DataFrame()
    result_df['Week'] = test_df['Week']
    result_df['Actual'] = y_test.values
    result_df['Predicted'] = y_pred

    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(test_df['Week'], y_test, label='Actual', marker='o')
    ax.plot(test_df['Week'], y_pred, label='Predicted', marker='x')
    ax.set_title("Actual vs Predicted Usage (Week 149–156)")
    ax.set_xlabel("Week")
    ax.set_ylabel("Quantity Used")
    ax.legend()
    ax.grid(True)

    return result_df, {'MAPE': mape, 'RMSE': rmse, 'MAE': mae}, fig
