import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Delhi Air Intelligence",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COLOR PALETTE (used for charts + theming)
# ============================================================

COLORFUL_SEQUENCE = [
    "#6366f1", "#ec4899", "#f59e0b", "#10b981",
    "#06b6d4", "#8b5cf6", "#ef4444", "#14b8a6",
    "#f97316", "#3b82f6"
]

AQI_COLOR_SCALE = [
    [0.00, "#22c55e"],
    [0.20, "#eab308"],
    [0.40, "#f97316"],
    [0.60, "#ef4444"],
    [0.80, "#a855f7"],
    [1.00, "#111827"]
]

WARM_COOL_SCALE = ["#06b6d4", "#6366f1", "#ec4899", "#f97316", "#ef4444"]


# ============================================================
# CUSTOM CSS (UI REFRESH ONLY — no logic changed below)
# ============================================================

st.markdown("""
<style>

/* ---------- Global background (colourful animated) ---------- */
.stApp {
    background: linear-gradient(-45deg, #ff6ec4, #7873f5, #4ade80, #38bdf8, #facc15, #f472b6, #ff6ec4);
    background-size: 500% 500%;
    animation: gradientShift 18s ease infinite;
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.block-container {
    background: rgba(248, 250, 252, 0.95);
    border-radius: 28px;
    margin-top: 14px;
    box-shadow: 0px 20px 60px rgba(0,0,0,0.35);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
    max-width: 1300px;
}

/* ---------- Header (colourful animated gradient title) ---------- */
.main-title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #ec4899, #6366f1 25%, #06b6d4 50%, #10b981 75%, #f59e0b);
    background-size: 300% 300%;
    animation: titleShift 8s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}

@keyframes titleShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.sub-title {
    text-align: center;
    font-size: 16px;
    color: #64748b;
    margin-bottom: 28px;
    font-weight: 600;
}

/* ---------- Cards ---------- */
.card {
    background: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 8px 24px rgba(15,23,42,0.06);
    border: 1px solid #eef1f6;
    margin-bottom: 18px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0px 12px 28px rgba(15,23,42,0.10);
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #0f172a;
    margin-top: 26px;
    margin-bottom: 14px;
    border-left: 5px solid #ec4899;
    padding-left: 12px;
    background: linear-gradient(90deg, rgba(236,72,153,0.08), rgba(99,102,241,0.02));
    border-radius: 6px;
    padding-top: 6px;
    padding-bottom: 6px;
}

.explanation-box {
    background: rgba(255,255,255,0.95);
    padding: 22px;
    border-radius: 20px;
    box-shadow: 0px 8px 24px rgba(15,23,42,0.06);
    border: 1px solid #eef1f6;
    margin-top: 15px;
}

.flow-box {
    background: linear-gradient(135deg, #ede9fe, #fce7f3);
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    border: 1px solid #e4e7ec;
    margin: 8px 0;
    font-weight: 600;
    color: #1e293b;
}

.arrow {
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: #ec4899;
}

.risk-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0px 8px 24px rgba(15,23,42,0.06);
    text-align: center;
    border: 1px solid #eef1f6;
}

/* ---------- Sidebar (colourful, titles in boxes) ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4c1d95, #6d28d9, #db2777);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

/* Sidebar main title box */
section[data-testid="stSidebar"] h1 {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 16px;
    padding: 14px 12px;
    text-align: center;
    font-size: 22px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
    margin-bottom: 10px;
}

/* Sidebar "Dashboard Controls" markdown heading box */
section[data-testid="stSidebar"] h3 {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    padding: 10px 12px;
    text-align: center;
    margin-top: 8px;
    margin-bottom: 14px;
}

/* Sidebar radio group container -> box */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 16px;
    padding: 10px;
}

/* Each radio option -> its own mini box */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 12px;
    padding: 10px 12px !important;
    margin-bottom: 8px !important;
    width: 100%;
    transition: transform 0.15s ease, background 0.15s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.22);
    transform: translateX(3px);
}

section[data-testid="stSidebar"] .stRadio > label {
    font-weight: 700;
}

/* ---------- Metric styling ---------- */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff, #f5f3ff);
    border-radius: 16px;
    padding: 14px 16px;
    border: 1px solid #eef1f6;
    box-shadow: 0px 4px 14px rgba(99,102,241,0.10);
}

/* ---------- Dataframe corners ---------- */
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 28px 0 14px 0;
}

/* ---------- Feature slide cards ---------- */
.feature-card {
    background: white;
    border-radius: 20px;
    padding: 22px;
    border: 1px solid #eef1f6;
    box-shadow: 0px 8px 24px rgba(15,23,42,0.07);
    height: 100%;
}

.feature-card h4 {
    margin-top: 0;
    color: #0f172a;
}

.advisory-pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 10px;
}

.pill-green { background: #dcfce7; color: #166534; }
.pill-yellow { background: #fef9c3; color: #854d0e; }
.pill-orange { background: #ffedd5; color: #9a3412; }
.pill-red { background: #fee2e2; color: #991b1b; }
.pill-purple { background: #f3e8ff; color: #6b21a8; }
.pill-black { background: #e5e7eb; color: #111827; }

.delta-up { color: #dc2626; font-weight: 700; }
.delta-down { color: #16a34a; font-weight: 700; }
.delta-flat { color: #64748b; font-weight: 700; }

</style>
""", unsafe_allow_html=True)


# ============================================================
# FILE PATHS
# ============================================================

FORECAST_FILE = "outputs/forecast_72h.csv"
LOCATION_FORECAST_FILE = "outputs/location_forecast_72h.csv"
LOCATION_FILE = "data/delhi_locations.csv"
MAIN_DATA_FILE = "data/delhincr.csv"

