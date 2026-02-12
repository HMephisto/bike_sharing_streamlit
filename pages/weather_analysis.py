import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="Analysis", layout="wide")
st.sidebar.title("🚴 Overview")

df = pd.read_csv("df_day_cleaned.csv")

with st.sidebar:
    st.page_link("app.py", label="🏠 Dashboard")
    st.page_link("pages/raw_data.py", label="📝 Raw Data")

    st.sidebar.title("Data Analysis")
    st.page_link("pages/analysis.py", label="📈 User Behaviour Analysis")
    st.page_link("pages/weather_analysis.py", label="🔍 Weather Analysis")
st.title("User Behaviour Analysis")

st.write("Analisis Rental Sepeda ketika Musim Atau Suhu berubah-rubah")


# Load data
df = pd.read_csv("df_day_cleaned.csv")

df['weather'] = pd.to_numeric(df['weather'])

df['suhu'] = df['temp'] * 41
df['kelembapan'] = df['humidity'] * 100
df['kecepatan_angin'] = df['windspeed'] * 67

avg_rentals_weather = df.groupby('weather')['total'].mean()

fig, ax = plt.subplots(1, 3, figsize=(15, 5))

ax[0].scatter(df['suhu'], df['total'], alpha=0.5, c='orange')
ax[0].set_title('Suhu')
ax[0].set_xlabel('Suhu (°C)')
ax[0].set_ylabel('Total Rental')

ax[1].scatter(df['kelembapan'], df['total'], alpha=0.5, c='skyblue')
ax[1].set_title('Kelembapan')
ax[1].set_xlabel('%')
ax[1].set_ylabel('Total Rental')

ax[2].scatter(df['kecepatan_angin'], df['total'], alpha=0.5, c='green')
ax[2].set_title('Kecepatan Angin')
ax[2].set_xlabel('Kecepatan Angin (km/h)')
ax[2].set_ylabel('Total Rental')

plt.subplots_adjust(wspace=0.4)

st.pyplot(fig)

st.subheader("Kondisi Cuaca terhadap Jumlah Rental Sepeda")

weather_data = [
    df[df['weather'] == i]['total']
    for i in sorted(df['weather'].unique())
]

fig, ax = plt.subplots()

ax.boxplot(
    weather_data,
    tick_labels=['Cerah', 'Berawan', 'Hujan'],
    patch_artist=True
)

ax.set_title('Kondisi Cuaca terhadap Jumlah Rental Sepeda')
ax.set_ylabel('Total Rental')

st.pyplot(fig)

st.markdown("""
Berdasarkan hasil visualisasi dan perhitungan didapat hasil sebagai berikut:
1. Perhitungan korelasi.

    Dengan menghitung korelasi kita dapat mengetahui seberapa kuat suatu faktor berhubungan dengan jumlah penyewaan. Jika angkanya negatif, itu berarti ketika nilai faktor tersebut meningkat, jumlah penyewa justru menurun.
      *   Kondisi Cuaca : -0.29 (Dampak negatif terkuat)
      *   Kecepatan Angin: -0.23 (Dampak Negatif Moderat)
      *   Kelembapan: -0.10 (Dampak Negatif Lemah)
      *   Suhu: +0.63 (Dampak Positif Kuat)

2. Visualisasi Data

    Grafik Suhu : terlihat saat cuaca lebih hangat, lebih banyak orang yang berkendara, dan akan menurun ketika cuaca semakin dingin.
    
    Grafik Kelembapan : terlihat data terlalu tersebar dan tidak memiliki pola yang jelas, sehingga mengonfirmasi bahwa kelembapan saja bukan faktor penentu besar bagi sebagian perental.

    Grafik Kecepatan Angin : terlihat bahwa data tersebar di sebelah kiri dan menurun semakin kekanan. hal ini menandakan bahwa semakin tinggi kecapatan angin semakin turun jumlah perental, walaupun tidak signifikan.

    Grafik Cuaca : Grafik ini menunjukkan faktor yang paling jelas

    *   Cerah   : Rata - rata penyewaan tinggi (~4876)
    *   Berawan : Sedikit lebih rendah (~4035)
    *   Hujan   : Penurunan Drastis (~1803)





""")