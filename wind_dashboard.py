# Wind Energy Feasibility Dashboard (Enhanced for Submission)

import pandas as pd
import numpy as np
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import base64

# --- Dashboard Title ---
st.set_page_config(page_title="Wind Energy Feasibility", layout="wide")
st.title("Wind Energy Feasibility Dashboard")

# --- Introduction / Instructions ---
st.markdown("""
Welcome to the Wind Energy Feasibility Dashboard!

This dashboard helps you analyze historical wind speed data, forecast future wind speeds using the ARIMA model, 
and estimate potential energy generation from a small wind turbine.

**Instructions:**  
- Upload a CSV file containing two columns: `date` and `wspd` (wind speed in m/s).  
- Date format is flexible; the app will attempt to parse it automatically.  
- Forecast is for the next 30 days.
""")

# --- Sample CSV & Meteostat Instructions ---
st.markdown("### 📌 How to Get Wind Data")

sample_csv = """date,wspd
2024-01-01,5.2
2024-01-02,6.1
2024-01-03,4.8
2024-01-04,5.5
2024-01-05,6.3
"""

def generate_download_link(csv_string, filename):
    b64 = base64.b64encode(csv_string.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Sample CSV</a>'
    return href

st.markdown(
    "You have two options to get started with wind speed data:\n\n"
    "1. **🗂️ Use Sample Data**  \n" + generate_download_link(sample_csv, "sample_wind_data.csv") + "\n\n"
    "2. **🌐 Get Real Data from Meteostat**  \n"
    "- Visit: [https://meteostat.net/en/](https://meteostat.net/en/)  \n"
    "- Search for your city or location  \n"
    "- Choose 'Daily Data'  \n"
    "- Select your date range (e.g., Jan–Dec 2024)  \n"
    "- Click **Download CSV**\n\n"
    "Once you have your CSV file, upload it using the uploader below.",
    unsafe_allow_html=True
)

# --- Upload CSV File ---
uploaded_file = st.file_uploader("📁 Upload your wind data CSV", type="csv")

if uploaded_file is not None:
    try:
        wind_data = pd.read_csv(uploaded_file)
        wind_data.rename(columns=lambda col: col.strip().lower(), inplace=True)

        if 'date' not in wind_data.columns or 'wspd' not in wind_data.columns:
            st.error("CSV must contain 'date' and 'wspd' columns.")
        else:
            wind_data.rename(columns={'date': 'Date', 'wspd': 'WindSpeed'}, inplace=True)
            wind_data['Date'] = pd.to_datetime(wind_data['Date'], errors='coerce')
            wind_data.dropna(subset=['Date', 'WindSpeed'], inplace=True)

            # --- Historical Plot ---
            st.subheader(" Historical Wind Speed Data")
            st.line_chart(wind_data.set_index('Date')['WindSpeed'])

            # --- Forecasting ---
            st.subheader("🔮 Forecast Wind Speed (30 Days)")
            model = ARIMA(wind_data['WindSpeed'], order=(5, 1, 0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=30)
            forecast_dates = pd.date_range(start=wind_data['Date'].iloc[-1] + pd.Timedelta(days=1), periods=30)
            forecast_df = pd.DataFrame({'Date': forecast_dates, 'ForecastedWindSpeed': forecast})
            st.line_chart(forecast_df.set_index('Date'))

            # --- Energy Estimation ---
            st.subheader("⚡ Estimated Energy Generation (kW)")
            turbine_power_curve = lambda v: min(1.5 * (v ** 3) / 1000, 3)
            forecast_df['Energy_kW'] = forecast_df['ForecastedWindSpeed'].apply(turbine_power_curve)
            st.bar_chart(forecast_df.set_index('Date')['Energy_kW'])

            # --- Summary Statistics & CO₂ Impact ---
            avg_wind_speed = forecast_df['ForecastedWindSpeed'].mean()
            avg_energy = forecast_df['Energy_kW'].mean()
            estimated_monthly_output = avg_energy * 30
            co2_avoided = estimated_monthly_output * 0.8

            st.success(f" Average Forecasted Wind Speed: **{avg_wind_speed:.2f} m/s**")
            st.success(f" Average Estimated Energy Output: **{avg_energy:.2f} kW**")
            st.info(f" Estimated Monthly Output: **{estimated_monthly_output:.1f} kWh**")
            st.info(f" Estimated CO₂ Emissions Avoided: **{co2_avoided:.1f} kg/month**")
            st.caption("Note: CO₂ savings based on 0.8 kg CO₂/kWh grid offset.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV file to begin analysis.")