METRICS_FILE = "outputs/05_metrics_by_horizon.csv"
SUMMARY_FILE = "outputs/05_summary_24_48_72.csv"
IMPORTANCE_FILE = "outputs/07_feature_importance.csv"


# ============================================================
# CHECK MAIN FORECAST
# ============================================================

if not os.path.exists(FORECAST_FILE):

    st.error("❌ forecast_72h.csv was not found.")

    st.info(
        "Please run your main 72-hour forecasting script first."
    )

    st.stop()


# ============================================================
# LOAD MAIN FORECAST
# ============================================================

forecast = pd.read_csv(FORECAST_FILE)

if "timestamp" in forecast.columns:

    forecast["timestamp"] = pd.to_datetime(
        forecast["timestamp"],
        errors="coerce"
    )

    forecast = forecast.dropna(
        subset=["timestamp"]
    )

    forecast = forecast.sort_values(
        "timestamp"
    ).reset_index(drop=True)


# ============================================================
# LOAD LOCATION DATA
# ============================================================

location_data = None

if os.path.exists(LOCATION_FILE):

    location_data = pd.read_csv(
        LOCATION_FILE
    )


# ============================================================
# LOAD LOCATION FORECAST
# ============================================================

location_forecast = None

if os.path.exists(LOCATION_FORECAST_FILE):

    location_forecast = pd.read_csv(
        LOCATION_FORECAST_FILE
    )

    if "timestamp" in location_forecast.columns:

        location_forecast["timestamp"] = pd.to_datetime(
            location_forecast["timestamp"],
            errors="coerce"
        )

    if "predicted_aqi" in location_forecast.columns:

        location_forecast["predicted_aqi"] = pd.to_numeric(
            location_forecast["predicted_aqi"],
            errors="coerce"
        )

    if "predicted_pm25" in location_forecast.columns:

        location_forecast["predicted_pm25"] = pd.to_numeric(
            location_forecast["predicted_pm25"],
            errors="coerce"
        )

    if "location" in location_forecast.columns:

        location_forecast = location_forecast.dropna(
            subset=["location"]
        )


# ============================================================
# LOAD MAIN DATA
# ============================================================

main_data = None

if os.path.exists(MAIN_DATA_FILE):

    main_data = pd.read_csv(
        MAIN_DATA_FILE
    )

    if "timestamp" in main_data.columns:

        main_data["timestamp"] = pd.to_datetime(
            main_data["timestamp"],
            errors="coerce"
        )

        main_data = main_data.sort_values(
            "timestamp"
        )


# ============================================================
# LOAD MODEL METRICS
# ============================================================

metrics = None

if os.path.exists(METRICS_FILE):

    try:
        metrics = pd.read_csv(METRICS_FILE)
    except Exception:
        metrics = None


summary_metrics = None

if os.path.exists(SUMMARY_FILE):

    try:
        summary_metrics = pd.read_csv(SUMMARY_FILE)
    except Exception:
        summary_metrics = None


# ============================================================
# LOAD FEATURE IMPORTANCE
# ============================================================

feature_importance = None

if os.path.exists(IMPORTANCE_FILE):

    try:
        feature_importance = pd.read_csv(
            IMPORTANCE_FILE
        )
    except Exception:
        feature_importance = None


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🌫️ Delhi Air Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'AI-Powered Air Pollution Monitoring & 72-Hour Forecasting System'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FORECAST START
# ============================================================

