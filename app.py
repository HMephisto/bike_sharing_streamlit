import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.sidebar.title("🚴 Bike Sharing")
st.sidebar.page_link("app.py", label="🏠 Dashboard")
st.sidebar.page_link("pages/raw_data.py", label="📄 Raw Data")
st.sidebar.page_link("pages/analysis.py", label="📄 Analysis")
st.sidebar.page_link("pages/anggota.py", label="👤 About Us")

day_df = pd.read_csv("df_day_cleaned.csv")
hour_df = pd.read_csv("hour.csv")
day_df["date"] = pd.to_datetime(day_df["date"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

st.title("📊 Dashboard Overview")

st.markdown(
    """
    <style>
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        text-align: center; /* Memastikan teks di tengah */
    }
    .metric-label {
        color: #888;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #fff;
        font-size: 32px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Filters")
year = st.sidebar.selectbox(
    "Select Year",
    options=day_df["year"].unique(),
    format_func=lambda x: "2011" if x == 0 else "2012"
)

season = st.sidebar.multiselect(
    "Select Season",
    options=day_df["season"].unique(),
    default=day_df["season"].unique()
)

filtered_day = day_df[(day_df["year"] == year) & (day_df["season"].isin(season))]
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Rentals</div>
            <div class="metric-value">{int(filtered_day["total"].sum()):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Casual Users</div>
            <div class="metric-value">{int(filtered_day["casual"].sum()):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Registered Users</div>
            <div class="metric-value">{int(filtered_day["registered"].sum()):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Rentals Over Time")
    st.line_chart(filtered_day.set_index("date")["total"])

with chart_col2:
    st.subheader("👥 Casual vs Registered")
    st.bar_chart(filtered_day[["casual", "registered"]])

st.divider()
season_col, empty_col = st.columns(2)

with season_col:
    st.subheader("🌤 Rentals by Season")
    season_data = filtered_day.groupby("season")["total"].sum()
    st.bar_chart(season_data)