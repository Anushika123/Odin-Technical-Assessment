from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def backend_pipeline(df):
    # Step 1: Feature selection
    features = ['Patient_Footfall', 'Last_Week_Usage', 'Public_Holiday', 'Rain_Impact']
    target = 'Quantity_Used'

    # Step 2: Handle missing data if any
    df = df.dropna(subset=features + [target])

    # Step 3: Train-test split (75% train, 25% test)
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Step 4: Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Step 5: Predict on test set
    y_pred = model.predict(X_test)

    # Step 6: Evaluation
    evaluation_df = pd.DataFrame({
        'Actual': y_test.values,
        'Predicted': y_pred
    }).reset_index(drop=True)

    # Optional: Add index as pseudo weeks for plotting
    evaluation_df['Week'] = range(1, len(evaluation_df) + 1)

    # Step 7: Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    metrics = {
        'MAE': round(mae, 2),
        'RMSE': round(rmse, 2),
        'MAPE': round(mape, 2)
    }

    return metrics, evaluation_df
