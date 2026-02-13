import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="Analysis", layout="wide")
st.sidebar.title("Bike Sharing")

df = pd.read_csv("df_day_cleaned.csv")

with st.sidebar:
    st.page_link("app.py", label="🏠 Dashboard")
    st.sidebar.page_link("pages/dataset.py", label="📝 Dataset")
    st.sidebar.page_link("pages/anggota.py", label="👤 About Us")

    st.sidebar.title("Data Analysis")
    st.page_link("pages/analysis.py", label="👥 User Behaviour Analysis")
    st.page_link("pages/weather_analysis.py", label="🌡️ Weather Analysis")
    st.page_link("pages/trend_analysis.py", label="📈 Trend Analysis")
    
st.title("Trend Analysis")

st.header("Tren penggunaan sepeda oleh pengguna terdaftar (registered) dari waktu ke waktu")
fig2, ax2 = plt.subplots(figsize=(14, 6))

df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
monthly_trend = df.groupby(['year', 'month'])['registered'].mean().reset_index()
monthly_trend['date'] = monthly_trend['year'].astype(str) + '-' + monthly_trend['month'].astype(str).str.zfill(2)
plt.plot(monthly_trend['date'], monthly_trend['registered'],
         marker='o', linestyle='-', color='skyblue', linewidth=2)

ax2.set_xlabel('Waktu (Tahun-Bulan)', fontsize=12)
ax2.set_ylabel('Rata-rata Pengguna Registered (per Hari)', fontsize=12)

x_ticks = monthly_trend[monthly_trend['month'] == 1]['date']
x_labels = monthly_trend[monthly_trend['month'] == 1]['year'].astype(str)

ax2.set_xticks(x_ticks, x_labels, rotation=45, ha='right')
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout() 

plt.annotate('Peningkatan Signifikan',
             xy=(monthly_trend['date'].iloc[15], monthly_trend['registered'].iloc[15]),
             xytext=(20, -50),
             textcoords='offset points',
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=10, color='red')

plt.show()
st.pyplot(fig2)

st.markdown("""
Berdasarkan analisa data dan plotline diatas, dapat ditarik kesimpulan :

* Terdapat peningkatan yang signifikan dalam rata-rata jumlah pengguna sepeda harian oleh pengguna registered selama periode waktu yang dicakup dataset.
* Pengguna cenderung meningkat tajam di bulan-bulan musim semi dan musim panas (Maret - September) dan menurun drastis pada bulan-bulan musim dingin (November - Februari).
* Pola ini menunjukkan kestabilan setiap tahun, sehingga menunjukkan pola musiman yang kuat.
* Puncak penggunaan di tahun 2012 juga jauh lebih tinggi daripada tahun sebelumnya. Ini mengindikasikan bahwa sistem bike sharing ini mampu meregistrasi dan mempertahankan pengguna dari tahun ke tahun.


Dari konklusi analisis ini, perusahaan dapat :

* Mengukur pertumbuhan loyal costumer dan pertumbuhan bisnis dalam jangka panjang.
* Menentukan momentum untuk menyusun berbagai strategi bisnis.
* Menentukan dasar keputusan investasi untuk pengembangan bisnis secara akurat.
""")

st.divider()

st.header("Analisis Pertumbuhan Penyewaan Sepeda (2011 vs 2012)")

df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

#menghitung total rental per tahun
annual_rentals = df.groupby('year')['total'].sum().reset_index()

rental_2011 = annual_rentals[annual_rentals['year'] == 2011]['total'].iloc[0]
rental_2012 = annual_rentals[annual_rentals['year'] == 2012]['total'].iloc[0]

diff = rental_2012 - rental_2011
percentage = (diff / rental_2011) * 100



fig5, ax5 = plt.subplots(figsize=(8,5))
ax5.bar(['2011', '2012'], [rental_2011, rental_2012], color=['#4e79a7','#f28e2b'])

ax5.set_ylabel("Total Rental")
ax5.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
st.pyplot(fig5)

st.subheader("Ringkasan Pertumbuhan Tahunan")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rental 2011", f"{rental_2011:,.0f}")

with col2:
    st.metric("Total Rental 2012", f"{rental_2012:,.0f}", f"{diff:+,.0f}")

with col3:
    kondisi = "Pertumbuhan Signifikan 📈" if diff > 0 else "Penurunan 📉"
    st.metric("Perubahan (%)", f"{percentage:+.2f}%", kondisi)

st.markdown(f"""
#### Insight 

Berdasarkan hasil perhitungan total penyewaan tahunan, terjadi peningkatan dari  
**{rental_2011:,.0f} penyewaan pada tahun 2011** menjadi  
**{rental_2012:,.0f} penyewaan pada tahun 2012**.

Hal ini menunjukkan adanya pertumbuhan sebesar **{percentage:.2f}%**, yang tergolong signifikan dalam periode satu tahun.

---

#### Conclusion

Dapat disimpulkan bahwa layanan *bike sharing* mengalami pertumbuhan yang sangat positif dari tahun 2011 ke 2012.  
Peningkatan ini mengindikasikan:

- Bertambahnya jumlah pengguna
- Meningkatnya kepercayaan masyarakat terhadap layanan
- Sistem operasional yang semakin optimal

---

#### Recommendation

- Perusahaan dapat mempertimbangkan penambahan armada sepeda.
- Mempertahankan kualitas layanan untuk menjaga pertumbuhan berkelanjutan.
- Siapkan infrastruktur operasional untuk mengantisipasi peningkatan lanjutan.

---
""")