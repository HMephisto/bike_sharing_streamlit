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
    
st.title("Weather Analysis")

# Load data
df = pd.read_csv("df_day_cleaned.csv")

df['weather'] = pd.to_numeric(df['weather'])

df['suhu'] = df['temp'] * 41
df['kelembapan'] = df['humidity'] * 100
df['kecepatan_angin'] = df['windspeed'] * 67

avg_rentals_weather = df.groupby('weather')['total'].mean()

st.header('Hubungan Suhu, Kelembapan, dan Kecepatan Angin terhadap Total Rental')

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

st.header("Kondisi Cuaca terhadap Jumlah Rental Sepeda")

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

ax.set_ylabel('Total Rental')

st.pyplot(fig)

st.markdown("""
#### Insight:
            
* **Suhu**: Terdapat tren positif antara suhu dan jumlah rental sepeda.
* **Kelembapan**: Variasi rental cukup besar saat kelembapan tinggi (tidak konsisten).
* **Kecepatan Angin**: Tidak terlihat hubungan yang sangat kuat namun kecepatan angin tinggi cenderung diikuti penurunan rental
* **Cuaca**: Cuaca cerah memiliki median rental tertinggi.
---
#### Conclusion:
            
* Faktor cuaca memiliki pengaruh nyata terhadap penggunaan sepeda.
* Hujan menjadi faktor utama penurunan penggunaan sepeda.
* Kondisi paling ideal untuk rental yaitu ketika suhu hangat, kelembapan sedang, angin rendah dan cuaca cerah
---
#### Recommendation:
            
* Tambah ketersediaan sepeda saat cuaca cerah & suhu nyaman (peak demand).
* Kurangi distribusi sepeda saat hujan untuk efisiensi operasional.


""")

st.divider()

st.header("Pengaruh perubahan musim terhadap jumlah rental sepeda di hari kerja dan di hari libur di tahun 2011 dan 2012")

if "year" not in df.columns:
    try:
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
    except:
        df["dteday"] = pd.to_datetime(df["dteday"])
        df["year"] = df["dteday"].dt.year

unique_years = sorted(df["year"].dropna().unique())
if set(unique_years) == {0, 1}:
    df_year = df.copy()
    df_year["year_label"] = df_year["year"].replace({0: 2011, 1: 2012})
else:
    df_year = df.copy()
    df_year["year_label"] = df_year["year"]

if "season_name" not in df_year.columns:
    df_year["season_name"] = df_year["season"]

rental_col = "total" if "total" in df_year.columns else ("cnt" if "cnt" in df_year.columns else None)

if rental_col is None:
    st.error("Kolom total/cnt tidak ditemukan di dataset.")
