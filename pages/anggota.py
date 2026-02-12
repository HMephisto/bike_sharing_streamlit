import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Kelompok 5", layout="centered")

st.sidebar.title("Bike Sharing")
st.sidebar.page_link("app.py", label="🏠 Dashboard")
st.sidebar.page_link("pages/raw_data.py", label="📝 Raw Data")
st.sidebar.page_link("pages/analysis.py", label="📊 Analysis")
st.sidebar.page_link("pages/anggota.py", label="👤 About Us")

st.title("Data Kelompok")
st.subheader("Kelompok 5")

data = {
    "NIM": [
        "10124015",
        "10124008",
        "10124037",
        "10124026",
        "10124009",
        "10124046"
    ],
    "Nama": [
        "Muhamad Hakim Nur Majid",
        "Ferdi",
        "Maudina Apriliani",
        "Rakesya Wijaya",
        "Muhamad Aditya Wicaksono",
        "Khansa Noor Jeihan Kareira"
    ]
}

df = pd.DataFrame(data)

st.write("### Anggota Kelompok:")
st.table(df)
