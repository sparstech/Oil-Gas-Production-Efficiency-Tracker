"""Train model for Ashbard production forecasting and save artifact.
Run: python train_model.py
"""
import pandas as pd, joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

df = pd.read_csv('ashbard_production.csv', parse_dates=['date']).sort_values('date')
df['lag_1'] = df['production_boe'].shift(1)
df['lag_7'] = df['production_boe'].shift(7)
df['roll_7_mean'] = df['production_boe'].rolling(7,min_periods=1).mean().shift(1)
df['dayofweek'] = df['date'].dt.dayofweek
df = df.dropna().reset_index(drop=True)

features = ['lag_1', 'lag_7', 'roll_7_mean', 'energy_kwh', 'dayofweek']
X = df[features]
y = df['production_boe']

split_idx = int(len(df)*0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
print('Test MAE:', mae)

joblib.dump({'model': model, 'features': features}, 'models/rf_production_model.joblib')
with open('models/model_metadata.json','w') as f:
    import json
    json.dump({'model':'RandomForestRegressor','mae_test': float(mae),'features': features}, f, indent=2)
print('Model saved to models/rf_production_model.joblib')
