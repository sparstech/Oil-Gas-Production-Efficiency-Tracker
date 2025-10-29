# Ashbard Energy — Production Efficiency Tracker Project

This repository contains a synthetic dataset, a Jupyter Notebook for EDA/KPIs/Forecasting/Anomaly detection, and a Streamlit starter app for visualizing the data.

## Contents
ashbard_energy_project/
├── data/production_data.csv
├── models/
│   ├── efficiency_model.pkl
│   └── shap_summary.png
├── serve_api.py          # Flask API for probabilistic forecasts
├── app.py                # Streamlit visualization
├── Ashbard_Energy_Tracker.ipynb
├── requirements.txt
├── Dockerfile
└── README.md


## Quick start (locally)
1. Create a virtual environment: `python -m venv venv`
2. Activate it and install requirements: `pip install -r requirements.txt`
3. Run the notebook in JupyterLab/Notebook or open `Ashbard_Energy_Tracker.ipynb`
4. Run the Streamlit app: `streamlit run app.py`

## Docker
Build and run the Streamlit app with Docker:
```
docker build -t ashbard-energy-app .
docker run -p 8501:8501 ashbard-energy-app
```

## CI
A GitHub Actions workflow runs `pip install -r requirements.txt` and executes the notebook using `nbconvert --execute` as a smoke test.
