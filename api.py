from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib, pandas as pd
from datetime import datetime, timedelta

app = FastAPI(title='Ashbard Production Forecast API')

MODEL_PATH = 'models/rf_production_model.joblib'

class ForecastRequest(BaseModel):
    days: int = 14
    last_known_date: str = None  # ISO date string, optional

# Load model at startup
_art = joblib.load(MODEL_PATH)
model = _art['model']
features = _art['features']

# Helper to create features given historical series (pandas Series indexed by date)
def make_feature_row(history_df, predict_date):
    # history_df must contain 'production_boe' and 'energy_kwh' for recent dates
    # We'll compute lag_1, lag_7, roll_7_mean and dayofweek for predict_date
    last = history_df.sort_index()
    lag_1 = float(last['production_boe'].iloc[-1])
    lag_7 = float(last['production_boe'].iloc[-7]) if len(last)>=7 else float(last['production_boe'].iloc[0])
    roll_7 = float(last['production_boe'].rolling(7, min_periods=1).mean().iloc[-1])
    dayofweek = predict_date.weekday()
    # For energy_kwh we'll use the average recent energy as a proxy
    energy_kwh = float(last['energy_kwh'].iloc[-1])
    return {'lag_1':lag_1,'lag_7':lag_7,'roll_7_mean':roll_7,'energy_kwh':energy_kwh,'dayofweek':dayofweek}

@app.post('/forecast')
def forecast(req: ForecastRequest):
    days = req.days if req.days>0 and req.days<=180 else 14
    # Load historical data (assumes CSV in working dir)
    try:
        df = pd.read_csv('ashbard_production.csv', parse_dates=['date']).set_index('date').sort_index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed loading data: {e}')
    history = df[['production_boe','energy_kwh']].copy()
    results = []
    last_date = history.index.max()
    if req.last_known_date:
        last_date = pd.to_datetime(req.last_known_date)
    for i in range(1, days+1):
        pred_date = last_date + timedelta(days=i)
        feats = make_feature_row(history, pred_date)
        X = pd.DataFrame([feats])[features]
        pred = model.predict(X)[0]
        # append prediction to history so next step can use it as lag
        history.loc[pred_date] = {'production_boe': float(pred), 'energy_kwh': feats['energy_kwh']}
        results.append({'ds': pred_date.strftime('%Y-%m-%d'), 'yhat': float(pred)})
    return {'predictions': results}
