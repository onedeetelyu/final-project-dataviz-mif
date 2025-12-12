import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Final Project - Data Visualization",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# TITLE & INTRO
# =========================================================
st.title("📊 Interactive Data Visualization Dashboard")
st.markdown("""
**Final Project – Visualisasi Data Interaktif**

Dashboard ini dibuat untuk memenuhi tugas **Final Project** mata kuliah
**Visualisasi Data**, dengan fokus pada:
- eksplorasi data secara interaktif
- analisis visual berbasis pengguna
- penyajian insight yang mudah dipahami
""")

st.divider()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.header("⚙️ Kontrol Interaktif")

# Dummy pilihan (nanti bisa diganti sesuai dataset)
selected_metric = st.sidebar.selectbox(
    "Pilih metrik:",
    ["Metrik A", "Metrik B", "Metrik C"]
)

year_range = st.sidebar.slider(
    "Rentang tahun:",
    2015, 2025, (2018, 2024)
)

# =========================================================
# LOAD DATA (CONTOH)
# =========================================================
@st.cache_data
def load_data():
    # DATA CONTOH (nanti ganti dataset asli)
    data = pd.DataFrame({
        "Year": np.arange(2015, 2026),
        "Value_A": np.random.randint(50, 100, 11),
        "Value_B": np.random.randint(30, 80, 11),
        "Value_C": np.random.randint(10, 60, 11)
    })
    return data

df = load_data()

# =========================================================
# FILTER DATA
# =========================================================
df_filtered = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# Mapping metric
metric_map = {
    "Metrik A": "Value_A",
    "Metrik B": "Value_B",
    "Metrik C": "Value_C"
}

metric_col = metric_map[selected_metric]

# =========================================================
# VISUALIZATION
# =========================================================
st.subheader("📈 Visualisasi Interaktif")

fig = px.line(
    df_filtered,
    x="Year",
    y=metric_col,
    markers=True,
    title=f"Perkembangan {selected_metric}"
)

fig.update_layout(
    xaxis_title="Tahun",
    yaxis_title=selected_metric,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# DATA TABLE (DETAILS ON DEMAND)
# =========================================================
with st.expander("📋 Lihat Data Tabel"):
    st.dataframe(df_filtered, use_container_width=True)

# =========================================================
# INSIGHT SECTION
# =========================================================
st.subheader("🧠 Insight Singkat")

st.write(f"""
Berdasarkan visualisasi **{selected_metric}** pada rentang tahun
**{year_range[0]}–{year_range[1]}**, terlihat adanya variasi nilai
yang dapat dianalisis lebih lanjut oleh pengguna.
""")

# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption("© Final Project Visualisasi Data | Streamlit Dashboard")