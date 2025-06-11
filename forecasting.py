# forecast.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


def train_and_forecast(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    output_rows = []
    all_actuals = []
    all_predictions = []
    metrics = {}

    for item in df['item_code'].unique():
        item_df = df[df['item_code'] == item].reset_index(drop=True)
        item_df['week'] = item_df.index + 1

        if item_df['week'].max() < 156:
            continue

        train_df = item_df[item_df['week'] <= 148]
        test_df = item_df[(item_df['week'] > 148) & (item_df['week'] <= 156)]

        features = ['patient_footfall', 'last_week_usage', 'public_holiday', 'rain_impact']
        target = 'quantity_used'

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(train_df[features], train_df[target])

        predictions = model.predict(test_df[features])
        test_df = test_df.copy()
        test_df['predicted'] = predictions

        all_actuals.extend(test_df[target].values)
        all_predictions.extend(predictions)

        for _, row in test_df.iterrows():
            output_rows.append({
                'Item_Code': item,
                'Week': int(row['week']),
                'Actual': row[target],
                'Predicted': row['predicted']
            })

        mape = np.mean(np.abs((test_df[target] - predictions) / test_df[target])) * 100
        rmse = np.sqrt(mean_squared_error(test_df[target], predictions))
        mae = mean_absolute_error(test_df[target], predictions)

        metrics[item] = {
            'MAPE (%)': round(mape, 2),
            'RMSE': round(rmse, 2),
            'MAE': round(mae, 2)
        }

    overall_mape = np.mean(np.abs((np.array(all_actuals) - np.array(all_predictions)) / np.array(all_actuals))) * 100
    overall_rmse = np.sqrt(mean_squared_error(all_actuals, all_predictions))
    overall_mae = mean_absolute_error(all_actuals, all_predictions)

    metrics['Overall'] = {
        'MAPE (%)': round(overall_mape, 2),
        'RMSE': round(overall_rmse, 2),
        'MAE': round(overall_mae, 2)
    }

    result_df = pd.DataFrame(output_rows)
    return result_df, metrics
