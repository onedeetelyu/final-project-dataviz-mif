# =========================================================
# Bandung Weather Interactive Dashboard
# =========================================================

import streamlit as st
import pandas as pd
import altair as alt

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Bandung Weather Dashboard",
    page_icon="🌦️",
    layout="wide",
)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("weather_bandung_2024_25.csv")

    # Standarisasi nama kolom → lowercase + underscore
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Parse tanggal
    df["date"] = pd.to_datetime(df["date"])

    return df

df = load_data()

# =========================================================
# TITLE
# =========================================================
st.title("🌦️ Bandung Weather Interactive Dashboard")
st.markdown("""
Dashboard ini menyajikan **visualisasi interaktif data cuaca Kota Bandung (2024–2025)**  
berdasarkan data BMKG, dengan fokus pada:
- eksplorasi tren cuaca
- distribusi kategori cuaca
- perbandingan antar waktu
""")

st.divider()

# =========================================================
# SIDEBAR FILTER
# =========================================================
st.sidebar.header("⚙️ Interactive Filters")

years = sorted(df["date"].dt.year.unique())
selected_years = st.sidebar.multiselect(
    "Select year(s):",
    years,
    default=years
)

weather_types = sorted(df["weather_class"].dropna().unique())
selected_weather = st.sidebar.multiselect(
    "Select weather category:",
    weather_types,
    default=weather_types
)

filtered_df = df[
    (df["date"].dt.year.isin(selected_years)) &
    (df["weather_class"].isin(selected_weather))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# =========================================================
# METRICS SUMMARY
# =========================================================
st.subheader("📊 Summary Statistics")

cols = st.columns(4)

cols[0].metric("Max Temperature (°C)", f"{df['temp_max'].max():.1f}")
cols[1].metric("Min Temperature (°C)", f"{df['temp_min'].min():.1f}")
cols[2].metric("Total Rainfall (mm)", f"{df['rain'].sum():.1f}")
cols[3].metric("Avg Humidity (%)", f"{df['humidity'].mean():.1f}")

st.divider()

# =========================================================
# TEMPERATURE RANGE CHART
# =========================================================
st.subheader("🌡️ Daily Temperature Range")

temp_chart = (
    alt.Chart(filtered_df)
    .mark_bar(width=2)
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("temp_max:Q", title="Temperature (°C)"),
        y2="temp_min:Q",
        color=alt.Color("date:T", timeUnit="year", title="Year"),
        tooltip=["date", "temp_min", "temp_max"]
    )
    .interactive()
)

st.altair_chart(temp_chart, width='stretch')

# =========================================================
# WEATHER DISTRIBUTION
# =========================================================
st.subheader("☁️ Weather Category Distribution")

weather_pie = (
    alt.Chart(filtered_df)
    .mark_arc()
    .encode(
        theta=alt.Theta("count():Q"),
        color=alt.Color("weather_class:N", title="Weather"),
        tooltip=["weather_class", "count()"]
    )
)

st.altair_chart(weather_pie, width='stretch')

# =========================================================
# RAINFALL OVER TIME
# =========================================================
st.subheader("🌧️ Rainfall Over Time")

rain_chart = (
    alt.Chart(filtered_df)
    .mark_line()
    .encode(
        x="date:T",
        y=alt.Y("rain:Q", title="Rainfall (mm)"),
        tooltip=["date", "rain"]
    )
    .interactive()
)

st.altair_chart(rain_chart, width='stretch')

# =========================================================
# MONTHLY WEATHER BREAKDOWN
# =========================================================
st.subheader("📅 Monthly Weather Breakdown")

monthly_weather = (
    alt.Chart(filtered_df)
    .mark_bar()
    .encode(
        x=alt.X("month(date):O", title="Month"),
        y=alt.Y("count():Q", title="Number of Days").stack("normalize"),
        color=alt.Color("weather_class:N", title="Weather"),
        tooltip=["weather_class", "count()"]
    )
)

st.altair_chart(monthly_weather, width='stretch')

# =========================================================
# RAW DATA
# =========================================================
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered_df)

st.caption("© Final Project Visualisasi Data | Bandung Weather Dashboard")