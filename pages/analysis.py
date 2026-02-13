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

ax2.set_title('Tren Rata-rata Penggunaan Sepeda oleh Pengguna Registered',
          fontsize=16, fontweight='bold')
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


st.write()
st.header("Perbandingan Jumlah Rental Sepeda pada Awal Bulan (1-10) vs Akhir Bulan (21-31)")

df = pd.read_csv("df_day_cleaned.csv")

try:
    df['date'] = pd.to_datetime(df['date'])
except:
    df['date'] = pd.to_datetime(df['dteday'])

df['day_of_month'] = df['date'].dt.day
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def categorize_period(day):
    if 1 <= day <= 10:
        return 'Awal Bulan (1-10)'
    elif 21 <= day <= 31:
        return 'Akhir Bulan (21-31)'
    else:
        return 'Pertengahan'

df['period'] = df['day_of_month'].apply(categorize_period)

period_data = df[df['period'].isin(['Awal Bulan (1-10)', 'Akhir Bulan (21-31)'])].copy()

rental_col = 'cnt' if 'cnt' in df.columns else 'total'
period_comparison = period_data.groupby(['year', 'month', 'period'])[rental_col].mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(14, 6))

awal_bulan = period_comparison[period_comparison['period'] == 'Awal Bulan (1-10)'].copy()
akhir_bulan = period_comparison[period_comparison['period'] == 'Akhir Bulan (21-31)'].copy()

awal_bulan['time'] = awal_bulan['year'].astype(str) + '-' + awal_bulan['month'].astype(str).str.zfill(2)
akhir_bulan['time'] = akhir_bulan['year'].astype(str) + '-' + akhir_bulan['month'].astype(str).str.zfill(2)

ax3.plot(awal_bulan['time'], awal_bulan[rental_col], 
         marker='o', linestyle='-', color='#4e79a7', linewidth=2, 
         label='Awal Bulan (1-10)', markersize=6)
ax3.plot(akhir_bulan['time'], akhir_bulan[rental_col], 
         marker='s', linestyle='-', color='#f28e2b', linewidth=2, 
         label='Akhir Bulan (21-31)', markersize=6)

ax3.set_title('Perbandingan Rata-rata Rental Sepeda: Awal Bulan vs Akhir Bulan (2011-2012)',
              fontsize=16, fontweight='bold')
ax3.set_xlabel('Waktu (Tahun-Bulan)', fontsize=12)
ax3.set_ylabel('Rata-rata Jumlah Rental per Hari', fontsize=12)

x_ticks = awal_bulan[awal_bulan['month'] == 1]['time']
x_labels = awal_bulan[awal_bulan['month'] == 1]['year'].astype(str)
ax3.set_xticks(x_ticks)
ax3.set_xticklabels(x_labels, rotation=45, ha='right')

ax3.legend(loc='upper left', fontsize=11)
ax3.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
st.pyplot(fig3)

st.subheader("📊 Statistik Perbandingan")

col1, col2, col3 = st.columns(3)

rata_awal = period_data[period_data['period'] == 'Awal Bulan (1-10)'][rental_col].mean()
rata_akhir = period_data[period_data['period'] == 'Akhir Bulan (21-31)'][rental_col].mean()
selisih = rata_akhir - rata_awal
persen_beda = (selisih / rata_awal) * 100 if rata_awal != 0 else 0

with col1:
    st.metric("Rata-rata Awal Bulan", f"{rata_awal:,.0f}", "rentals/hari")

with col2:
    st.metric("Rata-rata Akhir Bulan", f"{rata_akhir:,.0f}", f"{selisih:+.0f} ({persen_beda:+.1f}%)")

with col3:
    periode_lebih_tinggi = "Akhir Bulan" if rata_akhir > rata_awal else "Awal Bulan"
    st.metric("Periode Lebih Tinggi", periode_lebih_tinggi)

st.markdown(f"""
### 📈 Insight dan Kesimpulan

Dari hasil analisis, terlihat bahwa rata-rata penyewaan sepeda di awal bulan (1–10) lebih tinggi dibandingkan akhir bulan (21–31). Awal bulan mencatat angka sekitar **{rata_awal:,.0f}** penyewaan per hari, sedangkan akhir bulan sedikit lebih rendah, yaitu **{rata_akhir:,.0f}** penyewaan per hari.

Perbedaan ini menunjukkan bahwa penggunaan cenderung lebih aktif menyewa sepeda di awal bulan. Hal ini bisa terjadi karena beberapa alasan, misalnya:

* Awal bulan biasanya orang baru menerima gaji, sehingga mereka lebih leluasa melakukan aktivitas seperti olahraga atau rekreasi.
* Jadwal dan aktivitas di awal bulan mungkin lebih stabil, sehingga lebih banyak waktu untuk bersepeda.
* Menjelang akhir bulan, sebagian orang mulai mengurangi pengeluaran atau aktivitas luar karena kesibukan atau faktor finansial.

Meskipun ada perbedaan, peningkatan hanya sebesar **{abs(persen_beda):.1f}%** menunjukkan bahwa perbedaan awal dan akhir bulan tidak terlalu signifikan dalam mempengaruhi penyewaan sepeda. Faktor-faktor lain seperti kondisi cuaca, hari kerja versus hari libur, dan seasonal pattern mungkin memiliki pengaruh yang lebih besar terhadap penggunaan sepeda. 

Namun, dari perspektif bisnis, peningkatan **{abs(persen_beda):.1f}%** ini tetap bisa dimanfaatkan untuk strategi promosi atau penawaran khusus di awal bulan untuk memaksimalkan revenue.

### 💡 Rekomendasi untuk Perusahaan

**Strategi Operasional:**

1. **Manajemen Inventori:**
   - Sesuaikan ketersediaan sepeda berdasarkan pola awal vs akhir bulan
   - Siapkan lebih banyak sepeda di periode yang memiliki demand lebih tinggi
   - Lakukan pemeliharaan rutin di periode dengan demand lebih rendah

2. **Strategi Pricing:**
   - Pertimbangkan dynamic pricing berdasarkan periode bulan
   - Tawarkan promo khusus di awal bulan untuk meningkatkan utilisasi
   - Maksimalkan revenue di akhir bulan dengan paket premium

3. **Marketing & Promosi:**
   - Kampanye marketing intensif di periode demand rendah
   - Program loyalitas untuk pengguna di awal bulan
   - Bundle deals untuk mendorong penggunaan konsisten sepanjang bulan

4. **Perencanaan SDM:**
   - Alokasi staff lebih banyak di periode puncak
   - Jadwal shift fleksibel mengikuti pola demand
   - Training staff untuk handle peak periods
""")