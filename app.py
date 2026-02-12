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

st.markdown("""
    <style>
    .metric-card {
        background-color: #1e1e1e; 
        padding: 15px; 
        border-radius: 10px;
        border: 1px solid #333; 
        text-align: center; 
        min-height: 100px;
    }
    .metric-label { 
        color: #888; 
        font-size: 13px; 
        margin-bottom: 5px; 
    }
    .metric-value { 
        color: #fff; 
        font-size: 22px; 
        font-weight: bold; 
    }
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #888;
        font-size: 16px;
    }
    .empty-state-icon {
        font-size: 48px;
        margin-bottom: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.header("Filters")

year_opts = sorted(day_df["year"].unique())
year_labels = {0: "2011", 1: "2012"}

year = st.sidebar.multiselect(
    "Select Year", 
    options=year_opts, 
    default=year_opts,  
    format_func=lambda x: year_labels.get(x, str(x))
)

season_opts = sorted(day_df["season"].unique())

if isinstance(season_opts[0], str):
    season_labels_map = {s: s for s in season_opts}
else:
    season_labels_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}

season = st.sidebar.multiselect(
    "Select Season", 
    options=season_opts, 
    default=season_opts,  
    format_func=lambda x: season_labels_map.get(x, str(x))
)

year_filter = year if len(year) > 0 else year_opts
season_filter = season if len(season) > 0 else season_opts

filtered_day = day_df[
    (day_df["year"].isin(year_filter)) & 
    (day_df["season"].isin(season_filter))
]

has_data = not filtered_day.empty and len(year) > 0

col1, col2, col3, col4, col5, col6 = st.columns(6)

if has_data:
    metrics = [
        ("Total Rentals", filtered_day["total"].sum()),
        ("Casual Users", filtered_day["casual"].sum()),
        ("Registered Users", filtered_day["registered"].sum()),
        ("Max Daily Rentals", filtered_day["total"].max()),
        ("Min Daily Rentals", filtered_day["total"].min()),
        ("Avg Daily Rentals", filtered_day["total"].mean()),
    ]
else:
    metrics = [
        ("Total Rentals", 0),
        ("Casual Users", 0),
        ("Registered Users", 0),
        ("Max Daily Rentals", 0),
        ("Min Daily Rentals", 0),
        ("Avg Daily Rentals", 0),
    ]

cols = [col1, col2, col3, col4, col5, col6]
for i, (label, value) in enumerate(metrics):
    with cols[i]:
        if label == "Avg Daily Rentals":
            val = f"{int(value):,}" if pd.notnull(value) and value > 0 else "0"
        else:
            val = f"{int(value):,}" if pd.notnull(value) else "0"
        
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">{label}</div>'
            f'<div class="metric-value">{val}</div>'
            f'</div>', 
            unsafe_allow_html=True
        )

st.divider()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Rentals Over Time")
    
    if has_data:
        trend_data = filtered_day[["date", "total"]].copy()
        trend_data = trend_data.set_index("date")
        st.line_chart(trend_data)
    else:
        st.info("Pilih tahun untuk melihat tren.")
        empty_df = pd.DataFrame({
            "date": pd.date_range(start="2011-01-01", end="2011-01-31", freq="D"),
            "total": [0] * 31
        }).set_index("date")
        st.line_chart(empty_df)

with chart_col2:
    st.subheader("👥 Casual vs Registered")
    
    if has_data:
        temp_df = filtered_day.copy()
        temp_df['year_month'] = temp_df['date'].dt.to_period('M').astype(str)
        monthly = temp_df.groupby('year_month')[['registered', 'casual']].mean().reset_index()
        
        monthly_melted = monthly.melt(
            id_vars=['year_month'],
            value_vars=['registered', 'casual'],
            var_name='User Type',
            value_name='Average Rentals'
        )
        
        c = alt.Chart(monthly_melted).mark_line(point=True).encode(
            x=alt.X('year_month:N', title='Month-Year', axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('Average Rentals:Q', title='Average Daily Rentals'),
            color=alt.Color('User Type:N', scale=alt.Scale(scheme='category10')),
            tooltip=['year_month:N', 'User Type:N', alt.Tooltip('Average Rentals:Q', format='.0f')]
        ).properties(height=400).interactive()
        
        st.altair_chart(c, use_container_width=True)
    else:
        st.info("Data kosong.")
        empty_data = pd.DataFrame({
            'Month-Year': ['2011-01'],
            'Average Rentals': [0],
            'User Type': ['casual']
        })
        c_empty = alt.Chart(empty_data).mark_line().encode(
            x=alt.X('Month-Year:N', title='Month-Year'),
            y=alt.Y('Average Rentals:Q', title='Average Rentals', scale=alt.Scale(domain=[0, 1]))
        ).properties(height=400)
        st.altair_chart(c_empty, use_container_width=True)

st.divider()

st.subheader("🌤 Rentals by Season")

season_order = ['Spring', 'Summer', 'Fall', 'Winter']
season_colors = ['#FFB7C5', '#f1c40f', '#e67e22', '#3498db']  

if has_data:
    season_data = filtered_day.groupby("season")["total"].sum().reset_index()
    
    if isinstance(season_data['season'].iloc[0], str):
        season_data['season_name'] = season_data['season']
    else:
        season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
        season_data['season_name'] = season_data['season'].map(season_map)
    
    season_data = season_data.dropna(subset=['season_name'])
    
    if len(season_data) > 0:
        chart_season = alt.Chart(season_data).mark_bar().encode(
            x=alt.X(
                "season_name:N", 
                sort=season_order, 
                axis=alt.Axis(labelAngle=0), 
                title="Season"
            ),
            y=alt.Y("total:Q", title="Total Rentals"),
            color=alt.Color(
                "season_name:N", 
                scale=alt.Scale(domain=season_order, range=season_colors), 
                legend=None
            ),
            tooltip=[
                alt.Tooltip('season_name:N', title='Season'),
                alt.Tooltip('total:Q', title='Total Rentals', format=',')
            ]
        ).properties(height=400)
        
        st.altair_chart(chart_season, use_container_width=True)
    else:
        st.warning("No season data available for the selected filters.")
else:
    dummy = pd.DataFrame({'season': season_order, 'total': [0, 0, 0, 0]})
    chart_empty_season = alt.Chart(dummy).mark_bar().encode(
        x=alt.X("season:N", sort=season_order, title="season", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("total:Q", title="total", scale=alt.Scale(domain=[0, 1])),
        color=alt.value("#555")  # Dark gray bars for empty state
    ).properties(height=400)
    st.altair_chart(chart_empty_season, use_container_width=True)

