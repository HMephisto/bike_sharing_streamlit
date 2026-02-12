import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dataset", layout="wide")
st.sidebar.title("Bike Sharing")
st.sidebar.page_link("app.py", label="🏠 Dashboard")
st.sidebar.page_link("pages/dataset.py", label="📝 Dataset")
st.sidebar.page_link("pages/analysis.py", label="📊 Analysis")
st.sidebar.page_link("pages/anggota.py", label="👤 About Us")

day_df = pd.read_csv("day.csv")
day_df_clean = pd.read_csv("df_day_cleaned.csv")

st.title("📄 Raw Dataset")
st.subheader("Day Dataset")
st.dataframe(day_df)

st.title("📄 Clean Dataset")
st.subheader("Day Dataset")
st.dataframe(day_df_clean)
