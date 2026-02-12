import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.sidebar.title("Bike Sharing")
st.sidebar.page_link("app.py", label="🏠 Dashboard")
st.sidebar.page_link("pages/dataset.py", label="📝 Dataset")
st.sidebar.page_link("pages/analysis.py", label="📊 Analysis")
st.sidebar.page_link("pages/anggota.py", label="👤 About Us")

day_df = pd.read_csv("df_day_cleaned.csv")

day_df["date"] = pd.to_datetime(day_df["date"])

st.title("📊 Dashboard Overview")

st.markdown(
    """
    <style>
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        text-align: center; /* Memastikan teks di tengah */
    }
    .metric-label {
        color: #888;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #fff;
        font-size: 32px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Filters")
year = st.sidebar.multiselect(
    "Select Year",
    options=day_df["year"].unique(),
    default=day_df["year"].unique(),
    format_func=lambda x: "2011" if x == 0 else "2012"
)

season = st.sidebar.multiselect(
    "Select Season",
    options=day_df["season"].unique(),
    default=day_df["season"].unique()
)

filtered_day = day_df[(day_df["year"].isin(year)) & (day_df["season"].isin(season))]
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Rentals</div>
            <div class="metric-value">{int(filtered_day["total"].sum()):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Casual Users</div>
            <div class="metric-value">{int(filtered_day["casual"].sum()):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Registered Users</div>
            <div class="metric-value">{int(filtered_day["registered"].sum()):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Rentals Over Time")
    st.line_chart(filtered_day.set_index("date")["total"])

filtered_day['year'] = filtered_day['date'].dt.year
filtered_day['month'] = filtered_day['date'].dt.month
monthly_trend_registred = filtered_day.groupby(['year', 'month'])['registered'].mean().reset_index()
monthly_trend_casual = filtered_day.groupby(['year', 'month'])['casual'].mean().reset_index()


monthly_trend = monthly_trend_registred.merge(
    monthly_trend_casual,
    on=["year", "month"],
    suffixes=("_registered", "_casual")
)
monthly_trend["year_month"] = pd.to_datetime(
    monthly_trend["year"].astype(str) + "-" + monthly_trend["month"].astype(str)
)
month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


with chart_col2:
    st.subheader("👥 Casual vs Registered")
    chart = alt.Chart(monthly_trend).transform_fold(
    ['registered', 'casual'],
    as_=['user_type', 'value']
    ).mark_line(point=True).encode(
        x=alt.X('year_month:T', title='Month-Year'),  
        y=alt.Y('value:Q', title='Average Rentals'),
        color=alt.Color('user_type:N', title='User Type'),
        tooltip=['year:N', 'month:O', 'value:Q', 'user_type:N']
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

st.divider()



st.subheader("🌤 Rentals by Season")


season_data = filtered_day.groupby("season")["total"].sum().reset_index()

chart = alt.Chart(season_data).mark_bar().encode(
    x=alt.X("season:N", axis=alt.Axis(labelAngle=0)),  # horizontal labels
    y="total:Q"
)

st.altair_chart(chart, use_container_width=True)