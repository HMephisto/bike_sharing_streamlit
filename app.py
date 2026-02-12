import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# =========================
# SIDEBAR NAVIGATION
# =========================
st.sidebar.title("🚴 Bike Sharing")

st.sidebar.page_link("app.py", label="📊 Dashboard")
st.sidebar.page_link("pages/raw_data.py", label="📄 Raw Data")
st.sidebar.page_link("pages/analysis.py", label="📄 Analysis")

# =========================
# LOAD DATA
# =========================
day_df = pd.read_csv("df_day_cleaned.csv")
hour_df = pd.read_csv("hour.csv")



# Convert date
day_df["date"] = pd.to_datetime(day_df["date"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# =========================
# DASHBOARD CONTENT
# =========================
st.title("📊 Dashboard Overview")

# Filters
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
# filtered_hour = hour_df[(hour_df["year"] == year) & (hour_df["season"].isin(season))]

# KPI
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", int(filtered_day["total"].sum()))
col2.metric("Casual Users", int(filtered_day["casual"].sum()))
col3.metric("Registered Users", int(filtered_day["registered"].sum()))

st.divider()

# Charts side-by-side
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Rentals Over Time")
    st.line_chart(filtered_day.set_index("date")["total"])

with col2:
    st.subheader("👥 Casual vs Registered")
    st.bar_chart(filtered_day[["casual", "registered"]])

col3, col4 = st.columns(2)

with col3:
    st.subheader("🌤 Rentals by Season")
    season_data = filtered_day.groupby("season")["total"].sum()
    st.bar_chart(season_data)

# with col4:
#     st.subheader("⏰ Hourly Rental Pattern")
#     hourly_data = filtered_hour.groupby("hr")["total"].mean()
#     st.line_chart(hourly_data)

