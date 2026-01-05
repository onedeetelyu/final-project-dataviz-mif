# =========================================================
# Bandung Weather Interactive Dashboard
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================================================
# PAGE CONFIG
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

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Parse date
    df["date"] = pd.to_datetime(df["date"])

    return df

df = load_data()

# =========================================================
# TITLE & INTRO
# =========================================================
# st.title("🌦️ Interactive Analysis of Daily Weather Patterns in Bandung (2024–2025)")
st.title("🌦️ Bandung Weather Interactive Dashboard: Exploratory Analysis (2024-25)")
st.markdown("""
This dashboard presents **interactive visualizations of daily weather data for Bandung City (2024–2025)** based on observations from the **Indonesian Meteorological, Climatological, and Geophysical Agency (BMKG)**.

"The dashboard emphasizes interpretability and interactive exploration rather than prediction."

The visualization is designed to support **exploratory analysis** by combining time-series trends, rolling statistics, and variability indicators to help users better understand both **short-term fluctuations** and **longer-term patterns**.

**Key objectives of this dashboard include:**
- Exploring temporal trends of temperature, rainfall, wind speed, and humidity
- Comparing multiple weather variables using dynamic rolling windows
- Visualizing uncertainty through rolling averages and standard deviation bands
- Analyzing the distribution and seasonality of weather categories interactively
            
💡 *Use the interactive controls (sliders, dropdowns, and hover tooltips) to customize the visualizations and reveal detailed insights.*
""")

st.divider()

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("⚙️ Interactive Filters")

# Date range slider (daily)
date_range = st.sidebar.slider(
    "Select date range:",
    min_value=df["date"].min().date(),
    max_value=df["date"].max().date(),
    value=(df["date"].min().date(), df["date"].max().date())
)

# WINDOW_OPTIONS = {
#     "1 day": 1,
#     "3 days": 3,
#     "7 days": 7,
#     "14 days": 14,
#     "30 days": 30,
#     # "90 days": 90,
#     # "365 days": 365,
# }

# selected_window_label = st.sidebar.radio(
#     "Select rolling window:",
#     list(WINDOW_OPTIONS.keys()),
#     index=3  # default 14 days
# )

# WINDOW_DAYS = WINDOW_OPTIONS[selected_window_label]

WINDOW_LABELS = {
    1: "Daily",
    3: "3-Day Avg",
    7: "Weekly Avg",
    14: "Bi-Weekly Avg",
    30: "Monthly Avg",
}

WINDOW_DAYS = st.sidebar.radio(
    "Rolling Averaging Window",
    options=[1, 3, 7, 14, 30],
    format_func=lambda x: WINDOW_LABELS[x],
    horizontal=False
)

# # Weather category filter
# weather_options = df["weather_class"].unique().tolist()
# selected_weather = st.sidebar.multiselect(
#     "Select weather category:",
#     weather_options,
#     default=weather_options
# )

# =========================================================
# FILTER DATA
# =========================================================
df_filtered = df[
    (df["date"].dt.date >= date_range[0]) &
    (df["date"].dt.date <= date_range[1]) # &
    # (df["weather_class"].isin(selected_weather))
]

# =========================================================
# SUMMARY STATISTICS
# =========================================================
st.subheader("📊 Summary Statistics")

selected_years = sorted(df_filtered["date"].dt.year.unique())

cols = st.columns(6)

# Hitung nilai utama
max_temp = df_filtered["temp_max"].max()
min_temp = df_filtered["temp_min"].min()
# avg_wind = df_filtered["wind_avg"].mean()
avg_max_wind = df_filtered["wind_max"].mean()
avg_rain = df_filtered["rain"].mean()
avg_humidity = df_filtered["humidity"].mean()