if "timestamp" in forecast.columns and len(forecast) > 0:

    latest_time = forecast["timestamp"].min()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📅 Forecast Start\n\n"
            + latest_time.strftime("%d %B %Y")
        )

    with col2:

        st.info(
            "🕐 Forecast Time\n\n"
            + latest_time.strftime("%I:%M %p")
        )

    with col3:

        st.info(
            "📍 Region\n\nDelhi NCR"
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🌫️ Delhi Air Intelligence")

st.sidebar.markdown(
    "### Dashboard Controls"
)

page = st.sidebar.radio(
    "Select View",
    [
        "🏠 Overview",
        "🗺️ Delhi AQI Map",
        "📈 72-Hour Forecast",
        "🔎 Why Is AQI High?",
        "📊 Location Analysis",
        "🚀 Smart Insights",
        "🤖 Model Information"
    ]
)


# ============================================================
# AQI CATEGORY
# ============================================================

def get_aqi_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Satisfactory"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 300:
        return "Poor"

    elif aqi <= 400:
        return "Very Poor"

    else:
        return "Severe"


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(aqi):

    if aqi <= 100:
        return "🟢 LOW RISK"

    elif aqi <= 200:
        return "🟡 MODERATE RISK"

    elif aqi <= 300:
        return "🟠 HIGH RISK"

    elif aqi <= 400:
        return "🔴 VERY HIGH RISK"

    else:
        return "⚫ SEVERE RISK"


# ============================================================
# RISK COLOR
# ============================================================

def get_risk_color(aqi):

    if aqi <= 100:
        return "green"

    elif aqi <= 200:
        return "yellow"

    elif aqi <= 300:
        return "orange"

    elif aqi <= 400:
        return "red"

    else:
        return "black"


# ============================================================
# LOCATION FORECAST SUMMARY
# ============================================================

def create_location_summary():

    if location_forecast is None:
        return None

    if "location" not in location_forecast.columns:
        return None

    if "predicted_aqi" not in location_forecast.columns:
        return None

    data = location_forecast.copy()

    data["predicted_aqi"] = pd.to_numeric(
        data["predicted_aqi"],
        errors="coerce"
    )

    if "predicted_pm25" not in data.columns:

        data["predicted_pm25"] = np.nan

    data["predicted_pm25"] = pd.to_numeric(
        data["predicted_pm25"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["location", "predicted_aqi"]
    )

    if len(data) == 0:
        return None

    summary = data.groupby(
        "location"
    ).agg(
        max_aqi=("predicted_aqi", "max"),
        average_aqi=("predicted_aqi", "mean"),
        max_pm25=("predicted_pm25", "max"),
        average_pm25=("predicted_pm25", "mean")
    ).reset_index()

    summary["aqi_category"] = summary[
        "max_aqi"
    ].apply(get_aqi_category)

    summary["risk"] = summary[
        "max_aqi"
    ].apply(get_risk_level)

    summary["risk_color"] = summary[
        "max_aqi"
    ].apply(get_risk_color)

    summary = summary.sort_values(
        "max_aqi",
        ascending=False
    ).reset_index(drop=True)

    summary["rank"] = range(
        1,
        len(summary) + 1
    )

    return summary


location_summary = create_location_summary()


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        '<div class="section-title">🌤️ Current Air Quality</div>',
        unsafe_allow_html=True
    )

    current = forecast.iloc[0]

    pm25 = float(
        current["predicted_pm25"]
    )

    aqi = float(
        current["predicted_aqi"]
    )

    category = current.get(
        "aqi_category",
        get_aqi_category(aqi)
    )


    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🌫️ PM2.5",
            f"{pm25:.1f} µg/m³"
        )

    with c2:

        st.metric(
            "📊 Predicted AQI",
            f"{aqi:.0f}"
        )

    with c3:

        st.metric(
            "⚠️ Category",
            category
        )

    with c4:

        st.metric(
            "⏱️ Forecast",
            "72 Hours"
        )


    if aqi <= 50:

        st.success(
            "🟢 Air quality is GOOD."
        )

    elif aqi <= 100:

        st.info(
            "🟡 Air quality is SATISFACTORY."
        )

    elif aqi <= 200:

        st.warning(
            "🟠 Air quality is MODERATE."
        )

    elif aqi <= 300:

        st.warning(
            "🔴 Air quality is POOR."
        )

    elif aqi <= 400:

        st.error(
            "🟣 Air quality is VERY POOR."
        )

    else:

        st.error(
            "⚫ Air quality is SEVERE."
        )


    # --------------------------------------------------------
    # MAIN FORECAST
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📈 72-Hour PM2.5 Trend</div>',
        unsafe_allow_html=True
    )

    fig = px.line(
        forecast,
        x="timestamp",
        y="predicted_pm25",
        markers=True,
        title="Predicted PM2.5",
        color_discrete_sequence=["#ec4899"]
    )

    fig.update_traces(
        line=dict(width=3, color="#ec4899"),
        marker=dict(size=6, color="#6366f1")
    )

    fig.update_layout(
        xaxis_title="Date & Time",
        yaxis_title="PM2.5 (µg/m³)",
        hovermode="x unified",
        plot_bgcolor="rgba(246,244,255,0.6)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # FUTURE LOCATION RISK
    # --------------------------------------------------------

    if location_summary is not None:

        st.markdown(
            '<div class="section-title">'
            '📍 Next 72-Hour Location Risk'
            '</div>',
            unsafe_allow_html=True
        )

        top = location_summary.iloc[0]

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "🔴 Highest Risk Location",
                top["location"]
            )

        with c2:

            st.metric(
                "Maximum Predicted AQI",
                f"{top['max_aqi']:.0f}"
            )

        with c3:

            st.metric(
                "Risk",
                top["risk"]
            )


# ============================================================
# DELHI AQI MAP
# ============================================================

