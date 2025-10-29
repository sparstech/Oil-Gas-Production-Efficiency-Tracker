
from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
model = joblib.load('models/efficiency_model.pkl')

@app.route('/forecast', methods=['POST'])
def forecast():
    input_data = request.get_json()
    df = pd.DataFrame(input_data)
    preds = [est.predict(df) for est in model.estimators_]
    mean_pred = np.mean(preds, axis=0)
    std_pred = np.std(preds, axis=0)
    return jsonify({
        "forecast_mean": mean_pred.tolist(),
        "forecast_std": std_pred.tolist()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