else:
    # menghitung rata-rata rental per tahun, musim, dan workingday
    info = (
        df_year.groupby(["year_label", "season_name", "workingday"])[rental_col]
        .mean()
        .astype(int)
        .reset_index()
    )

    workday_map = {"Yes": "Hari Kerja", "No": "Hari Libur/Weekend"}
    info["workingday_label"] = info["workingday"].map(workday_map).fillna(info["workingday"].astype(str))

    # pivot per tahun
    pivot_2011 = info[info["year_label"] == 2011].pivot(
        index="season_name",
        columns="workingday_label",
        values=rental_col
    ).reset_index()

    pivot_2012 = info[info["year_label"] == 2012].pivot(
        index="season_name",
        columns="workingday_label",
        values=rental_col
    ).reset_index()

    pivot_2011.columns = ["Season"] + [f"2011 - {c}" for c in pivot_2011.columns[1:]]
    pivot_2012.columns = ["Season"] + [f"2012 - {c}" for c in pivot_2012.columns[1:]]

    pivot_all = pd.merge(pivot_2011, pivot_2012, on="Season", how="outer")

    fig4, ax4 = plt.subplots(figsize=(12, 6))

    season_order = ["Spring", "Summer", "Fall", "Winter"]
    pivot_all["Season"] = pd.Categorical(pivot_all["Season"], categories=season_order, ordered=True)
    pivot_all = pivot_all.sort_values("Season")
    value_cols = [c for c in pivot_all.columns if c != "Season"]

    x = np.arange(len(pivot_all["Season"]))
    width = 0.18

    for i, col in enumerate(value_cols):
        ax4.bar(x + (i - (len(value_cols) - 1) / 2) * width, pivot_all[col], width=width, label=col)

    ax4.set_title("Pengaruh Musim terhadap Rental Sepeda (2011 vs 2012)")
    ax4.set_xlabel("Musim")
    ax4.set_ylabel("Rata-rata Jumlah Rental")
    ax4.set_xticks(x)
    ax4.set_xticklabels(pivot_all["Season"].astype(str))
    ax4.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    ax4.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    st.pyplot(fig4)

    mean_2011 = df_year[df_year["year_label"] == 2011][rental_col].mean()
    mean_2012 = df_year[df_year["year_label"] == 2012][rental_col].mean()
    diff = mean_2012 - mean_2011
    pct = (diff / mean_2011) * 100 if mean_2011 != 0 else 0

    st.subheader("Ringkasan aktivitas *bike sharing* Tahun 2011 vs 2012")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Rata-rata Rental 2011", f"{mean_2011:,.0f}")

    with c2:
        st.metric("Rata-rata Rental 2012", f"{mean_2012:,.0f}", f"{diff:+.0f} ({pct:+.1f}%)")

    with c3:
        kondisi = "Naik (2012 > 2011)" if diff > 0 else "Turun (2012 < 2011)" if diff < 0 else "Stabil"
        st.metric("Perubahan", kondisi)
    
st.markdown("""
            #### Insight 

            Berdasarkan hasil analisis pengaruh musim terhadap jumlah rental sepeda pada hari kerja dan hari libur di tahun 2011 dan 2012, diperoleh beberapa insight penting:
            * **Musim memiliki pengaruh signifikan terhadap jumlah rental sepeda.**  
            Musim dengan cuaca yang lebih hangat seperti *Summer* dan *Fall* menunjukkan rata-rata rental yang lebih tinggi dibandingkan *Winter*.
            * **Hari Kerja cenderung lebih stabil dibandingkan Hari Libur.**  
            Pada hari kerja, jumlah rental relatif konsisten di setiap musim karena penggunaan sepeda didominasi oleh aktivitas rutin seperti bekerja atau sekolah.
            * **Hari Libur lebih sensitif terhadap perubahan musim.**  
            Pada musim spring dan summer, rental di hari libur meningkat cukup signifikan. Namun pada Winter, terjadi penurunan yang lebih drastis dibanding hari kerja.
            * **Terjadi peningkatan total penggunaan dari 2011 ke 2012.**  
            Hal ini menunjukkan adanya pertumbuhan pengguna serta peningkatan penggunaan layanan bike sharing dari tahun 2011 ke tahun 2012.

            ---

            #### Conclusion
            Dari analisis ini dapat disimpulkan bahwa:
            - **Faktor musim merupakan salah satu determinan utama dalam permintaan rental sepeda.**
            - Permintaan tertinggi terjadi pada musim dengan kondisi cuaca yang lebih mendukung aktivitas luar ruangan.
            - Hari kerja menunjukkan pola permintaan yang lebih stabil sepanjang tahun, sedangkan hari libur memiliki fluktuasi yang lebih besar tergantung musim.
            ---

            #### Recomendation
            - Tambahkan jumlah sepeda dan kapasitas operasional saat memasuki **Spring dan Summer**.
            - Siapkan sistem maintenance lebih intensif di musim dingin (winter) untuk efisiensi biaya.
            - Terapkan promo atau diskon khusus di musim dingin (winter) untuk menjaga tingkat penggunaan.
            - Fokuskan kampanye promosi pada awal musim panas.
            ---
""")
