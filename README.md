# 🌦️ Bandung Weather Interactive Dashboard

An interactive data visualization dashboard for exploring **daily weather conditions in Bandung City (Indonesia)** using official **BMKG observations**.

This project was developed as a **Final Project for Data Visualization**, focusing on:
- interactive exploration
- comparative analysis
- time-series weather patterns

---

## 📌 Features

✔ Interactive time-series visualization  
✔ Rolling average & variability analysis  
✔ Multi-variable weather comparison  
✔ Weather category distribution  
✔ Year-to-year statistical comparison  
✔ Fully interactive Plotly-based charts  

---

## 📊 Dataset

**Source:**  
Badan Meteorologi, Klimatologi, dan Geofisika (BMKG)  
https://dataonline.bmkg.go.id/

**Time span:**  
2024 – 2025 (daily observations)

**Variables used:**
- Temperature (min, max, average)
- Rainfall
- Humidity
- Sunshine duration
- Wind speed (average & maximum)
- Weather category (rule-based classification)

---

## 🌤️ Weather Classification

Daily weather conditions are classified into **6 simplified categories** based on BMKG-inspired rules:

- Sunny
- Partly Cloudy
- Cloudy
- Light Rain
- Moderate Rain
- Heavy Rain

The classification is **rule-based**, interpretable, and designed for visualization purposes.

---

## 📈 Visualizations Included

- **Temperature Range & Rolling Average**
- **Wind Speed (Rolling Avg ± Standard Deviation)**
- **Rainfall (Rolling Avg ± Standard Deviation)**
- **Humidity (Rolling Avg ± Standard Deviation)**
- **Weather Category Distribution**
- **Monthly Weather Distribution (Normalized)**

All charts support:
- zooming
- panning
- hover tooltips
- dynamic filtering

---

## 🧠 Methodology

- Data preprocessing using `pandas`
- Rolling window statistics for trend smoothing
- Standard deviation bands for variability analysis
- Interactive visualization using `plotly`
- Dashboard layout built with `streamlit`

---

## 🚀 Deployment

This dashboard is deployed using **Streamlit Cloud**.

To run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 👤 Author

**Wandi Yusuf Kurniawan - 203012320013**
Final Project – Advanced Data Visualization
Telkom University

---

© 2026
