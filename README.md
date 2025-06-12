# 🌬️ Wind Energy Feasibility Dashboard

This is an interactive Streamlit dashboard that helps users assess the wind energy potential for a given location. The tool forecasts wind speed using time-series analysis and estimates energy output from a small wind turbine.

## 📊 Features

- Upload real wind speed data (e.g., from [Meteostat](https://meteostat.net))
- Forecast next 30 days of wind speed using ARIMA model
- Estimate energy output (kW) using a cubic turbine power curve
- Visualize historical and forecast data using clean, interactive charts

## 📁 File Structure

- `wind_dashboard.py` — Main Streamlit dashboard code
- `requirements.txt` — Required libraries for deployment
##🌐 Live Demo

[Click here to view the live dashboard](https://wind-energy-dashboardgit-mapnx7k5pdgborozbb9xbh.streamlit.app/)

## 🚀 How to Run Locally 

```bash
pip install -r requirements.txt
streamlit run wind_dashboard.py