elif page == "🗺️ Delhi AQI Map":

    st.markdown(
        '<div class="section-title">'
        '🗺️ Delhi Location-wise 72-Hour AQI Risk Map'
        '</div>',
        unsafe_allow_html=True
    )


    if location_forecast is None:

        st.error(
            "❌ location_forecast_72h.csv was not found."
        )

        st.info(
            "Run 08_location_forecast.py first."
        )

        st.stop()


    if location_data is None:

        st.error(
            "❌ delhi_locations.csv was not found."
        )

        st.stop()


    if location_summary is None:

        st.error(
            "❌ Location forecast data is incomplete."
        )

        st.stop()


    summary = location_summary.copy()


    # --------------------------------------------------------
    # GET COORDINATES
    # --------------------------------------------------------

    coordinates = location_data[
        [
            "location",
            "lat",
            "lon"
        ]
    ].drop_duplicates(
        subset=["location"]
    )


    coordinates["lat"] = pd.to_numeric(
        coordinates["lat"],
        errors="coerce"
    )

    coordinates["lon"] = pd.to_numeric(
        coordinates["lon"],
        errors="coerce"
    )


    map_data = summary.merge(
        coordinates,
        on="location",
        how="left"
    )


    map_data = map_data.dropna(
        subset=["lat", "lon"]
    )


    # --------------------------------------------------------
    # LOCATION FILTER
    # --------------------------------------------------------

    selected_location = st.selectbox(
        "📍 Select Location",
        ["All Locations"] +
        sorted(
            map_data["location"].unique()
        )
    )


    if selected_location != "All Locations":

        selected_map = map_data[
            map_data["location"] ==
            selected_location
        ].copy()

    else:

        selected_map = map_data.copy()


    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    if len(selected_map) > 0:

        fig_map = px.scatter_map(
            selected_map,
            lat="lat",
            lon="lon",
            size="max_aqi",
            color="max_aqi",
            hover_name="location",

            hover_data={
                "max_aqi": ":.0f",
                "average_aqi": ":.0f",
                "max_pm25": ":.1f",
                "average_pm25": ":.1f",
                "aqi_category": True,
                "risk": True,
                "lat": False,
                "lon": False
            },

            color_continuous_scale=AQI_COLOR_SCALE,

            zoom=9.5,

            center={
                "lat": 28.6139,
                "lon": 77.2090
            },

            height=650
        )


        fig_map.update_layout(

            map_style="open-street-map",

            margin={
                "r": 0,
                "t": 0,
                "l": 0,
                "b": 0
            },

            coloraxis_colorbar={
                "title": "Max AQI"
            }
        )


        st.plotly_chart(
            fig_map,
            use_container_width=True,
            key="future_location_map"
        )


    # --------------------------------------------------------
    # RISK LEGEND
    # --------------------------------------------------------

    st.markdown(
        "### 🚦 Future AQI Risk Levels"
    )

    r1, r2, r3, r4, r5 = st.columns(5)

    with r1:
        st.success("🟢 AQI ≤ 100\nLow Risk")

    with r2:
        st.warning("🟡 AQI 101–200\nModerate")

    with r3:
        st.warning("🟠 AQI 201–300\nHigh")

    with r4:
        st.error("🔴 AQI 301–400\nVery High")

    with r5:
        st.error("⚫ AQI > 400\nSevere")


    # --------------------------------------------------------
    # HIGHEST RISK LOCATION
    # --------------------------------------------------------

    st.markdown(
        "### 🚨 Highest-Risk Location in Next 72 Hours"
    )


    highest = summary.iloc[0]


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "📍 Location",
            highest["location"]
        )


    with c2:

        st.metric(
            "Maximum AQI",
            f"{highest['max_aqi']:.0f}"
        )


    with c3:

        st.metric(
            "Maximum PM2.5",
            f"{highest['max_pm25']:.1f}"
        )


    with c4:

        st.metric(
            "Risk",
            highest["risk"]
        )


    # --------------------------------------------------------
    # LOCATION RANKING
    # --------------------------------------------------------

    st.markdown(
        "### 🏆 Location Risk Ranking"
    )


    ranking = summary[
        [
            "rank",
            "location",
            "max_aqi",
            "average_aqi",
            "max_pm25",
            "risk",
            "aqi_category"
        ]
    ].copy()


    ranking.columns = [
        "Rank",
        "Location",
        "Max Forecast AQI",
        "Average AQI",
        "Max PM2.5",
        "Risk",
        "AQI Category"
    ]


    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 72-HOUR FORECAST
# ============================================================