# Jika hanya 1 tahun → TANPA delta
if len(selected_years) == 1:
    cols[0].metric(f"Record Max Temperature (°C) in {selected_years[0]}", f"{max_temp:.1f}")
    cols[1].metric(f"Record Min Temperature (°C) in {selected_years[0]}", f"{min_temp:.1f}")
    # cols[2].metric(f"Average Wind (m/s) in {selected_years[0]}", f"{avg_wind:.2f}")
    cols[2].metric(f"Average Max Wind (m/s) in {selected_years[0]}", f"{avg_max_wind:.2f}")
    cols[3].metric(f"Average Rainfall (mm) in {selected_years[0]}", f"{avg_rain:.2f}")
    cols[4].metric(f"Average Humidity (%) in {selected_years[0]}", f"{avg_humidity:.1f}")

# Jika ≥ 2 tahun → PAKAI delta
else:
    y_curr, y_prev = selected_years[-1], selected_years[-2]

    df_curr = df_filtered[df_filtered["date"].dt.year == y_curr]
    df_prev = df_filtered[df_filtered["date"].dt.year == y_prev]

    cols[0].metric(
        f"Record Max Temperature (°C) in {y_curr}",
        f"{df_curr['temp_max'].max():.1f}",
        delta=f"{df_curr['temp_max'].max() - df_prev['temp_max'].max():+.1f} from {y_prev}"
    )

    cols[1].metric(
        f"Record Min Temperature (°C) in {y_curr}",
        f"{df_curr['temp_min'].min():.1f}",
        delta=f"{df_curr['temp_min'].min() - df_prev['temp_min'].min():+.1f} from {y_prev}"
    )

    # cols[2].metric(
    #     f"Average Wind (m/s) in {y_curr}",
    #     f"{df_curr['wind_avg'].mean():.2f}",
    #     delta=f"{df_curr['wind_avg'].mean() - df_prev['wind_avg'].mean():+.2f} from {y_prev}"
    # )

    cols[2].metric(
        f"Record Max Wind (m/s) in {y_curr}",
        f"{df_curr['wind_max'].mean():.2f}",
        delta=f"{df_curr['wind_max'].mean() - df_prev['wind_max'].mean():+.2f} from {y_prev}"
    )

    cols[3].metric(
        f"Average Rainfall (mm) in {y_curr}",
        f"{df_curr['rain'].mean():.2f}",
        delta=f"{df_curr['rain'].mean() - df_prev['rain'].mean():+.2f} from {y_prev}"
    )

    cols[4].metric(
        f"Average Humidity (%) in {y_curr}",
        f"{df_curr['humidity'].mean():.1f}",
        delta=f"{df_curr['humidity'].mean() - df_prev['humidity'].mean():+.1f} from {y_prev}"
    )

weather_icons = {
    "Sunny": "☀️",
    "Partly Cloudy": "⛅",
    "Cloudy": "☁️",
    "Light Rain": "🌦️",
    "Moderate Rain": "🌧️",
    "Heavy Rain": "⛈️",
}

most_common_weather = df_filtered["weather_class"].value_counts().idxmax()

cols[5].metric(
    "Most Common Weather",
    f"{weather_icons.get(most_common_weather, '🌤️')} {most_common_weather}"
)

st.divider()

# =========================================================
# VISUALIZATIONS
# =========================================================
st.subheader("📊 Weather Visualizations")

df_plot = df_filtered.copy()

df_plot["month"] = df_plot["date"].dt.to_period("M").dt.to_timestamp()

window_safe = min(WINDOW_DAYS, len(df_plot))

# ---------- ROLLING COMPUTATIONS ----------
df_plot = df_filtered.copy()

# TEMPERATURE
df_plot["temp_max_roll"] = (
    df_plot["temp_max"]
    .rolling(window=window_safe, min_periods=1)
    .mean()
)

df_plot["temp_min_roll"] = (
    df_plot["temp_min"]
    .rolling(window=window_safe, min_periods=1)
    .mean()
)

df_plot["temp_avg_roll"] = (
    df_plot["temp_avg"]
    .rolling(window=window_safe, min_periods=1)
    .mean()
)

