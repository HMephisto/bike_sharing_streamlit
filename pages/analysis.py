import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="Analysis", layout="wide")

# SIDEBAR NAVIGATION
st.sidebar.title("🚴 Overview")

df = pd.read_csv("df_day_cleaned.csv")

with st.sidebar:
    st.page_link("app.py", label="🏠 Dashboard")
    st.page_link("pages/raw_data.py", label="📊 Raw Data")

    st.sidebar.title("Data Analysis")
    st.page_link("pages/analysis.py", label="📄 User Behaviour Analysis")
    st.page_link("pages/weather_analysis.py", label="🔍 Weather Analysis")

st.title("User Behaviour Analysis")

st.write("Perbandingan Hari Kerja dan Akhir Pekan dalam Penggunaan Sepeda")


# Load data
df = pd.read_csv("df_day_cleaned.csv")


holiday_weekday_impact = df.groupby(['holiday', 'weekday'])['total'].mean().reset_index()

weekday_order_map = {
    'Sunday': 0,
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6
}
holiday_weekday_impact['weekday_order'] = holiday_weekday_impact['weekday'].map(weekday_order_map)
holiday_weekday_impact = holiday_weekday_impact.sort_values(by=['holiday', 'weekday_order']).reset_index(drop=True)

holiday_weekday_impact['holiday'] = holiday_weekday_impact['holiday'].replace({'No': 'Weekday', 'Yes': 'Holiday'})

weekdays = list(weekday_order_map.keys())
num_weekdays = len(weekdays)
bar_width = 0.35

holiday_types = holiday_weekday_impact['holiday'].unique()
num_holiday_types = len(holiday_types)


r = np.arange(num_weekdays)

fig, ax = plt.subplots(figsize=(12, 7))

for i, holiday_type in enumerate(holiday_types):
    holiday_data = holiday_weekday_impact[
        holiday_weekday_impact['holiday'] == holiday_type
    ]
    holiday_data = holiday_data.set_index('weekday').reindex(weekdays).reset_index()

    bar_pos = r + (i - (num_holiday_types - 1) / 2) * bar_width

    ax.bar(
        bar_pos,
        holiday_data['total'],
        width=bar_width,
        label=holiday_type,
        color='skyblue' if holiday_type == 'Weekday' else 'lightcoral'
    )

ax.set_title('Pengaruh Hari Libur dan Hari dalam Seminggu terhadap Rata-rata Rental Sepeda', fontsize=16)
ax.set_xlabel('Hari dalam Seminggu')
ax.set_ylabel('Rata-rata Jumlah Rental')
ax.set_xticks(r)
ax.set_xticklabels(weekdays, rotation=45, ha='right')
ax.legend(title='Jenis Hari', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()

# Show in Streamlit
st.pyplot(fig)

st.write("Data menunjukkan bahwa total keseluruhan pesepeda saat holiday dan weekday tidak memiliki perbedaan signifikan, tetapi ada beberapa hari on holiday yang ternyata memiliki angka yang sangat tinggi")