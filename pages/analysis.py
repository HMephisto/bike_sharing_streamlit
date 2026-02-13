import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="User Behaviour Analysis", layout="wide")
st.sidebar.title("Bike Sharing")

df = pd.read_csv("df_day_cleaned.csv")

with st.sidebar:
    st.page_link("app.py", label="🏠 Dashboard")
    st.sidebar.page_link("pages/dataset.py", label="📝 Dataset")
    st.sidebar.page_link("pages/anggota.py", label="👤 About Us")

    st.sidebar.title("Data Analysis")
    st.page_link("pages/analysis.py", label="📈 User Behaviour Analysis")
    st.page_link("pages/weather_analysis.py", label="🌡️ Weather Analysis")


st.title("User Behaviour Analysis")

st.write()
st.header("Perbandingan rata-rata penyewaan sepeda antara Working Day dan Weekend/Holiday ")


# Load data
df = pd.read_csv("df_day_cleaned.csv")
impact_data = df.groupby(['workingday', 'weekday'])['total'].mean().reset_index()

weekday_order_map = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 
    'Friday': 4, 'Saturday': 5, 'Sunday': 6
}
impact_data['weekday_order'] = impact_data['weekday'].map(weekday_order_map)
impact_data = impact_data.sort_values(by=['workingday', 'weekday_order']).reset_index(drop=True)

impact_data['category'] = impact_data['workingday'].replace({'Yes': 'Working Day', 'No': 'Weekend/Holiday'})

weekdays = list(weekday_order_map.keys())
num_weekdays = len(weekdays)
bar_width = 0.35
categories = ['Working Day', 'Weekend/Holiday']

r = np.arange(num_weekdays)
fig, ax = plt.subplots(figsize=(12, 7))

for i, cat in enumerate(categories):
    subset = impact_data[impact_data['category'] == cat] 
    subset = subset.set_index('weekday').reindex(weekdays).reset_index()
    bar_pos = r + (i - (len(categories) - 1) / 2) * bar_width

    ax.bar(
        bar_pos,
        subset['total'],
        width=bar_width,
        label=cat,
        color='#4e79a7' if cat == 'Working Day' else '#f28e2b'
    )



ax.set_title('Rata-rata penyewaan Sepeda Working Day vs Weekend dan Holiday', fontsize=16)
ax.set_xlabel('Hari dalam Seminggu')
ax.set_ylabel('Rata-rata Jumlah Rental')
ax.set_xticks(r)
ax.set_xticklabels(weekdays)
ax.legend(title='Kategori Hari', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()


st.pyplot(fig)

st.markdown("""
Berdasarkan grafik diatas, didapat sebuah insight bahwa :

*   Pada working day, penggunaan sepeda terasa stabil dengan rentang antara 4000 - 4500 mengindikasikan bahwa pekerja atau pelajar meminati penggunaan sepeda setiap harinya
*   pada weekend, penggunaan sepeda juga terasa stabil di angka 4000-4500 mengindikasikan pula bahwa sepeda tetap menjadi tranportasi yang memiliki banyak minat di hari libur
            
Maka konklusi yang bisa kita dapat adalah, sebagai berikut :
   
*   Rata-rata pengguna tetap nyaman menggunakan sepeda ketika working day dan weekend, dan grafik menunjukkan kestabilan yang bisa digunakan perusahaan untuk acuan agar tetap menjaga ketersediaan sepeda saat working day
*   Penggunaan sepeda saat holiday cenderung naik turun dibandingkan hari biasa. Ini juga bisa digunakan oleh perusahaan misal untuk pemeliharaan sepeda


Saran yang bisa diberikan untuk perusahaan adalah sebagai berikut:

*   Persiapkan selalu ketersedian sepeda ketika working day dan weekend/holiday
*   Holiday cenderung naik dan turun, maka direkomendasikan pula untuk perusahaan mempersiapkan stok sepeda cadangan agar supply tetap tersedia 
*   Persiapkan diskon voucher/promo di hari-hari non-Holiday (Wworking day/Weekend), karena ini akan menjaga loyalitas pengguna sepeda                                                             
""")


st.write()
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

#Memberi judul dan label
ax2.set_title('Tren Rata-rata Penggunaan Sepeda oleh Pengguna Registered',
          fontsize=16, fontweight='bold')
ax2.set_xlabel('Waktu (Tahun-Bulan)', fontsize=12)
ax2.set_ylabel('Rata-rata Pengguna Registered (per Hari)', fontsize=12)

#Menampilkan label untuk awal setiap tahun
x_ticks = monthly_trend[monthly_trend['month'] == 1]['date']
x_labels = monthly_trend[monthly_trend['month'] == 1]['year'].astype(str)

ax2.set_xticks(x_ticks, x_labels, rotation=45, ha='right')
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout() #Layout agar tidak terpotong

#Anotasi
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