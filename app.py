import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Ashbard Energy - Efficiency Tracker')

@st.cache_data
def load_data():
    ash = pd.read_csv(r"/mnt/data/ashbard_production.csv", parse_dates=['date'])
    dl = pd.read_csv(r"/mnt/data/dealership_energy.csv", parse_dates=['date'])
    return ash, dl

ash, dl = load_data()

st.title('Ashbard Energy — Efficiency & Operations')

st.sidebar.header('Filters')
date_min = st.sidebar.date_input('From', ash['date'].min().date())
date_max = st.sidebar.date_input('To', ash['date'].max().date())
well = st.sidebar.selectbox('Well', options=['ALL'] + sorted(ash['well_id'].unique().tolist()))

mask = (ash['date'].dt.date >= date_min) & (ash['date'].dt.date <= date_max)
if well != 'ALL':
    mask &= (ash['well_id'] == well)
df = ash[mask].copy()

st.header('Overview KPIs')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total BOE', f"{'{':}{''}")  # placeholder to avoid f-string eval here
col2.metric('Avg Energy (kWh/day)', f"{'{':}{''}")
col3.metric('Avg Energy/BOE', f"{'{':}{''}")
col4.metric('Operating cost (USD)', f"{'{':}{''}")

st.subheader('Production & Energy Trends')
fig, ax = plt.subplots(figsize=(12,4))
daily = df.groupby('date').agg({'production_boe':'sum','energy_kwh':'sum'}).reset_index()
ax.plot(daily['date'], daily['production_boe'], label='BOE/day')
ax.plot(daily['date'], daily['energy_kwh']/50, label='Energy/50 (scaled)')
ax.legend()
st.pyplot(fig)

st.subheader('Dealership Snapshot')
st.dataframe(dl.tail(10))

st.write('---')
st.write('This Streamlit app is a simple starter. For production, consider adding authentication, database integration, and more charts (plotly) + model endpoints for forecasting.')
