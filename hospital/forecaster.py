import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

class HospitalDemandForecaster:
    def __init__(self, file_path):
        self.file_path = file_path
        self.models = {}

    def preprocess_data(self):
        data = pd.read_excel(self.file_path)
        data.rename(columns={'Quantity_Used': 'Quantity_used'}, inplace=True)

        data['Week'] = pd.to_datetime(data['Week'])
        data.sort_values(['Item_Code', 'Week'], inplace=True)

        data['Lag_1'] = data.groupby('Item_Code')['Quantity_used'].shift(1)
        data['Lag_2'] = data.groupby('Item_Code')['Quantity_used'].shift(2)

        data = data.assign(week_index=data.groupby('Item_Code').cumcount() + 1)
        return data.dropna()

    def train_models(self, data):
        results = {}

        for item in data['Item_Code'].unique():
            item_data = data[data['Item_Code'] == item]

            train = item_data[item_data['week_index'] <= 148]
            test = item_data[item_data['week_index'] > 148]

            if len(train) == 0 or len(test) == 0:
                continue

            # Random Forest
            features = ['Patient_Footfall', 'Public_Holiday', 'Rain_Impact', 'Lag_1', 'Lag_2']
            X_train = train[features]
            y_train = train['Quantity_used']
            X_test = test[features]

            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_model.fit(X_train, y_train)
            rf_pred = rf_model.predict(X_test)

            actual = test['Quantity_used'].values
            rf_metrics = {
                'MAE': mean_absolute_error(actual, rf_pred),
                'MAPE': mean_absolute_percentage_error(actual, rf_pred) * 100,
                'RMSE': np.sqrt(mean_squared_error(actual, rf_pred))
            }

            results[item] = {
                'description': train['Item_Description'].iloc[0],
                'rf_metrics': rf_metrics,
                'actual': actual.tolist(),
                'rf_pred': rf_pred.tolist(),
                'weeks': test['week_index'].tolist()
            }

        return results

    def run_forecasting(self):
        data = self.preprocess_data()
        return self.train_models(data)
