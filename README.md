# Ashbard Energy — Production Efficiency Tracker (Sample Project)

This repository contains a synthetic dataset, a Jupyter Notebook for EDA/KPIs/Forecasting/Anomaly detection, and a Streamlit starter app for visualizing the data.

## Contents
- `ashbard_production.csv` — synthetic upstream production dataset
- `dealership_energy.csv` — synthetic car dealership energy & fleet dataset
- `Ashbard_Energy_Tracker.ipynb` — Jupyter Notebook (EDA, KPIs, anomaly detection, forecasting)
- `app.py` — Streamlit starter app
- `.github/workflows/ci.yml` — GitHub Actions workflow to run basic checks
- `Dockerfile` — Dockerfile to containerize the Streamlit app
- `requirements.txt` — Python dependencies

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