# WIND
# df_plot["wind_avg_roll"] = df_plot["wind_avg"].rolling(window_safe, 1).mean()
# df_plot["wind_std_roll"] = df_plot["wind_avg"].rolling(window_safe, 1).std()

# df_plot["wind_upper"] = df_plot["wind_avg_roll"] + df_plot["wind_std_roll"]
# df_plot["wind_lower"] = df_plot["wind_avg_roll"] - df_plot["wind_std_roll"]

df_plot["wind_max_avg_roll"] = df_plot["wind_max"].rolling(window_safe, 1).mean()
df_plot["wind_max_std_roll"] = df_plot["wind_max"].rolling(window_safe, 1).std()

df_plot["wind_upper"] = df_plot["wind_max_avg_roll"] + df_plot["wind_max_std_roll"]
df_plot["wind_lower"] = df_plot["wind_max_avg_roll"] - df_plot["wind_max_std_roll"]

# RAIN
df_plot["rain_roll"] = df_plot["rain"].rolling(window_safe, 1).mean()
df_plot["rain_std"] = df_plot["rain"].rolling(window_safe, 1).std()

df_plot["rain_upper"] = df_plot["rain_roll"] + df_plot["rain_std"]
df_plot["rain_lower"] = df_plot["rain_roll"] - df_plot["rain_std"]

# HUMIDITY
df_plot["hum_roll"] = df_plot["humidity"].rolling(window_safe, 1).mean()
df_plot["hum_std"] = df_plot["humidity"].rolling(window_safe, 1).std()

df_plot["hum_upper"] = df_plot["hum_roll"] + df_plot["hum_std"]
df_plot["hum_lower"] = df_plot["hum_roll"] - df_plot["hum_std"]

# MONTH
df_plot["month"] = df_plot["date"].dt.month_name()

COLORS = {
    # 🔥 TEMPERATURE (Fire)
    "temp_avg": "#B22222",                # Firebrick (deep red)
    "temp_range": "rgba(178,34,34,0.25)", # soft red band

    # 🌬️ WIND (Air – white blue)
    "wind": "#6EC1E4",                    # light sky blue
    "wind_band": "rgba(110,193,228,0.25)",

    # 🌊 RAIN (Water – deep blue)
    "rain": "#1F4E79",                    # strong blue
    "rain_band": "rgba(31,78,121,0.25)",

    # 🌿 HUMIDITY (Earth/Plant – green)
    "humidity": "#2E8B57",                # sea green
    "humidity_band": "rgba(46,139,87,0.25)",
}

WEATHER_COLORS = {
    "Sunny": "#FDB813",           # warm yellow (sun)
    "Partly Cloudy": "#B3DDF2",   # soft sky blue
    "Cloudy": "#9E9E9E",          # neutral gray
    "Light Rain": "#6EC1E4",      # light blue rain
    "Moderate Rain": "#2F80ED",   # strong blue
    "Heavy Rain": "#1C3F95",      # deep navy (not black)
}