elif page == "📈 72-Hour Forecast":

    st.markdown(
        '<div class="section-title">'
        '📈 AI 72-Hour Forecast'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # PM2.5
    # --------------------------------------------------------

    fig1 = px.line(
        forecast,
        x="timestamp",
        y="predicted_pm25",
        markers=True,
        title="🌫️ Predicted PM2.5",
        color_discrete_sequence=["#06b6d4"]
    )

    fig1.update_traces(
        line=dict(width=3, color="#06b6d4"),
        marker=dict(size=6, color="#ec4899")
    )

    fig1.update_layout(
        hovermode="x unified",
        plot_bgcolor="rgba(240,249,255,0.6)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )


    # --------------------------------------------------------
    # AQI
    # --------------------------------------------------------

    fig2 = px.line(
        forecast,
        x="timestamp",
        y="predicted_aqi",
        markers=True,
        title="📊 Predicted AQI",
        color_discrete_sequence=["#8b5cf6"]
    )

    fig2.update_traces(
        line=dict(width=3, color="#8b5cf6"),
        marker=dict(size=6, color="#f59e0b")
    )

    fig2.update_layout(
        hovermode="x unified",
        plot_bgcolor="rgba(250,245,255,0.6)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    st.markdown(
        "### ⚠️ Forecast AQI Categories"
    )

    category_count = forecast[
        "aqi_category"
    ].value_counts().reset_index()

    category_count.columns = [
        "Category",
        "Hours"
    ]


    fig3 = px.bar(
        category_count,
        x="Category",
        y="Hours",
        title="Number of Forecast Hours in Each AQI Category",
        color="Category",
        color_discrete_sequence=COLORFUL_SEQUENCE
    )

    fig3.update_layout(
        plot_bgcolor="rgba(255,251,235,0.6)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


    # --------------------------------------------------------
    # COMPLETE FORECAST
    # --------------------------------------------------------

    st.markdown(
        "### 🕐 Complete Forecast"
    )

    table = forecast.copy()


    rename_map = {

        "timestamp":
            "Date & Time",

        "forecast_hour":
            "Forecast Hour",

        "predicted_pm25":
            "Predicted PM2.5",

        "predicted_aqi":
            "Predicted AQI",

        "aqi_category":
            "AQI Category"
    }


    table = table.rename(
        columns=rename_map
    )


    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# WHY IS AQI HIGH
# ============================================================

elif page == "🔎 Why Is AQI High?":

    st.markdown(
        '<div class="section-title">'
        '🔎 Why Is AQI High?'
        '</div>',
        unsafe_allow_html=True
    )


    if main_data is None:

        st.warning(
            "Main historical dataset was not found."
        )

        st.info(
            "The explanation section requires data/delhincr.csv."
        )

    else:

        # ----------------------------------------------------
        # GET LATEST AVAILABLE RECORD
        # ----------------------------------------------------

        if "timestamp" in main_data.columns:

            valid_data = main_data.dropna(
                subset=["timestamp"]
            )

        else:

            valid_data = main_data.copy()


        if len(valid_data) == 0:

            st.warning(
                "No valid historical records were found."
            )

        else:

            row = valid_data.iloc[-1]


            # ------------------------------------------------
            # READ IMPORTANT VARIABLES
            # ------------------------------------------------

            def get_value(column):

                if column in row.index:

                    try:
                        return float(row[column])
                    except Exception:
                        return np.nan

                return np.nan


            pm25_value = get_value(
                "pm2_5_ugm3"
            )

            wind_value = get_value(
                "wind_speed_10m_kmh"
            )

            boundary_value = get_value(
                "boundary_layer_height_m"
            )

            inversion_value = get_value(
                "inversion_strength_c"
            )

            fire_value = get_value(
                "upwind_stubble_fire_count"
            )

            humidity_value = get_value(
                "relative_humidity"
            )


            # ------------------------------------------------
            # CURRENT CONDITIONS
            # ------------------------------------------------

            st.markdown(
                "### 🌫️ Atmospheric Conditions"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                if not np.isnan(pm25_value):

                    st.metric(
                        "PM2.5",
                        f"{pm25_value:.1f} µg/m³"
                    )

                else:

                    st.metric(
                        "PM2.5",
                        "N/A"
                    )


            with c2:

                if not np.isnan(wind_value):

                    st.metric(
                        "Wind Speed",
                        f"{wind_value:.1f} km/h"
                    )

                else:

                    st.metric(
                        "Wind Speed",
                        "N/A"
                    )


            with c3:

                if not np.isnan(humidity_value):

                    st.metric(
                        "Relative Humidity",
                        f"{humidity_value:.1f}%"
                    )

                else:

                    st.metric(
                        "Relative Humidity",
                        "N/A"
                    )


            # ------------------------------------------------
            # PHYSICAL EXPLANATION
            # ------------------------------------------------

            st.markdown(
                "### 🔬 Pollution Formation & Accumulation"
            )

            st.markdown(
                '<div class="explanation-box">',
                unsafe_allow_html=True
            )

            f1, f2, f3 = st.columns(3)

            with f1:

                st.markdown(
                    '<div class="flow-box">'
                    '🔥 Pollution Sources'
                    '<br><br>'
                    'Vehicles • Industry • Biomass Burning'
                    '</div>',
                    unsafe_allow_html=True
                )

            with f2:

                st.markdown(
                    '<div class="flow-box">'
                    '🌬️ Atmospheric Conditions'
                    '<br><br>'
                    'Wind • Humidity • PBL • Temperature'
                    '</div>',
                    unsafe_allow_html=True
                )

            with f3:

                st.markdown(
                    '<div class="flow-box">'
                    '🌫️ Pollution Accumulation'
                    '<br><br>'
                    'PM2.5 increases → AQI increases'
                    '</div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # EXPLANATION RULES
            # ------------------------------------------------

            st.markdown(
                "### 🧠 Why Can Pollution Become High?"
            )


            explanations = []


            if not np.isnan(wind_value):

                if wind_value < 5:

                    explanations.append(
                        "🌬️ **Low wind speed:** "
                        "weak winds reduce the dispersion of pollutants."
                    )

                elif wind_value < 10:

                    explanations.append(
                        "🌬️ **Moderate wind:** "
                        "pollutant dispersion may still be limited."
                    )

                else:

                    explanations.append(
                        "🌬️ **Stronger wind:** "
                        "generally helps disperse pollutants."
                    )


            if not np.isnan(boundary_value):

                if boundary_value < 500:

                    explanations.append(
                        "⬇️ **Low planetary boundary layer height:** "
                        "pollutants are trapped closer to the surface."
                    )

                else:

                    explanations.append(
                        "⬆️ **Higher planetary boundary layer:** "
                        "provides more atmospheric volume for dispersion."
                    )


            if not np.isnan(inversion_value):

                if inversion_value > 2:

                    explanations.append(
                        "🌡️ **Atmospheric inversion:** "
                        "stable air can suppress vertical mixing."
                    )

                else:

                    explanations.append(
                        "🌡️ **Weak inversion:** "
                        "there is less evidence of strong temperature inversion."
                    )


            if not np.isnan(fire_value):

                if fire_value > 0:

                    explanations.append(
                        "🔥 **Upwind stubble-fire activity detected:** "
                        "regional biomass burning can contribute to pollution."
                    )

                else:

                    explanations.append(
                        "🔥 **No detected upwind stubble-fire activity "
                        "in the available record.**"
                    )


            if not np.isnan(humidity_value):

                if humidity_value > 80:

                    explanations.append(
                        "💧 **High humidity:** "
                        "humid conditions can contribute to particulate growth "
                        "and haze."
                    )


            if len(explanations) == 0:

                st.info(
                    "Not enough atmospheric variables are available "
                    "to generate a detailed explanation."
                )

            else:

                for reason in explanations:

                    st.warning(
                        reason
                    )


# ============================================================
# LOCATION ANALYSIS
# ============================================================

elif page == "📊 Location Analysis":

    st.markdown(
        '<div class="section-title">'
        '📊 Location-wise Future Air Quality Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    if location_forecast is None:

        st.error(
            "❌ location_forecast_72h.csv was not found."
        )

        st.info(
            "Run 08_location_forecast.py first."
        )

        st.stop()


    if location_summary is None:

        st.error(
            "❌ Location forecast data is incomplete."
        )

        st.stop()


    # --------------------------------------------------------
    # SELECT LOCATION
    # --------------------------------------------------------

    selected_location = st.selectbox(
        "📍 Choose a Delhi NCR Location",
        sorted(
            location_summary["location"].unique()
        )
    )


    selected_data = location_forecast[
        location_forecast["location"] ==
        selected_location
    ].copy()


    selected_data = selected_data.sort_values(
        "timestamp"
    )


    selected_summary = location_summary[
        location_summary["location"] ==
        selected_location
    ].iloc[0]


    # --------------------------------------------------------
    # LOCATION METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "📍 Location",
            selected_location
        )


    with c2:

        st.metric(
            "Maximum Forecast AQI",
            f"{selected_summary['max_aqi']:.0f}"
        )


    with c3:

        st.metric(
            "Average AQI",
            f"{selected_summary['average_aqi']:.0f}"
        )


    with c4:

        st.metric(
            "Risk",
            selected_summary["risk"]
        )


    # --------------------------------------------------------
    # PM2.5 METRICS
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Maximum PM2.5",
            f"{selected_summary['max_pm25']:.1f} µg/m³"
        )


    with c2:

        st.metric(
            "Average PM2.5",
            f"{selected_summary['average_pm25']:.1f} µg/m³"
        )


    with c3:

        st.metric(
            "AQI Category",
            selected_summary["aqi_category"]
        )


    # --------------------------------------------------------
    # PEAK TIME
    # --------------------------------------------------------

    peak_row = selected_data.loc[
        selected_data["predicted_aqi"].idxmax()
    ]


    st.markdown(
        "### 🚨 Peak Pollution Period"
    )


    p1, p2, p3 = st.columns(3)


    with p1:

        st.metric(
            "Peak AQI",
            f"{peak_row['predicted_aqi']:.0f}"
        )


    with p2:

        st.metric(
            "Peak PM2.5",
            f"{peak_row['predicted_pm25']:.1f}"
        )


    with p3:

        st.metric(
            "Peak Time",
            peak_row["timestamp"].strftime(
                "%d %b %Y, %I:%M %p"
            )
        )


    # --------------------------------------------------------
    # AQI CHART
    # --------------------------------------------------------

    fig_aqi = px.line(
        selected_data,
        x="timestamp",
        y="predicted_aqi",
        markers=True,
        title=(
            "📊 "
            + selected_location
            + " - Predicted AQI"
        ),
        color_discrete_sequence=["#f97316"]
    )

    fig_aqi.update_traces(
        line=dict(width=3, color="#f97316"),
        marker=dict(size=6, color="#6366f1")
    )

    fig_aqi.update_layout(
        xaxis_title="Date & Time",
        yaxis_title="Predicted AQI",
        hovermode="x unified",
        plot_bgcolor="rgba(255,247,237,0.6)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_aqi,
        use_container_width=True
    )


    # --------------------------------------------------------
    # PM2.5 CHART
    # --------------------------------------------------------

    fig_pm = px.line(
        selected_data,
        x="timestamp",
        y="predicted_pm25",
        markers=True,
        title=(
            "🌫️ "
            + selected_location
            + " - Predicted PM2.5"
        ),
        color_discrete_sequence=["#10b981"]
    )

    fig_pm.update_traces(
        line=dict(width=3, color="#10b981"),
        marker=dict(size=6, color="#ec4899")
    )

    fig_pm.update_layout(
        xaxis_title="Date & Time",
        yaxis_title="PM2.5 (µg/m³)",
        hovermode="x unified",
        plot_bgcolor="rgba(236,253,245,0.6)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_pm,
        use_container_width=True
    )


    # --------------------------------------------------------
    # LOCATION FORECAST TABLE
    # --------------------------------------------------------

    st.markdown(
        "### 🕐 Location Forecast"
    )


    location_table = selected_data.copy()


    location_table = location_table.rename(
        columns={
            "timestamp": "Date & Time",
            "predicted_aqi": "Predicted AQI",
            "predicted_pm25": "Predicted PM2.5"
        }
    )


    st.dataframe(
        location_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SMART INSIGHTS (NEW EXTRA SLIDE — additive only, uses
# existing loaded data; does not modify any prior logic)
# ============================================================

elif page == "🚀 Smart Insights":

    st.markdown(
        '<div class="section-title">🚀 Smart Insights & Advisory</div>',
        unsafe_allow_html=True
    )

    current = forecast.iloc[0]
    current_aqi = float(current["predicted_aqi"])
    current_pm25 = float(current["predicted_pm25"])
    current_category = current.get(
        "aqi_category",
        get_aqi_category(current_aqi)
    )

    pill_class_map = {
        "green": "pill-green",
        "yellow": "pill-yellow",
        "orange": "pill-orange",
        "red": "pill-red",
        "purple": "pill-purple",
        "black": "pill-black"
    }

    current_risk_color = get_risk_color(current_aqi)
    pill_class = pill_class_map.get(current_risk_color, "pill-yellow")

    # ------------------------------------------------------
    # 1. HEALTH ADVISORY ENGINE
    # ------------------------------------------------------

    st.markdown("### 🩺 Health Advisory")

    def get_health_advisory(aqi):

        if aqi <= 50:
            return [
                "✅ Safe for outdoor activities and exercise.",
                "✅ Windows can be kept open for ventilation."
            ]
        elif aqi <= 100:
            return [
                "🙂 Air quality is acceptable for most people.",
                "⚠️ Unusually sensitive individuals should watch for symptoms."
            ]
        elif aqi <= 200:
            return [
                "😷 Sensitive groups (children, elderly, asthma/heart patients) "
                "should reduce prolonged outdoor exertion.",
                "🪟 Consider keeping windows closed during peak traffic hours."
            ]
        elif aqi <= 300:
            return [
                "😷 Wear an N95 mask outdoors.",
                "🏃 Avoid outdoor exercise; shift workouts indoors.",
                "🫁 Asthma/COPD patients should keep rescue medication handy."
            ]
        elif aqi <= 400:
            return [
                "🚫 Avoid all outdoor physical activity.",
                "😷 N95/N99 mask mandatory outdoors.",
                "🏫 Consider outdoor school activity suspension.",
                "🌬️ Run air purifiers indoors if available."
            ]
        else:
            return [
                "🚨 SEVERE: Stay indoors as much as possible.",
                "😷 N99 mask required for any outdoor exposure.",
                "🏥 High risk for respiratory/cardiac patients — seek medical "
                "advice if symptoms appear.",
                "🏫 Recommend school closures / work-from-home advisories."
            ]

    st.markdown(
        f'<span class="advisory-pill {pill_class}">'
        f'{current_category.upper()} • AQI {current_aqi:.0f}</span>',
        unsafe_allow_html=True
    )

    advisory_lines = get_health_advisory(current_aqi)

    adv_col1, adv_col2 = st.columns(2)

    for i, line in enumerate(advisory_lines):
        target_col = adv_col1 if i % 2 == 0 else adv_col2
        with target_col:
            st.markdown(
                f'<div class="feature-card">{line}</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # 2. TREND VS YESTERDAY
    # ------------------------------------------------------

    st.markdown("### 📉 Trend vs. Previous Reading")

    trend_available = False

    if main_data is not None and "timestamp" in main_data.columns:

        hist = main_data.dropna(subset=["timestamp"]).copy()

        if "pm2_5_ugm3" in hist.columns and len(hist) >= 2:

            hist["pm2_5_ugm3"] = pd.to_numeric(
                hist["pm2_5_ugm3"], errors="coerce"
            )

            hist = hist.dropna(subset=["pm2_5_ugm3"])

            if len(hist) >= 2:

                latest_val = float(hist.iloc[-1]["pm2_5_ugm3"])
                prev_val = float(hist.iloc[-2]["pm2_5_ugm3"])
                delta = latest_val - prev_val

                trend_available = True

    if trend_available:

        t1, t2, t3 = st.columns(3)

        with t1:
            st.metric(
                "Latest Recorded PM2.5",
                f"{latest_val:.1f} µg/m³"
            )

        with t2:
            st.metric(
                "Previous Recorded PM2.5",
                f"{prev_val:.1f} µg/m³"
            )

        with t3:
            if delta > 0:
                st.markdown(
                    f'<div class="feature-card">Change<br>'
                    f'<span class="delta-up">▲ {delta:.1f} µg/m³ (worse)</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            elif delta < 0:
                st.markdown(
                    f'<div class="feature-card">Change<br>'
                    f'<span class="delta-down">▼ {abs(delta):.1f} µg/m³ (better)</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="feature-card">Change<br>'
                    '<span class="delta-flat">● No change</span></div>',
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "Not enough historical PM2.5 records available to compute a trend."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # 3. SOURCE ATTRIBUTION SNAPSHOT
    # ------------------------------------------------------

    st.markdown("### 🧪 Likely Contributing Factors (Snapshot)")

    if main_data is not None and len(main_data.dropna(
        subset=["timestamp"] if "timestamp" in main_data.columns else []
    ) if "timestamp" in main_data.columns else main_data) > 0:

        valid_data = (
            main_data.dropna(subset=["timestamp"])
            if "timestamp" in main_data.columns
            else main_data
        )

        row = valid_data.iloc[-1]

        def safe_val(col):
            if col in row.index:
                try:
                    return float(row[col])
                except Exception:
                    return np.nan
            return np.nan

        wind_v = safe_val("wind_speed_10m_kmh")
        boundary_v = safe_val("boundary_layer_height_m")
        inversion_v = safe_val("inversion_strength_c")
        fire_v = safe_val("upwind_stubble_fire_count")
        humidity_v = safe_val("relative_humidity")

        factor_names = []
        factor_scores = []

        if not np.isnan(wind_v):
            factor_names.append("Low Wind Dispersion")
            factor_scores.append(max(0, 10 - wind_v))

        if not np.isnan(boundary_v):
            factor_names.append("Low Boundary Layer")
            factor_scores.append(max(0, (800 - boundary_v) / 100))

        if not np.isnan(inversion_v):
            factor_names.append("Temperature Inversion")
            factor_scores.append(max(0, inversion_v))

        if not np.isnan(fire_v):
            factor_names.append("Stubble Fire Activity")
            factor_scores.append(fire_v)

        if not np.isnan(humidity_v):
            factor_names.append("High Humidity / Haze")
            factor_scores.append(max(0, (humidity_v - 50) / 10))

        if len(factor_names) > 0:

            factor_df = pd.DataFrame({
                "Factor": factor_names,
                "Relative Contribution Score": factor_scores
            }).sort_values(
                "Relative Contribution Score", ascending=True
            )

            fig_factors = px.bar(
                factor_df,
                x="Relative Contribution Score",
                y="Factor",
                orientation="h",
                title="Estimated Relative Contribution (Illustrative)",
                color="Factor",
                color_discrete_sequence=COLORFUL_SEQUENCE
            )

            fig_factors.update_layout(
                coloraxis_showscale=False,
                showlegend=False,
                plot_bgcolor="rgba(245,243,255,0.6)",
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig_factors, use_container_width=True)

            st.caption(
                "Scores are a simplified, rule-based estimate from the latest "
                "available weather/fire readings — not a formal source-apportionment model."
            )

        else:

            st.info("Not enough atmospheric variables available for this snapshot.")

    else:

        st.info("Historical dataset not available for source attribution.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # 4. DOWNLOADABLE ADVISORY REPORT
    # ------------------------------------------------------

    st.markdown("### 📄 Downloadable Public Advisory")

    top_location_line = ""

    if location_summary is not None and len(location_summary) > 0:
        top_loc = location_summary.iloc[0]
        top_location_line = (
            f"Highest-Risk Location (Next 72h): {top_loc['location']} "
            f"(Max AQI {top_loc['max_aqi']:.0f}, {top_loc['risk']})\n"
        )

    report_lines = [
        "DELHI AIR INTELLIGENCE — PUBLIC ADVISORY BULLETIN",
        "=" * 55,
        f"Generated: {pd.Timestamp.now().strftime('%d %B %Y, %I:%M %p')}",
        "",
        f"Current Predicted AQI: {current_aqi:.0f} ({current_category})",
        f"Current Predicted PM2.5: {current_pm25:.1f} µg/m³",
        top_location_line,
        "Health Advisory:",
    ] + [f"  - {line}" for line in advisory_lines] + [
        "",
        "This bulletin is auto-generated from a 72-hour AI forecasting "
        "system for Delhi NCR.",
    ]

    report_text = "\n".join(report_lines)

    st.download_button(
        label="⬇️ Download Advisory Bulletin (.txt)",
        data=report_text,
        file_name="delhi_air_advisory_bulletin.txt",
        mime="text/plain"
    )

    st.text_area(
        "Preview",
        report_text,
        height=220
    )


# ============================================================
# MODEL INFORMATION
# ============================================================

elif page == "🤖 Model Information":

    st.markdown(
        '<div class="section-title">'
        '🤖 AI Model & System Information'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SYSTEM PIPELINE
    # --------------------------------------------------------

    st.markdown(
        "### 🔄 Forecasting Pipeline"
    )


    st.markdown(
        """
        <div class="explanation-box">

        <div class="flow-box">
        📥 Historical Weather + Pollution Data
        </div>

        <div class="arrow">↓</div>

        <div class="flow-box">
        🧹 Data Validation & Cleaning
        </div>

        <div class="arrow">↓</div>

        <div class="flow-box">
        ⚙️ Feature Engineering
        </div>

        <div class="arrow">↓</div>

        <div class="flow-box">
        🤖 Machine Learning Models
        </div>

        <div class="arrow">↓</div>

        <div class="flow-box">
        🔮 72-Hour AQI Forecast
        </div>

        <div class="arrow">↓</div>

        <div class="flow-box">
        🗺️ Location-wise Risk Analysis
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # MODELS
    # --------------------------------------------------------

    st.markdown(
        "### 🧠 Models Used"
    )


    model_table = pd.DataFrame({

        "Model": [
            "Persistence Baseline",
            "Random Forest",
            "HistGradientBoosting"
        ],

        "Purpose": [
            "Baseline comparison",
            "Non-linear ensemble prediction",
            "Gradient boosting prediction"
        ]
    })


    st.dataframe(
        model_table,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # ACTUAL METRICS
    # --------------------------------------------------------

    st.markdown(
        "### 📈 Model Performance"
    )


    if metrics is not None:

        st.dataframe(
            metrics,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Model performance file was not found."
        )


    if summary_metrics is not None:

        st.markdown(
            "### 📊 24 / 48 / 72 Hour Summary"
        )

        st.dataframe(
            summary_metrics,
            use_container_width=True,
            hide_index=True
        )


    # --------------------------------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------------------------------

    st.markdown(
        "### 🎯 Feature Importance"
    )


    if feature_importance is not None:

        st.dataframe(
            feature_importance,
            use_container_width=True,
            hide_index=True
        )

        # Try to find feature and importance columns

        feature_column = None
        importance_column = None

        for col in feature_importance.columns:

            lower = col.lower()

            if "feature" in lower:

                feature_column = col

            if (
                "importance" in lower
                or "importance" in lower
            ):

                importance_column = col


        if (
            feature_column is not None
            and importance_column is not None
        ):

            plot_data = feature_importance.copy()

            plot_data[importance_column] = pd.to_numeric(
                plot_data[importance_column],
                errors="coerce"
            )

            plot_data = plot_data.dropna(
                subset=[importance_column]
            )

            plot_data = plot_data.sort_values(
                importance_column,
                ascending=False
            ).head(15)

            fig_imp = px.bar(
                plot_data,
                x=importance_column,
                y=feature_column,
                orientation="h",
                title="Top 15 Important Features",
                color=importance_column,
                color_continuous_scale=WARM_COOL_SCALE
            )

            fig_imp.update_layout(
                coloraxis_showscale=False,
                plot_bgcolor="rgba(240,253,250,0.6)",
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig_imp,
                use_container_width=True
            )

    else:

        st.info(
            "Feature importance file was not found."
        )


    # --------------------------------------------------------
    # DATA ARCHITECTURE
    # --------------------------------------------------------

    st.markdown(
        "### 🗃️ Dataset Architecture"
    )


    data_info = pd.DataFrame({

        "Component": [
            "Historical Dataset",
            "Weather Variables",
            "Pollution Variables",
            "Fire Variables",
            "Location Data",
            "Forecast Horizon"
        ],

        "Description": [
            "Delhi NCR historical observations",
            "Temperature, humidity, wind, pressure and related variables",
            "PM2.5 and other pollutant measurements",
            "Regional fire / stubble-burning indicators when available",
            "Delhi NCR monitoring locations",
            "72 hours"
        ]
    })


    st.dataframe(
        data_info,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # LOCATION FORECAST STATUS
    # --------------------------------------------------------

    st.markdown(
        "### 📍 Location Forecast Status"
    )


    if location_forecast is not None:

        unique_locations = (
            location_forecast["location"]
            .nunique()
        )

        st.success(
            "✅ Location forecasting is available."
        )

        st.info(
            f"Forecast generated for "
            f"{unique_locations} locations."
        )

    else:

        st.warning(
            "⚠️ Location forecast file is not available."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <hr>

    <div style="text-align:center; color:#667085;">

    🌫️ <b>Delhi Air Intelligence</b><br>

    Air Pollution–Weather Coupled Forecasting System<br>

    Delhi NCR Focus • 72-Hour Forecasting

    </div>
    """,
    unsafe_allow_html=True
)
