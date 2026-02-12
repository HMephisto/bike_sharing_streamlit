import streamlit as st
import pandas as pd

st.set_page_config(page_title="Raw Data", layout="wide")
st.sidebar.title("Bike Sharing")
st.sidebar.page_link("app.py", label="🏠 Dashboard")
st.sidebar.page_link("pages/raw_data.py", label="📝 Raw Data")
st.sidebar.page_link("pages/analysis.py", label="📊 Analysis")
st.sidebar.page_link("pages/anggota.py", label="👤 About Us")

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

st.title("📄 Raw Dataset")
st.subheader("Day Dataset")
st.dataframe(day_df)
st.subheader("Hour Dataset")
st.dataframe(hour_df)
