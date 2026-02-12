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
    st.sidebar.page_link("pages/anggota.py", label="👤 About Us")

    st.sidebar.title("Data Analysis")
    st.page_link("pages/analysis.py", label="📈 User Behaviour Analysis")
    st.page_link("pages/weather_analysis.py", label="🔍 Weather Analysis")


st.title("User Behaviour Analysis")
st.write("Perbandingan Working Day dan Weekend/Holiday dalam penggunaan rental sepeda")


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


ax.set_title('Rental Sepeda Working Day vs Weekend dan Holiday', fontsize=16)
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
Berdasarkan grafik diatas, dapat disimpulkan bahwa penggunaan sepeda sangat diminati baik di working day atau holiday, dengan beberapa poin sebagai berikut :
   
*   Pada working day, penggunaan sepeda terasa stabil dengan rentang antara 4000 - 4500
*   pada weekend, penggunaan sepeda juga terasa stabil di angka 4000-4500
*   Terdapat lonjakan yang sangat tinggi di hari rabu karena setelah meriset kembali dataset, ditemukan bahwa ternyata hari tersebut tepat berada pada hari libur nasional tanggal 4 Juli 2012
*   Penurunan terjadi pula di hari selasa, karena setelah diriset kembali di dataset, ternyata holiday hanya bertepatan satu hari dengan natal, dan dikarenakan suhu yang dingin pemakaian sepeda menjadi sedikit
        
""")