# ---------- ROW 1 ----------
col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()

    # Temperature max
    fig.add_trace(
        go.Scatter(
            x=df_plot["date"],
            y=df_plot["temp_max_roll"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    # Temperature min (range)
    fig.add_trace(
        go.Scatter(
            x=df_plot["date"],
            y=df_plot["temp_min_roll"],
            mode="lines",
            fill="tonexty",
            fillcolor=COLORS["temp_range"],
            line=dict(width=0),
            name="Rolling Temp Range (Min–Max)",
            customdata=df_plot["temp_max_roll"],
            hovertemplate=
            "<b>Max Temp:</b> %{customdata:.1f} °C<br>" +
            "<b>Min Temp:</b> %{y:.1f} °C" +
            "<extra></extra>"
        )
    )

    # Average temperature
    fig.add_trace(
        go.Scatter(
            x=df_plot["date"],
            y=df_plot["temp_avg_roll"],
            mode="lines",
            line=dict(color=COLORS["temp_avg"], width=2),
            name=f"Rolling Avg Temp",
            hovertemplate=
            "<b>Avg Temp:</b> %{y:.1f}°C" +
            "<extra></extra>"
        )
    )

    def comfort_line(fig, y, label):
        fig.add_hline(
            y=y,
            line_dash="dot",
            line_color="gray",
            annotation_text=label,
            annotation_position="top right",
            annotation=dict(
                font=dict(color="rgba(255,255,255,0.4)", size=10)
            )
        )

    comfort_line(fig, 35, "Sweltering")
    comfort_line(fig, 29, "Hot")
    comfort_line(fig, 24, "Warm")
    comfort_line(fig, 18, "Comfortable")

    fig.update_layout(
        height=400,
        hovermode="x unified",
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
        title=f"Temperature ({WINDOW_DAYS}-Day Rolling Avg and Range)",  
    )

    st.plotly_chart(fig, width='content')

with col2:
    fig_wind = go.Figure()

    fig_wind.add_trace(go.Scatter(
        x=df_plot["date"], y=df_plot["wind_upper"],
        line=dict(width=0), showlegend=False, hoverinfo="skip"
    ))

    fig_wind.add_trace(go.Scatter(
        x=df_plot["date"], y=df_plot["wind_lower"],
        fill="tonexty",
        fillcolor=COLORS["wind_band"],
        line=dict(width=0),
        name="±1 Std Dev",
        hoverinfo="skip"
    ))

    fig_wind.add_trace(
        go.Scatter(
            x=df_plot["date"],
            y=df_plot["wind_max_avg_roll"],
            mode="lines",
            line=dict(color=COLORS["wind"], width=2),
            name="Rolling Avg Max Wind",
            customdata=df_plot["wind_max_std_roll"],
            hovertemplate=
            "<b>Avg Max Wind:</b> %{y:.2f} m/s<br>" +
            "<b>Std Dev:</b> %{customdata:.2f} m/s" +
            "<extra></extra>"
        )
    )

    def wind_levels(fig_wind):
        levels = [
            (1.5, "Calm"),
            (3.3, "Breeze"),
            (5.5, "Fresh Breeze"),
            (8.0, "Strong Wind"),
        ]

        for y, label in levels:
            fig_wind.add_hline(
                y=y,
                line_dash="dot",
                line_color="gray",
                annotation_text=label,
                annotation_position="top right",
                annotation=dict(
                    font=dict(color="rgba(255,255,255,0.4)", size=10)
                )
            )

    wind_levels(fig_wind)
    
    fig_wind.update_layout(
        height=400,
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
        xaxis_title="Date",
        yaxis_title="Max Wind Speed (m/s)",
        title=f"Max Wind Speed ({WINDOW_DAYS}-Day Rolling Avg ± 1 Std)",        
    )

    st.plotly_chart(fig_wind, width='content')

# ---------- ROW 2 ----------
col3, col4 = st.columns(2)

with col3:
    fig_rain = go.Figure()

    fig_rain.add_trace(go.Scatter(
        x=df_plot["date"], y=df_plot["rain_upper"],
        line=dict(width=0), showlegend=False, hoverinfo="skip"
    ))

    fig_rain.add_trace(go.Scatter(
        x=df_plot["date"], y=df_plot["rain_lower"],
        fill="tonexty",
        fillcolor=COLORS["rain_band"],
        line=dict(width=0),
        name="±1 Std Dev",
        hoverinfo="skip"
    ))

    fig_rain.add_trace(
        go.Scatter(
            x=df_plot["date"],
            y=df_plot["rain_roll"],
            mode="lines",
            line=dict(color=COLORS["rain"], width=2),
            name="Rolling Avg Rain",
            customdata=df_plot["rain_std"],
            hovertemplate=
            "<b>Avg Rain:</b> %{y:.2f} mm<br>" +
            "<b>Std Dev:</b> %{customdata:.2f} mm" +
            "<extra></extra>"
        )
    )

    def rain_levels(fig_rain):
        levels = [
            (5, "Light Rain"),
            (20, "Moderate Rain"),
            (50, "Heavy Rain"),
        ]

        for y, label in levels:
            fig_rain.add_hline(
                y=y,
                line_dash="dot",
                line_color="gray",
                annotation_text=label,
                annotation_position="top right",
                annotation=dict(
                    font=dict(color="rgba(255,255,255,0.4)", size=10)
                )
            )

    rain_levels(fig_rain)

    fig_rain.update_layout(
        height=400,
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
        xaxis_title="Date",
        yaxis_title="Rainfall (mm)",
        title=f"Rainfall ({WINDOW_DAYS}-Day Rolling Avg ± 1 Std)",
    )

    st.plotly_chart(fig_rain, width='content')

with col4:
    fig_hum = go.Figure()

    fig_hum.add_trace(go.Scatter(
        x=df_plot["date"], y=df_plot["hum_upper"],
        line=dict(width=0), showlegend=False, hoverinfo="skip"
    ))

    fig_hum.add_trace(go.Scatter(
        x=df_plot["date"], y=df_plot["hum_lower"],
        fill="tonexty",
        fillcolor=COLORS["humidity_band"],
        line=dict(width=0),
        name="±1 Std Dev",
        hoverinfo="skip"
    ))

    fig_hum.add_trace(
        go.Scatter(
            x=df_plot["date"],
            y=df_plot["hum_roll"],
            mode="lines",
            line=dict(color=COLORS["humidity"], width=2),
            name="Rolling Avg Humidity",
            customdata=df_plot["hum_std"],
            hovertemplate=
            "<b>Avg Humidity:</b> %{y:.1f} %<br>" +
            "<b>Std Dev:</b> %{customdata:.1f} %" +
            "<extra></extra>"
        )
    )

    def humidity_levels(fig_hum):
        levels = [
            (60, "Dry"),
            (75, "Comfort"),
            (85, "Humid"),
            (90, "Very Humid"),
        ]

        for y, label in levels:
            fig_hum.add_hline(
                y=y,
                line_dash="dot",
                line_color="gray",
                annotation_text=label,
                annotation_position="top right",
                annotation=dict(
                    font=dict(color="rgba(255,255,255,0.4)", size=10)
                )
            )

    humidity_levels(fig_hum)

    fig_hum.update_layout(
        height=400,
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
        xaxis_title="Date",
        yaxis_title="Humidity (%)",
        title=f"Humidity ({WINDOW_DAYS}-Day Rolling Avg ± 1 Std)",
    )

    st.plotly_chart(fig_hum, width='content')

# ---------- ROW 3 ----------
col5, col6 = st.columns(2)

with col5:
    fig_weather = px.pie(
        df_plot,
        names="weather_class",
        color="weather_class",
        color_discrete_map=WEATHER_COLORS,
        title="Weather Category Distribution"
    )

    fig_weather.update_layout(
        height=400, 
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center")
    )

    st.plotly_chart(fig_weather, width='content')

with col6:
    fig_month = px.histogram(
        df_plot,
        x="month",
        color="weather_class",
        color_discrete_map=WEATHER_COLORS,
        barmode="stack",
        barnorm="percent",
        category_orders={
            "month": [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
        },
        labels={"month": "Month", "count": "Percentage (%)"},
        title="Monthly Weather Distribution (Percentage)",
    )

    fig_month.update_layout(
        height=400,
        yaxis_title="Percentage of Days (%)",
        legend_title="Weather Class",
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center")
    )

    st.plotly_chart(fig_month, width='content')

st.divider()
# =========================================================
# RAW DATA
# =========================================================
with st.expander("📋 View Raw Data"):
    st.dataframe(df_filtered, width='content')

st.divider()
# =========================================================
# FOOTER
# =========================================================
st.caption("© Final Project – Data Visualization | Made by Wandi Yusuf Kurniawan - 203012320013 | 2026")
