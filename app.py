import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from datetime import date, timedelta
import requests
import re
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


# PAGE CONFIG

st.set_page_config(
    page_title="Bangladesh Rainfall & Agriculture System",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# DESIGN

INDIGO = "#0B1D33"
SLATE = "#1B4965"
TEAL = "#1F9E92"
AMBER = "#E8873A"
GREEN = "#2E8B57"
INK = "#0F2436"
LINE = "#D9E2EC"

pio.templates["monsoon"] = pio.templates["plotly_white"]
pio.templates["monsoon"].layout.colorway = [
    TEAL, INDIGO, AMBER, SLATE, GREEN, "#6FA8C4"
]
pio.templates["monsoon"].layout.font = dict(
    family="Inter, sans-serif",
    color=INK,
    size=13
)
pio.templates["monsoon"].layout.title.font = dict(
    family="Space Grotesk, sans-serif",
    size=16,
    color=INDIGO
)
pio.templates["monsoon"].layout.paper_bgcolor = "rgba(0,0,0,0)"
pio.templates["monsoon"].layout.plot_bgcolor = "rgba(0,0,0,0)"
pio.templates["monsoon"].layout.xaxis.gridcolor = LINE
pio.templates["monsoon"].layout.yaxis.gridcolor = LINE
pio.templates.default = "monsoon"


# CSS

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root{
    --bg:#F4F7F9;
    --card:#FFFFFF;
    --ink:#0F2436;
    --muted:#5F7280;
    --indigo:#0B1D33;
    --slate:#1B4965;
    --teal:#1F9E92;
    --green:#2E8B57;
    --amber:#E8873A;
    --line:#D9E2EC;
}

html,body{
    background:var(--bg)!important;
    color:var(--ink)!important;
    font-family:'Inter','Noto Sans Bengali',sans-serif!important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main{
    background:var(--bg)!important;
    color:var(--ink)!important;
}

.block-container{
    padding-top:1.4rem;
    padding-bottom:2rem;
    max-width:1360px;
}

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4{
    color:var(--indigo)!important;
    font-family:'Space Grotesk','Noto Sans Bengali',sans-serif!important;
}

[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] .stMarkdown{
    color:var(--ink)!important;
}

.hero{
    position:relative;
    overflow:hidden;
    padding:2.4rem;
    border-radius:20px;
    background:linear-gradient(135deg,#0B1D33 0%,#1B4965 100%);
    margin-bottom:1.6rem;
}

.hero h1{
    color:white!important;
    margin:0 0 .5rem;
}

.hero p{
    color:#D7E5EF!important;
}

.hero-stats{
    display:flex;
    gap:2rem;
    flex-wrap:wrap;
    margin-top:1.5rem;
}

.hero-stat{
    border-left:3px solid #1F9E92;
    padding-left:.8rem;
}

.hero-num{
    color:white!important;
    font-size:1.5rem;
    font-weight:700;
}

.hero-label{
    color:#B8CDDB!important;
    font-size:.8rem;
}

.section-title{
    font-size:1.2rem;
    font-weight:700;
    color:var(--indigo)!important;
    margin:1.5rem 0 .8rem;
}

.card{
    background:white;
    border:1px solid var(--line);
    border-radius:16px;
    padding:1.2rem;
    margin-bottom:1rem;
}

.agri-card{
    background:white;
    border:1px solid #D9E8DF;
    border-left:5px solid var(--green);
    border-radius:16px;
    padding:1.2rem;
    margin-bottom:1rem;
}

.result-card{
    background:linear-gradient(135deg,#F1FAF5,#FFFFFF);
    border:1px solid #B8DEC7;
    border-radius:18px;
    padding:1.5rem;
}

.warning-card{
    background:#FFF7EC;
    border-left:5px solid var(--amber);
    border-radius:12px;
    padding:1rem;
}

[data-testid="stMain"] label{
    color:var(--ink)!important;
    font-weight:600!important;
}

[data-testid="stMain"] input,
[data-testid="stMain"] textarea{
    background:white!important;
    color:var(--ink)!important;
}

[data-testid="stMain"] div[data-baseweb="select"] > div{
    background:white!important;
    color:var(--ink)!important;
}

[data-testid="stMain"] div[data-baseweb="select"] *{
    color:var(--ink)!important;
}

[data-testid="stMain"] .stButton>button{
    border-radius:10px;
    font-weight:600;
    background:white!important;
    color:var(--indigo)!important;
}

[data-testid="stMain"] .stButton>button[kind="primary"]{
    background:var(--teal)!important;
    color:white!important;
    border-color:var(--teal)!important;
}

div[data-testid="stMetric"],
div[data-testid="metric-container"]{
    background:white!important;
    border:1px solid var(--line)!important;
    border-radius:12px;
    padding:.8rem 1rem;
}

div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] *{
    color:var(--indigo)!important;
}

div[data-testid="stSidebar"]{
    background:#292D39!important;
}

div[data-testid="stSidebar"] p,
div[data-testid="stSidebar"] span,
div[data-testid="stSidebar"] label{
    color:#EAF0F5!important;
}

div[data-testid="stSidebar"] div[role="radiogroup"]{
    gap:4px!important;
}

div[data-testid="stSidebar"] div[role="radiogroup"] label{
    padding:.65rem .75rem!important;
    border-radius:10px;
}

div[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
    background:rgba(255,255,255,.08)!important;
}

div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){
    background:rgba(31,158,146,.25)!important;
    border-left:3px solid var(--teal)!important;
}

.footer{
    text-align:center;
    color:#5F7280!important;
    padding:2rem 0 1rem;
}

#MainMenu,footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# LOAD MODEL

@st.cache_resource
def load_model():

    candidates = [
        "rainfall_model.pkl",
        "rainfall_model(4).pkl",
        "rainfall_model(2).pkl"
    ]

    for name in candidates:

        if Path(name).exists():

            with open(name, "rb") as f:

                return pickle.load(f), name

    raise FileNotFoundError("rainfall_model.pkl not found")


@st.cache_data
def load_dataset():

    candidates = [
        "bangladesh_weather_stations_FINAL.csv",
        "bangladesh_weather_stations_FINAL(7).csv",
        "bangladesh_weather_stations_FINAL(4).csv"
    ]

    for name in candidates:

        if Path(name).exists():

            return pd.read_csv(name), name

    raise FileNotFoundError(
        "bangladesh_weather_stations_FINAL.csv not found"
    )


try:

    package, MODEL_FILE = load_model()

    df, CSV_FILE = load_dataset()

    model = package["model"]

    feature_columns = package["feature_columns"]

    train_medians = package["train_medians"]

except Exception as e:

    st.error(" File loading failed")

    st.exception(e)

    st.stop()


# DATA CHECK

required = [

    "Date",
    "Station_ID",
    "Latitude",
    "Longitude",

    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",

    "apparent_temperature_mean",

    "sunshine_duration",
    "daylight_duration",

    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",

    "shortwave_radiation_sum",

    "weather_code",

    "et0_fao_evapotranspiration",

    "rain_sum"
]


missing = [

    c for c in required

    if c not in df.columns
]


if missing:

    st.error(
        f"Missing columns: {missing}"
    )

    st.stop()


df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
).dt.normalize()


df = (
    df
    .dropna(subset=["Date"])
    .sort_values(
        ["Station_ID", "Date"]
    )
    .reset_index(drop=True)
)


for c in [

    "Station",
    "District",
    "Division"

]:

    if c not in df.columns:

        df[c] = df["Station_ID"]


# GLOBAL WEATHER VALUES

latitude = 0.0
longitude = 0.0

temperature_mean = 0.0
temperature_max = 0.0
temperature_min = 0.0

apparent_temperature = 0.0

sunshine_duration = 0.0
daylight_duration = 0.0

wind_speed = 0.0
wind_gusts = 0.0
wind_direction = 0.0

shortwave_radiation = 0.0

weather_code = 0

et0 = 0.0

# CREATE PREDICTION FEATURES

def create_prediction_features(
    historical_df,
    station,
    target_date
):

    data = historical_df.copy()

    data["Date"] = pd.to_datetime(
        data["Date"]
    )

    data = (

        data
        .sort_values(
            ["Station_ID", "Date"]
        )
        .reset_index(drop=True)

    )


    target_row = {

        "Date": target_date,

        "Station_ID": station,

        "Latitude": latitude,

        "Longitude": longitude,

        "temperature_2m_mean":
            temperature_mean,

        "temperature_2m_max":
            temperature_max,

        "temperature_2m_min":
            temperature_min,

        "apparent_temperature_mean":
            apparent_temperature,

        "sunshine_duration":
            sunshine_duration,

        "daylight_duration":
            daylight_duration,

        "wind_speed_10m_max":
            wind_speed,

        "wind_gusts_10m_max":
            wind_gusts,

        "wind_direction_10m_dominant":
            wind_direction,

        "shortwave_radiation_sum":
            shortwave_radiation,

        "weather_code":
            weather_code,

        "et0_fao_evapotranspiration":
            et0,

        "rain_sum":
            np.nan
    }


    data = data[
        ~(
            (data["Station_ID"] == station)
            &
            (data["Date"] == target_date)
        )
    ].copy()


    target_df = pd.DataFrame(
        [target_row]
    )


    data = pd.concat(
        [data, target_df],
        ignore_index=True
    )


    data = (

        data
        .sort_values(
            ["Station_ID", "Date"]
        )
        .reset_index(drop=True)

    )


    # CALENDAR

    data["year"] = (
        data["Date"].dt.year
    )

    data["month"] = (
        data["Date"].dt.month
    )

    data["day"] = (
        data["Date"].dt.day
    )

    data["dayofyear"] = (
        data["Date"].dt.dayofyear
    )

    data["dayofweek"] = (
        data["Date"].dt.dayofweek
    )

    data["weekofyear"] = (

        data["Date"]
        .dt.isocalendar()
        .week
        .astype(int)

    )


    # CYCLIC

    data["month_sin"] = np.sin(
        2 * np.pi *
        data["month"] / 12
    )

    data["month_cos"] = np.cos(
        2 * np.pi *
        data["month"] / 12
    )

    data["dayofyear_sin"] = np.sin(
        2 * np.pi *
        data["dayofyear"] /
        365.25
    )

    data["dayofyear_cos"] = np.cos(
        2 * np.pi *
        data["dayofyear"] /
        365.25
    )

    data["dayofweek_sin"] = np.sin(
        2 * np.pi *
        data["dayofweek"] /
        7
    )

    data["dayofweek_cos"] = np.cos(
        2 * np.pi *
        data["dayofweek"] /
        7
    )


    # RAIN LAGS

    RAIN_LAGS = [

        1, 2, 3,
        5, 7,
        14, 21, 30

    ]


    for lag in RAIN_LAGS:

        data[
            f"rain_lag_{lag}"
        ] = (

            data
            .groupby("Station_ID")
            ["rain_sum"]
            .shift(lag)

        )


    # RAIN OCCURRENCE

    rain_occurrence = (
        data["rain_sum"] > 0
    ).astype(int)


    for lag in [

        1, 2, 3, 7

    ]:

        data[
            f"rain_occurrence_lag_{lag}"
        ] = (

            rain_occurrence
            .groupby(
                data["Station_ID"]
            )
            .shift(lag)

        )


    # ROLLING

    shifted_rain = (

        data
        .groupby("Station_ID")
        ["rain_sum"]
        .shift(1)

    )


    for window in [

        3, 7, 14, 30

    ]:

        grouped_rain = (

            shifted_rain
            .groupby(
                data["Station_ID"]
            )

        )


        data[
            f"rain_roll_mean_{window}"
        ] = (

            grouped_rain
            .transform(
                lambda x:
                x.rolling(
                    window,
                    min_periods=1
                ).mean()
            )

        )


        data[
            f"rain_roll_sum_{window}"
        ] = (

            grouped_rain
            .transform(
                lambda x:
                x.rolling(
                    window,
                    min_periods=1
                ).sum()
            )

        )


        data[
            f"rain_roll_std_{window}"
        ] = (

            grouped_rain
            .transform(
                lambda x:
                x.rolling(
                    window,
                    min_periods=2
                ).std()
            )

        )


    # WEATHER LAGS

    same_day_weather = [

        "temperature_2m_mean",
        "temperature_2m_max",
        "temperature_2m_min",

        "apparent_temperature_mean",

        "sunshine_duration",
        "daylight_duration",

        "wind_speed_10m_max",
        "wind_gusts_10m_max",
        "wind_direction_10m_dominant",

        "shortwave_radiation_sum",

        "weather_code",

        "et0_fao_evapotranspiration"

    ]


    for feature in same_day_weather:

        for lag in [

            1, 2, 3, 7

        ]:

            data[
                f"{feature}_lag_{lag}"
            ] = (

                data
                .groupby(
                    "Station_ID"
                )[feature]
                .shift(lag)

            )


    # STATION DUMMIES

    station_dummies = pd.get_dummies(

        data["Station_ID"],

        prefix="station",

        dtype=int

    )


    data = pd.concat(
        [data, station_dummies],
        axis=1
    )


    prediction_row = data[

        (data["Station_ID"] == station)

        &

        (data["Date"] == target_date)

    ].copy()


    if len(prediction_row) != 1:

        raise ValueError(
            "Could not create target prediction row."
        )


    X_prediction = prediction_row.reindex(

        columns=feature_columns,

        fill_value=0

    )


    for col in X_prediction.columns:

        X_prediction[col] = pd.to_numeric(

            X_prediction[col],

            errors="coerce"

        )


    X_prediction = X_prediction.replace(
        [np.inf, -np.inf],
        np.nan
    )


    station_history = data[

        (data["Station_ID"] == station)

        &

        (data["Date"] < target_date)

    ].reindex(
        columns=feature_columns
    )


    for col in station_history.columns:

        station_history[col] = pd.to_numeric(

            station_history[col],

            errors="coerce"

        )


    station_medians = station_history.median(
        numeric_only=True
    )


    X_prediction = X_prediction.fillna(
        station_medians
    )


    X_prediction = X_prediction.fillna(
        train_medians
    )


    X_prediction = X_prediction.fillna(0)


    return X_prediction


# WEATHER VALUES

def set_weather_values(
    values,
    meta
):

    global latitude
    global longitude

    global temperature_mean
    global temperature_max
    global temperature_min

    global apparent_temperature

    global sunshine_duration
    global daylight_duration

    global wind_speed
    global wind_gusts
    global wind_direction

    global shortwave_radiation

    global weather_code

    global et0


    def num(
        k,
        default=0.0
    ):

        v = values.get(
            k,
            default
        )

        return (
            default
            if pd.isna(v)
            else float(v)
        )


    latitude = num(
        "Latitude",
        float(meta["Latitude"])
    )

    longitude = num(
        "Longitude",
        float(meta["Longitude"])
    )


    temperature_mean = num(
        "temperature_2m_mean"
    )

    temperature_max = num(
        "temperature_2m_max"
    )

    temperature_min = num(
        "temperature_2m_min"
    )

    apparent_temperature = num(
        "apparent_temperature_mean"
    )

    sunshine_duration = num(
        "sunshine_duration"
    )

    daylight_duration = num(
        "daylight_duration"
    )

    wind_speed = num(
        "wind_speed_10m_max"
    )

    wind_gusts = num(
        "wind_gusts_10m_max"
    )

    wind_direction = num(
        "wind_direction_10m_dominant"
    )

    shortwave_radiation = num(
        "shortwave_radiation_sum"
    )

    weather_code = int(
        num("weather_code")
    )

    et0 = num(
        "et0_fao_evapotranspiration"
    )


# HISTORY DAYS

def get_model_history_days():

    rain_lags = []

    roll_windows = []

    weather_lags = []


    for col in feature_columns:

        m = re.fullmatch(
            r"rain_lag_(\d+)",
            col
        )

        if m:

            rain_lags.append(
                int(m.group(1))
            )

            continue


        m = re.fullmatch(
            r"rain_roll_(?:mean|sum|std)_(\d+)",
            col
        )

        if m:

            roll_windows.append(
                int(m.group(1))
            )

            continue


        m = re.fullmatch(
            r"(.+)_lag_(\d+)",
            col
        )

        if m and not col.startswith("rain_"):

            weather_lags.append(
                int(m.group(2))
            )


    return max(

        rain_lags
        +
        roll_windows
        +
        weather_lags
        +
        [1]

    )


HISTORY_DAYS = get_model_history_days()


# OPEN METEO HISTORY

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def fetch_open_meteo_range(
    lat,
    lon,
    start_date,
    end_date
):

    start_date = pd.Timestamp(
        start_date
    ).date()

    end_date = pd.Timestamp(
        end_date
    ).date()


    if start_date > end_date:

        return pd.DataFrame()


    daily = [

        "rain_sum",

        "temperature_2m_mean",
        "temperature_2m_max",
        "temperature_2m_min",

        "apparent_temperature_mean",

        "sunshine_duration",
        "daylight_duration",

        "wind_speed_10m_max",
        "wind_gusts_10m_max",
        "wind_direction_10m_dominant",

        "shortwave_radiation_sum",

        "weather_code",

        "et0_fao_evapotranspiration"

    ]


    response = requests.get(

        "https://archive-api.open-meteo.com/v1/archive",

        params={

            "latitude": float(lat),

            "longitude": float(lon),

            "daily": ",".join(daily),

            "timezone": "Asia/Dhaka",

            "start_date": str(start_date),

            "end_date": str(end_date)

        },

        timeout=30

    )


    response.raise_for_status()


    daily_data = response.json().get(
        "daily",
        {}
    )


    if not daily_data or "time" not in daily_data:

        raise ValueError(
            "Historical weather API returned no daily data."
        )


    out = pd.DataFrame(
        daily_data
    ).rename(
        columns={
            "time": "Date"
        }
    )


    out["Date"] = pd.to_datetime(
        out["Date"]
    ).dt.normalize()


    return out


# BUILD HISTORY

def build_on_demand_history(
    station,
    target_date
):

    target_date = pd.Timestamp(
        target_date
    ).normalize()


    start_date = target_date - pd.Timedelta(
        days=HISTORY_DAYS
    )


    end_date = target_date - pd.Timedelta(
        days=1
    )


    station_id = station["Station_ID"]


    local = df[

        (df["Station_ID"] == station_id)

        &

        (df["Date"] >= start_date)

        &

        (df["Date"] <= end_date)

    ].copy()


    expected_dates = pd.date_range(

        start_date,

        end_date,

        freq="D"

    )


    local_dates = set(
        local["Date"].dt.normalize()
    )


    missing_dates = [

        d for d in expected_dates

        if d not in local_dates

    ]


    fetched = pd.DataFrame()


    if missing_dates:

        api_data = fetch_open_meteo_range(

            station["Latitude"],

            station["Longitude"],

            start_date,

            end_date

        )


        api_data = api_data[

            api_data["Date"].isin(
                missing_dates
            )

        ].copy()


        fetched = api_data.copy()

        fetched["Station_ID"] = station_id

        fetched["Latitude"] = station["Latitude"]

        fetched["Longitude"] = station["Longitude"]

        fetched["Station"] = station["Station"]

        fetched["District"] = station["District"]

        fetched["Division"] = station["Division"]


    history = pd.concat(

        [local, fetched],

        ignore_index=True

    )


    history = (

        history

        .drop_duplicates(

            subset=[
                "Station_ID",
                "Date"
            ],

            keep="last"

        )

        .sort_values(
            ["Station_ID", "Date"]
        )

        .reset_index(
            drop=True
        )

    )


    actual_dates = set(
        history["Date"].dt.normalize()
    )


    still_missing = [

        d.strftime("%Y-%m-%d")

        for d in expected_dates

        if d not in actual_dates

    ]


    if still_missing:

        raise ValueError(
            "Required historical data incomplete: "
            +
            ", ".join(
                still_missing[:10]
            )
        )


    if history["rain_sum"].isna().any():

        raise ValueError(
            "Required rain history contains missing values."
        )


    note = (

        f"Model needs {HISTORY_DAYS} previous days. "

        f"Used {len(local)} local CSV days and "

        f"{len(fetched)} API days."

    )


    return history, note


def build_prediction_history(
    station,
    target
):

    return build_on_demand_history(
        station,
        target
    )

# CONDITION

def condition(
    code,
    pred=None
):

    if pred is not None:

        if pred < 1:

            return (
                "☀️ Sunny",
                "Mostly dry conditions expected."
            )

        if pred < 10:

            return (
                "🌤️ Light Rain",
                "Light rainfall is possible."
            )

        if pred < 25:

            return (
                "🌧️ Moderate Rain",
                "Noticeable rainfall is expected."
            )

        if pred < 50:

            return (
                "⛈️ Heavy Rain",
                "Heavy rainfall expected."
            )

        return (
            "🚨 Very Heavy Rain",
            "Very heavy rainfall expected."
        )


    if code in [0, 1]:

        return (
            "☀️ Sunny",
            "Clear weather"
        )


    if code in [

        2, 3, 45, 48

    ]:

        return (
            "☁️ Cloudy",
            "Cloudy conditions"
        )


    return (
        "🌧️ Rainy",
        "Rainy conditions"
    )


# STATION TABLE

def station_table():

    return (

        df

        .groupby(
            "Station_ID",
            as_index=False
        )

        .agg(

            Station=(
                "Station",
                "first"
            ),

            District=(
                "District",
                "first"
            ),

            Division=(
                "Division",
                "first"
            ),

            Latitude=(
                "Latitude",
                "median"
            ),

            Longitude=(
                "Longitude",
                "median"
            )

        )

    )

# AGRICULTURE DATA
# Water requirement = Approximate mm/day

CROPS = {

    "ধান / Rice": {
        "name": "ধান / Rice",
        "water_mm": 7.0,
        "min_mm": 4.0,
        "max_mm": 10.0,
        "description": "ধান সাধারণত বেশি পানি প্রয়োজন করে।",
        "stage_factor": {
            "চারা / Seedling": 0.80,
            "বৃদ্ধি / Vegetative": 1.00,
            "ফুল / Flowering": 1.20,
            "দানার বৃদ্ধি / Grain Filling": 1.10,
            "পাকা / Maturity": 0.60
        }
    },

    "গম / Wheat": {
        "name": "গম / Wheat",
        "water_mm": 5.0,
        "min_mm": 3.0,
        "max_mm": 7.0,
        "description": "গমের জন্য মাঝারি পরিমাণ পানি প্রয়োজন।",
        "stage_factor": {
            "চারা / Seedling": 0.70,
            "বৃদ্ধি / Vegetative": 1.00,
            "ফুল / Flowering": 1.20,
            "দানার বৃদ্ধি / Grain Filling": 1.10,
            "পাকা / Maturity": 0.50
        }
    },

    "ভুট্টা / Maize": {
        "name": "ভুট্টা / Maize",
        "water_mm": 6.0,
        "min_mm": 3.0,
        "max_mm": 8.0,
        "description": "ফুল ও দানা গঠনের সময়ে বেশি পানি প্রয়োজন।",
        "stage_factor": {
            "চারা / Seedling": 0.70,
            "বৃদ্ধি / Vegetative": 1.00,
            "ফুল / Flowering": 1.30,
            "দানার বৃদ্ধি / Grain Filling": 1.20,
            "পাকা / Maturity": 0.60
        }
    },

    "আলু / Potato": {
        "name": "আলু / Potato",
        "water_mm": 5.0,
        "min_mm": 3.0,
        "max_mm": 7.0,
        "description": "আলুর মাটিতে অতিরিক্ত পানি জমে থাকা ক্ষতিকর।",
        "stage_factor": {
            "চারা / Seedling": 0.70,
            "বৃদ্ধি / Vegetative": 1.00,
            "ফুল / Flowering": 1.20,
            "দানার বৃদ্ধি / Grain Filling": 1.00,
            "পাকা / Maturity": 0.60
        }
    },

    "টমেটো / Tomato": {
        "name": "টমেটো / Tomato",
        "water_mm": 5.5,
        "min_mm": 3.0,
        "max_mm": 7.0,
        "description": "নিয়মিত কিন্তু নিয়ন্ত্রিত সেচ প্রয়োজন।",
        "stage_factor": {
            "চারা / Seedling": 0.70,
            "বৃদ্ধি / Vegetative": 1.00,
            "ফুল / Flowering": 1.20,
            "দানার বৃদ্ধি / Grain Filling": 1.20,
            "পাকা / Maturity": 0.80
        }
    },

    "পেঁয়াজ / Onion": {
        "name": "পেঁয়াজ / Onion",
        "water_mm": 4.0,
        "min_mm": 2.0,
        "max_mm": 6.0,
        "description": "অতিরিক্ত পানি পেঁয়াজের জন্য ক্ষতিকর হতে পারে।",
        "stage_factor": {
            "চারা / Seedling": 0.70,
            "বৃদ্ধি / Vegetative": 1.00,
            "ফুল / Flowering": 1.00,
            "দানার বৃদ্ধি / Grain Filling": 0.90,
            "পাকা / Maturity": 0.50
        }
    },

    "সবজি / Vegetables": {
        "name": "সবজি / Vegetables",
        "water_mm": 5.0,
        "min_mm": 3.0,
        "max_mm": 7.0,
        "description": "সাধারণ সবজির জন্য মাঝারি পানি প্রয়োজন।",
        "stage_factor": {
            "চারা / Seedling": 0.70,
            "বৃদ্ধি / Vegetative": 1.00,
            "ফুল / Flowering": 1.20,
            "দানার বৃদ্ধি / Grain Filling": 1.00,
            "পাকা / Maturity": 0.70
        }
    },

    "সরিষা / Mustard": {
        "name": "সরিষা / Mustard",
        "water_mm": 3.5,
        "min_mm": 2.0,
        "max_mm": 5.0,
        "description": "সরিষার জন্য তুলনামূলক কম পানি প্রয়োজন।",
        "stage_factor": {
            "চারা / Seedling": 0.70,
            "বৃদ্ধি / Vegetative": 1.00,
            "ফুল / Flowering": 1.20,
            "দানার বৃদ্ধি / Grain Filling": 1.00,
            "পাকা / Maturity": 0.50
        }
    }
}


SOIL_TYPES = {

    "বেলে মাটি / Sandy Soil": {
        "factor": 1.20,
        "description": "পানি দ্রুত নিচে চলে যায়, তাই বেশি সেচ লাগতে পারে।"
    },

    "দোআঁশ মাটি / Loamy Soil": {
        "factor": 1.00,
        "description": "পানি ধারণক্ষমতা মাঝারি ও ভালো।"
    },

    "এঁটেল মাটি / Clay Soil": {
        "factor": 0.85,
        "description": "পানি বেশি সময় ধরে রাখতে পারে।"
    }

}

# AGRICULTURE CALCULATION

def calculate_irrigation(

    land_area,
    area_unit,

    crop_name,
    crop_stage,

    soil_type,

    existing_water_mm,

    predicted_rain_mm,

    et0_value,

    irrigation_efficiency

):

    crop = CROPS[crop_name]

    soil = SOIL_TYPES[soil_type]


    # AREA TO M2

    if area_unit == "শতক / Decimal":

        area_m2 = land_area * 40.4686

    elif area_unit == "একর / Acre":

        area_m2 = land_area * 4046.86

    elif area_unit == "হেক্টর / Hectare":

        area_m2 = land_area * 10000

    else:

        area_m2 = land_area


    # CROP WATER REQUIREMENT

    base_crop_water = crop["water_mm"]

    stage_factor = crop["stage_factor"][crop_stage]

    soil_factor = soil["factor"]


    crop_water_need = (

        base_crop_water

        * stage_factor

        * soil_factor

    )


    # ET0 ADJUSTMENT

    if et0_value > 0:

        et_factor = min(
            max(
                et0_value / 5,
                0.70
            ),
            1.40
        )

    else:

        et_factor = 1.0


    crop_water_need = (

        crop_water_need
        *
        et_factor

    )


    # EFFECTIVE RAINFALL

    if predicted_rain_mm <= 5:

        effective_rain = (
            predicted_rain_mm * 0.90
        )

    elif predicted_rain_mm <= 20:

        effective_rain = (
            predicted_rain_mm * 0.80
        )

    else:

        effective_rain = (
            predicted_rain_mm * 0.65
        )


    # TOTAL AVAILABLE WATER

    available_water = (

        existing_water_mm

        +

        effective_rain

    )


    # NET WATER REQUIRED

    net_water_needed = max(

        crop_water_need

        -

        available_water,

        0

    )


    # IRRIGATION EFFICIENCY

    efficiency = max(
        irrigation_efficiency / 100,
        0.10
    )


    gross_water_mm = (

        net_water_needed

        / efficiency

    )


    # MM TO LITER

    water_liters = (

        gross_water_mm

        * area_m2

    )


    water_m3 = (

        water_liters / 1000

    )


    # STATUS

    if net_water_needed <= 0.5:

        status = "NO_IRRIGATION"

        status_bn = "আজ সেচ প্রয়োজন নেই"

        status_en = "No irrigation needed today"

    elif net_water_needed <= 3:

        status = "LOW"

        status_bn = "অল্প পরিমাণ সেচ দিন"

        status_en = "Light irrigation recommended"

    elif net_water_needed <= 7:

        status = "MEDIUM"

        status_bn = "মাঝারি পরিমাণ সেচ দিন"

        status_en = "Moderate irrigation recommended"

    else:

        status = "HIGH"

        status_bn = "বেশি পরিমাণ সেচ প্রয়োজন"

        status_en = "High irrigation requirement"


    return {

        "area_m2": area_m2,

        "crop_water_need": crop_water_need,

        "effective_rain": effective_rain,

        "available_water": available_water,

        "net_water_needed": net_water_needed,

        "gross_water_mm": gross_water_mm,

        "water_liters": water_liters,

        "water_m3": water_m3,

        "status": status,

        "status_bn": status_bn,

        "status_en": status_en

    }


# NAVIGATION

def nav():

    st.sidebar.markdown(

        """
        <div style="
        font-family:Space Grotesk;
        font-weight:700;
        font-size:1.25rem;
        color:#fff;
        padding:.2rem 0 1rem 0
        ">
        🌧️ Smart Rain & Agriculture
        </div>
        """,

        unsafe_allow_html=True

    )


    pages = [

        "🏠 Home",

        "🔮 Rain Prediction",

        "🌱 Agriculture",

        "📂 Historical Data",

        "📊 Analytics",

        "ℹ️ About"

    ]


    if (

        "page"
        not in st.session_state

        or

        st.session_state.page
        not in pages

    ):

        st.session_state.page = pages[0]


    def sidebar_changed():

        st.session_state.page = (
            st.session_state.main_navigation
        )


    if (

        "main_navigation"
        not in st.session_state

        or

        st.session_state.main_navigation
        !=
        st.session_state.page

    ):

        st.session_state.main_navigation = (
            st.session_state.page
        )


    choice = st.sidebar.radio(

        "Navigation",

        pages,

        key="main_navigation",

        label_visibility="collapsed",

        on_change=sidebar_changed

    )


    return choice


def go_to_page(
    page
):

    st.session_state.page = page

    st.rerun()

# HOME

def home():

    st.markdown(

        f"""
        <div class='hero'>

        <h1>
        🌧️ Bangladesh Smart Rainfall & Agriculture System
        </h1>

        <p>
        Rainfall prediction, agricultural water calculation
        and smart irrigation recommendation system.
        </p>

        <div class='hero-stats'>

        <div class='hero-stat'>
        <div class='hero-num'>
        {len(df):,}
        </div>
        <div class='hero-label'>
        Weather Records
        </div>
        </div>

        <div class='hero-stat'>
        <div class='hero-num'>
        {df.Station_ID.nunique()}
        </div>
        <div class='hero-label'>
        Weather Stations
        </div>
        </div>

        <div class='hero-stat'>
        <div class='hero-num'>
        CatBoost
        </div>
        <div class='hero-label'>
        Rainfall Model
        </div>
        </div>

        <div class='hero-stat'>
        <div class='hero-num'>
        🌱 Smart
        </div>
        <div class='hero-label'>
        Irrigation System
        </div>
        </div>

        </div>

        </div>
        """,

        unsafe_allow_html=True

    )


    st.markdown(
        "<div class='section-title'>🚀 Quick Access</div>",
        unsafe_allow_html=True
    )


    a, b, c = st.columns(3)


    if a.button(

        "🔮 Rainfall Prediction",

        use_container_width=True,

        type="primary"

    ):

        go_to_page(
            "🔮 Rain Prediction"
        )


    if b.button(

        "🌱 Smart Agriculture",

        use_container_width=True,

        type="primary"

    ):

        go_to_page(
            "🌱 Agriculture"
        )


    if c.button(

        "📊 Analytics",

        use_container_width=True,

        type="primary"

    ):

        go_to_page(
            "📊 Analytics"
        )


    st.divider()


    left, right = st.columns(
        [1.5, 1]
    )


    with left:

        monthly = (

            df

            .assign(
                Month=df["Date"].dt.month
            )

            .groupby(
                "Month",
                as_index=False
            )["rain_sum"]

            .mean()

            .rename(
                columns={
                    "rain_sum":
                    "Average Rainfall"
                }
            )

        )


        monthly["Month Name"] = (

            pd.to_datetime(

                monthly["Month"],

                format="%m"

            )

            .dt.strftime("%b")

        )


        fig = px.area(

            monthly,

            x="Month Name",

            y="Average Rainfall",

            title="Monthly Rainfall Pattern"

        )


        fig.update_yaxes(
            title="Rainfall (mm)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with right:

        latest = (

            df
            .sort_values("Date")
            .tail(1000)

        )


        fig = px.histogram(

            latest,

            x="rain_sum",

            nbins=30,

            title="Rainfall Distribution"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# RAIN PREDICTION

def prediction_page():

    st.title(
        "🔮 Rainfall Prediction"
    )


    st.caption(
        "ম্যানুয়ালি আবহাওয়ার তথ্য দিন এবং মডেল দিয়ে আজকের বৃষ্টিপাত predict করুন।"
    )


    meta = station_table().copy()


    meta["label"] = meta.apply(

        lambda x:

        f"{x.Station}, {x.District} ({x.Division})",

        axis=1

    )


    labels = sorted(
        meta["label"].tolist()
    )


    selected_label = st.selectbox(

        "📍 Station নির্বাচন করুন / Select Station",

        labels

    )


    station = (

        meta.loc[
            meta["label"]
            ==
            selected_label
        ]

        .iloc[0]

    )


    target = pd.Timestamp(

        st.date_input(

            "📅 Prediction Date",

            value=date.today(),

            max_value=date.today()

        )

    ).normalize()


    base = (

        df[
            df["Station_ID"]
            ==
            station["Station_ID"]
        ]

        .median(
            numeric_only=True
        )

        .to_dict()

    )


    values = {}


    with st.form(
        "manual_weather"
    ):

        st.subheader(
            "🌦️ Weather Information"
        )


        c1, c2, c3, c4 = st.columns(4)


        values[
            "temperature_2m_mean"
        ] = c1.number_input(

            "Mean Temperature °C",

            value=float(
                base.get(
                    "temperature_2m_mean",
                    25
                )
            )

        )


        values[
            "temperature_2m_max"
        ] = c2.number_input(

            "Max Temperature °C",

            value=float(
                base.get(
                    "temperature_2m_max",
                    30
                )
            )

        )


        values[
            "temperature_2m_min"
        ] = c3.number_input(

            "Min Temperature °C",

            value=float(
                base.get(
                    "temperature_2m_min",
                    20
                )
            )

        )


        values[
            "apparent_temperature_mean"
        ] = c4.number_input(

            "Apparent Temperature °C",

            value=float(
                base.get(
                    "apparent_temperature_mean",
                    25
                )
            )

        )


        c1, c2, c3, c4 = st.columns(4)


        values[
            "sunshine_duration"
        ] = c1.number_input(

            "Sunshine Duration",

            value=float(
                base.get(
                    "sunshine_duration",
                    0
                )
            )

        )


        values[
            "daylight_duration"
        ] = c2.number_input(

            "Daylight Duration",

            value=float(
                base.get(
                    "daylight_duration",
                    0
                )
            )

        )


        values[
            "wind_speed_10m_max"
        ] = c3.number_input(

            "Wind Speed",

            value=float(
                base.get(
                    "wind_speed_10m_max",
                    0
                )
            )

        )


        values[
            "wind_gusts_10m_max"
        ] = c4.number_input(

            "Wind Gusts",

            value=float(
                base.get(
                    "wind_gusts_10m_max",
                    0
                )
            )

        )


        c1, c2, c3, c4 = st.columns(4)


        values[
            "wind_direction_10m_dominant"
        ] = c1.number_input(

            "Wind Direction",

            value=float(
                base.get(
                    "wind_direction_10m_dominant",
                    0
                )
            )

        )


        values[
            "shortwave_radiation_sum"
        ] = c2.number_input(

            "Shortwave Radiation",

            value=float(
                base.get(
                    "shortwave_radiation_sum",
                    0
                )
            )

        )


        values[
            "weather_code"
        ] = c3.number_input(

            "Weather Code",

            value=int(
                base.get(
                    "weather_code",
                    0
                )
            ),

            step=1

        )


        values[
            "et0_fao_evapotranspiration"
        ] = c4.number_input(

            "ET0",

            value=float(
                base.get(
                    "et0_fao_evapotranspiration",
                    0
                )
            )

        )


        submitted = st.form_submit_button(

            "🌧️ Predict Rainfall",

            type="primary",

            use_container_width=True

        )


    if submitted:

        try:

            values["Latitude"] = station["Latitude"]

            values["Longitude"] = station["Longitude"]


            set_weather_values(
                values,
                station
            )


            pred_hist, bridge_note = (

                build_prediction_history(
                    station,
                    target
                )

            )


            X = create_prediction_features(

                pred_hist,

                station["Station_ID"],

                target

            )


            pred = max(

                float(

                    np.asarray(
                        model.predict(X)
                    )

                    .reshape(-1)[0]

                ),

                0

            )


            name, msg = condition(
                weather_code,
                pred
            )


            st.session_state.rain_prediction = {

                "prediction": pred,

                "station": station,

                "date": target,

                "weather_values": values,

                "condition": name,

                "message": msg,

                "et0": et0,

                "history_note": bridge_note

            }


        except Exception as e:

            st.error(
                "Prediction failed"
            )

            st.exception(e)


    if "rain_prediction" in st.session_state:

        result = (
            st.session_state.rain_prediction
        )


        pred = result["prediction"]


        st.divider()

        st.subheader(
            "🌧️ Prediction Result"
        )


        a, b, c = st.columns(3)


        a.metric(

            "Predicted Rainfall",

            f"{pred:.2f} mm"

        )


        b.metric(

            "Weather",

            result["condition"]

        )


        c.metric(

            "ET0",

            f"{result['et0']:.2f}"

        )


        st.info(
            result["message"]
        )


        st.success(
            "🌱 এই prediction Agriculture page-এ ব্যবহার করা যাবে।"
        )

# AGRICULTURE PAGE

def agriculture_page():

    st.title(
        "🌱 Smart Agriculture & Irrigation"
    )


    st.caption(
        "ফসল, জমির পরিমাণ, মাটির ধরন, আগে থেকে থাকা পানি এবং আজকের predicted rainfall অনুযায়ী কত পানি দিতে হবে তা হিসাব করুন।"
    )


    st.markdown(
        """
        <div class='agri-card'>

        <h3>
        💧 Smart Irrigation Recommendation
        </h3>

        <p>
        এই সিস্টেম হিসাব করবে:
        ফসলের পানির প্রয়োজন +
        মাটির ধরন +
        ফসলের growth stage +
        জমির পরিমাণ +
        আগে থেকে থাকা পানি +
        আজকের predicted rainfall +
        ET0
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # WEATHER SOURCE

    st.markdown(
        "<div class='section-title'>🌦️ Weather & Rainfall Information / আবহাওয়া ও বৃষ্টি</div>",
        unsafe_allow_html=True
    )


    weather_source = st.radio(

        "Rainfall Source / বৃষ্টির তথ্যের উৎস",

        [

            "Use Rain Prediction / Rainfall Prediction ব্যবহার করুন",

            "Manual Rainfall Input / নিজে বৃষ্টির পরিমাণ দিন"

        ]

    )


    predicted_rain = 0.0

    et0_value = 0.0


    if weather_source.startswith(
        "Use Rain Prediction"
    ):

        if (
            "rain_prediction"
            in st.session_state
        ):

            rain_data = (
                st.session_state.rain_prediction
            )


            predicted_rain = (
                rain_data["prediction"]
            )


            et0_value = (
                rain_data["et0"]
            )


            st.success(

                f"""
                🌧️ Predicted Rainfall: {predicted_rain:.2f} mm

                💨 ET0: {et0_value:.2f}
                """

            )

        else:

            st.warning(
                "আগে Rain Prediction page থেকে prediction করুন অথবা Manual Rainfall নির্বাচন করুন।"
            )


            predicted_rain = st.number_input(

                "আজকের বৃষ্টির পরিমাণ / Today's Rainfall (mm)",

                min_value=0.0,

                value=0.0

            )


            et0_value = st.number_input(

                "ET0 / Evapotranspiration",

                min_value=0.0,

                value=4.0

            )


    else:

        c1, c2 = st.columns(2)


        predicted_rain = c1.number_input(

            "আজকের বৃষ্টির পরিমাণ / Today's Rainfall (mm)",

            min_value=0.0,

            value=0.0,

            step=0.5

        )


        et0_value = c2.number_input(

            "ET0 / Evapotranspiration",

            min_value=0.0,

            value=4.0,

            step=0.1

        )

    # LAND

    st.markdown(
        "<div class='section-title'>📐 Land Information / জমির তথ্য</div>",
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    land_area = c1.number_input(

        "জমির পরিমাণ / Land Area",

        min_value=0.01,

        value=1.0,

        step=0.01

    )


    area_unit = c2.selectbox(

        "জমির একক / Area Unit",

        [

            "শতক / Decimal",

            "একর / Acre",

            "হেক্টর / Hectare",

            "বর্গমিটার / Square Meter"

        ]

    )

    # CROP

    st.markdown(
        "<div class='section-title'>🌾 Crop Information / ফসলের তথ্য</div>",
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    crop_name = c1.selectbox(

        "ফসল নির্বাচন করুন / Select Crop",

        list(
            CROPS.keys()
        )

    )


    crop_stage = c2.selectbox(

        "ফসলের অবস্থা / Crop Growth Stage",

        list(

            CROPS[crop_name][
                "stage_factor"
            ].keys()

        )

    )


    st.info(
        CROPS[crop_name]["description"]
    )

    # SOIL

    st.markdown(
        "<div class='section-title'>🟫 Soil Information / মাটির তথ্য</div>",
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    soil_type = c1.selectbox(

        "মাটির ধরন / Soil Type",

        list(
            SOIL_TYPES.keys()
        )

    )


    existing_water = c2.number_input(

        "আগে থেকে থাকা পানি / Existing Water (mm)",

        min_value=0.0,

        value=0.0,

        step=0.5

    )


    st.caption(
        SOIL_TYPES[soil_type][
            "description"
        ]
    )

    # IRRIGATION

    st.markdown(
        "<div class='section-title'>🚿 Irrigation System / সেচ ব্যবস্থা</div>",
        unsafe_allow_html=True
    )


    irrigation_method = st.selectbox(

        "সেচ পদ্ধতি / Irrigation Method",

        [

            "সাধারণ সেচ / Traditional Irrigation",

            "স্প্রিংকলার / Sprinkler",

            "ড্রিপ / Drip Irrigation"

        ]

    )


    if irrigation_method.startswith(
        "সাধারণ"
    ):

        default_efficiency = 60.0

    elif irrigation_method.startswith(
        "স্প্রিংকলার"
    ):

        default_efficiency = 75.0

    else:

        default_efficiency = 90.0


    irrigation_efficiency = st.slider(

        "সেচ দক্ষতা / Irrigation Efficiency (%)",

        min_value=30,

        max_value=100,

        value=int(default_efficiency)

    )

    # CALCULATE

    if st.button(

        "💧 Calculate Smart Irrigation / সেচ হিসাব করুন",

        type="primary",

        use_container_width=True

    ):


        result = calculate_irrigation(

            land_area=land_area,

            area_unit=area_unit,

            crop_name=crop_name,

            crop_stage=crop_stage,

            soil_type=soil_type,

            existing_water_mm=existing_water,

            predicted_rain_mm=predicted_rain,

            et0_value=et0_value,

            irrigation_efficiency=irrigation_efficiency

        )


        st.session_state.agri_result = {

            "result": result,

            "crop_name": crop_name,

            "crop_stage": crop_stage,

            "soil_type": soil_type,

            "predicted_rain": predicted_rain,

            "existing_water": existing_water,

            "et0": et0_value,

            "land_area": land_area,

            "area_unit": area_unit,

            "irrigation_method": irrigation_method,

            "efficiency": irrigation_efficiency

        }


    # RESULT

    if "agri_result" in st.session_state:

        data = (
            st.session_state.agri_result
        )

        result = data["result"]


        st.divider()


        st.subheader(
            "🌱 Smart Irrigation Result / স্মার্ট সেচের ফলাফল"
        )


        st.markdown(

            f"""
            <div class='result-card'>

            <h2>
            {result['status_bn']}
            </h2>

            <h3>
            {result['status_en']}
            </h3>

            </div>
            """,

            unsafe_allow_html=True

        )


        a, b, c, d = st.columns(4)


        a.metric(

            "ফসলের পানির প্রয়োজন / Crop Need",

            f"{result['crop_water_need']:.2f} mm"

        )


        b.metric(

            "কার্যকর বৃষ্টি / Effective Rain",

            f"{result['effective_rain']:.2f} mm"

        )


        c.metric(

            "নেট প্রয়োজন / Net Water Need",

            f"{result['net_water_needed']:.2f} mm"

        )


        d.metric(

            "সেচের পানি / Irrigation Water",

            f"{result['gross_water_mm']:.2f} mm"

        )


        st.markdown(
            "<div class='section-title'>💧 কত পানি দিতে হবে / How Much Water?</div>",
            unsafe_allow_html=True
        )


        a, b, c = st.columns(3)


        a.metric(

            "লিটার / Liters",

            f"{result['water_liters']:,.0f} L"

        )


        b.metric(

            "কিউবিক মিটার / Cubic Meter",

            f"{result['water_m3']:,.2f} m³"

        )


        c.metric(

            "জমির আয়তন / Land Area",

            f"{result['area_m2']:,.0f} m²"

        )


        # RECOMMENDATION

        st.markdown(
            "<div class='section-title'>🧠 Smart Recommendation / স্মার্ট পরামর্শ</div>",
            unsafe_allow_html=True
        )


        recommendations = []


        if result["status"] == "NO_IRRIGATION":

            recommendations.append(
                "✅ আজ অতিরিক্ত সেচ দেওয়ার প্রয়োজন নেই।"
            )

            recommendations.append(
                "🌧️ আগে থেকে থাকা পানি এবং predicted rainfall ফসলের প্রয়োজন মেটাতে যথেষ্ট।"
            )


        elif result["status"] == "LOW":

            recommendations.append(
                "💧 অল্প পরিমাণে সেচ দিন।"
            )


        elif result["status"] == "MEDIUM":

            recommendations.append(
                "💧 মাঝারি পরিমাণে সেচ দেওয়া ভালো হবে।"
            )


        else:

            recommendations.append(
                "⚠️ আজ ফসলের পানির চাহিদা বেশি। পর্যাপ্ত সেচ দিন।"
            )


        if predicted_rain >= 20:

            recommendations.append(
                "🌧️ আজ বেশি বৃষ্টির পূর্বাভাস আছে। সেচ দেওয়ার আগে বৃষ্টির পরিস্থিতি বিবেচনা করুন।"
            )


        if existing_water >= result["crop_water_need"]:

            recommendations.append(
                "💦 জমিতে আগে থেকেই পর্যাপ্ত পানি আছে। অতিরিক্ত পানি দেওয়া ক্ষতিকর হতে পারে।"
            )


        if data["soil_type"].startswith(
            "বেলে"
        ):

            recommendations.append(
                "🟫 বেলে মাটিতে পানি দ্রুত নিচে চলে যায়। একবারে বেশি না দিয়ে প্রয়োজন হলে ভাগ করে সেচ দিন।"
            )


        if data["soil_type"].startswith(
            "এঁটেল"
        ):

            recommendations.append(
                "🟫 এঁটেল মাটি পানি ধরে রাখে। পানি জমে আছে কিনা পরীক্ষা করুন।"
            )


        if data["irrigation_method"].startswith(
            "ড্রিপ"
        ):

            recommendations.append(
                "🚿 ড্রিপ সেচ পানি সাশ্রয়ে কার্যকর হতে পারে।"
            )


        for rec in recommendations:

            st.write(
                rec
            )

        # WATER BALANCE

        st.markdown(
            "<div class='section-title'>📊 Water Balance / পানির হিসাব</div>",
            unsafe_allow_html=True
        )


        chart_df = pd.DataFrame({

            "Category": [

                "Crop Water Need",

                "Existing Water",

                "Effective Rain",

                "Irrigation Needed"

            ],

            "Water (mm)": [

                result["crop_water_need"],

                data["existing_water"],

                result["effective_rain"],

                result["gross_water_mm"]

            ]

        })


        fig = px.bar(

            chart_df,

            x="Category",

            y="Water (mm)",

            title="Agricultural Water Balance"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # SUMMARY

        st.markdown(
            "<div class='section-title'>📋 Summary / সারসংক্ষেপ</div>",
            unsafe_allow_html=True
        )


        summary_df = pd.DataFrame({

            "বিষয় / Item": [

                "ফসল / Crop",

                "Growth Stage",

                "Soil Type",

                "Predicted Rainfall",

                "Existing Water",

                "ET0",

                "Water Required",

                "Irrigation Required"

            ],

            "মান / Value": [

                data["crop_name"],

                data["crop_stage"],

                data["soil_type"],

                f"{data['predicted_rain']:.2f} mm",

                f"{data['existing_water']:.2f} mm",

                f"{data['et0']:.2f}",

                f"{result['crop_water_need']:.2f} mm",

                f"{result['water_liters']:,.0f} Liters"

            ]

        })


        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )

# HISTORICAL DATA

def data_page():

    st.title(
        "📂 Historical Weather Dataset"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Records",
        f"{len(df):,}"
    )


    c2.metric(
        "Stations",
        df.Station_ID.nunique()
    )


    c3.metric(

        "Period",

        f"{df.Date.min().date()} → "
        f"{df.Date.max().date()}"

    )


    s1, s2, s3 = st.columns(3)


    station = s1.selectbox(

        "Station",

        ["All"]
        +
        sorted(
            df.Station.astype(str).unique()
        )

    )


    division = s2.selectbox(

        "Division",

        ["All"]
        +
        sorted(
            df.Division.astype(str).unique()
        )

    )


    dates = s3.date_input(

        "Date Range",

        value=(

            df.Date.min().date(),

            df.Date.max().date()

        )

    )


    x = df.copy()


    if station != "All":

        x = x[
            x.Station.astype(str)
            ==
            station
        ]


    if division != "All":

        x = x[
            x.Division.astype(str)
            ==
            division
        ]


    if (

        isinstance(
            dates,
            tuple
        )

        and

        len(dates) == 2

    ):

        x = x[

            (x.Date >= pd.Timestamp(dates[0]))

            &

            (x.Date <= pd.Timestamp(dates[1]))

        ]


    st.dataframe(

        x,

        use_container_width=True,

        height=480

    )


    st.download_button(

        "⬇️ Download Filtered CSV",

        x.to_csv(
            index=False
        ).encode(),

        "filtered_weather_data.csv",

        "text/csv"

    )
# ANALYTICS

def analytics_page():

    st.title(
        "📊 Advanced Analytics"
    )


    stations = sorted(
        df.Station.astype(str).unique()
    )


    sel = st.selectbox(

        "Station for detailed analytics",

        ["All"]
        +
        stations

    )


    if sel == "All":

        x = df.copy()

    else:

        x = df[
            df.Station.astype(str)
            ==
            sel
        ].copy()


    if x.empty:

        st.warning(
            "No data available."
        )

        return


    monthly = (

        x

        .assign(
            Month=x["Date"].dt.month
        )

        .groupby(
            "Month",
            as_index=False
        )["rain_sum"]

        .mean()

        .rename(
            columns={
                "rain_sum":
                "Average Rainfall"
            }
        )

    )


    monthly["Month Name"] = (

        pd.to_datetime(

            monthly["Month"],

            format="%m"

        )

        .dt.strftime("%b")

    )


    fig = px.bar(

        monthly,

        x="Month Name",

        y="Average Rainfall",

        title="Monthly Average Rainfall"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    a, b = st.columns(2)


    with a:

        fig = px.line(

            x
            .sort_values("Date")
            .tail(1000),

            x="Date",

            y="rain_sum",

            title="Historical Rainfall Trend"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    sample = x.sample(

        min(
            3000,
            len(x)
        ),

        random_state=42

    )


    with b:

        fig = px.scatter(

            sample,

            x="temperature_2m_mean",

            y="rain_sum",

            title="Temperature vs Rainfall"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    a, b = st.columns(2)


    with a:

        fig = px.scatter(

            sample,

            x="wind_speed_10m_max",

            y="rain_sum",

            title="Wind Speed vs Rainfall"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with b:

        fig = px.histogram(

            x,

            x="rain_sum",

            nbins=50,

            title="Rainfall Distribution"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    station_avg = (

        df

        .groupby(
            "Station",
            as_index=False
        )["rain_sum"]

        .mean()

        .sort_values(
            "rain_sum",
            ascending=False
        )

        .head(20)

    )


    fig = px.bar(

        station_avg,

        x="Station",

        y="rain_sum",

        title="Top 20 Stations by Average Rainfall"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )
# ABOUT

def about_page():

    st.title(
        "ℹ️ About System"
    )


    st.markdown("""

    ### 🌧️ Bangladesh Rainfall Prediction System

    **Model:** CatBoost Regression

    **Prediction Target:** Daily Rainfall (mm)

    **Features:** Weather, Calendar, Lag, Rolling & Station Features


    ### 🌱 Smart Agriculture System

    এই অংশে ব্যবহারকারী জানতে পারবেন:

    - 🌾 কোন ফসল কত পানি চায়
    - 📐 জমির পরিমাণ অনুযায়ী মোট পানি
    - 🌧️ predicted rainfall অনুযায়ী সেচ কমবে কিনা
    - 💧 আগে থেকে থাকা পানি বিবেচনা
    - 🟫 মাটির ধরন অনুযায়ী পানি
    - 🌱 crop growth stage অনুযায়ী পানি
    - 💨 ET0 অনুযায়ী পানির চাহিদা
    - 🚿 irrigation efficiency অনুযায়ী সেচ


    ### 👨‍💻 Developed By

    **Shams, Tasrif & Jishan**

    """)
# QUICK NAV

def quick_nav():

    st.divider()


    cols = st.columns(4)


    pages = [

        (
            "🏠 Home",
            "🏠 Home"
        ),

        (
            "🔮 Prediction",
            "🔮 Rain Prediction"
        ),

        (
            "🌱 Agriculture",
            "🌱 Agriculture"
        ),

        (
            "📊 Analytics",
            "📊 Analytics"
        )

    ]


    for col, (

        text,
        page

    ) in zip(
        cols,
        pages
    ):

        if col.button(

            text,

            use_container_width=True,

            key=f"quick_{page}"

        ):

            go_to_page(
                page
            )

# APP ROUTING

page = nav()


if page == "🏠 Home":

    home()


elif page == "🔮 Rain Prediction":

    prediction_page()


elif page == "🌱 Agriculture":

    agriculture_page()


elif page == "📂 Historical Data":

    data_page()


elif page == "📊 Analytics":

    analytics_page()


else:

    about_page()


quick_nav()


st.markdown(

    """
    <div class='footer'>

    <b>
    🌧️ Bangladesh Smart Rainfall & Agriculture System
    </b>

    <br>

    🌱 Rain Prediction • Smart Irrigation • Agriculture

    <br>

    Made by
    <b>
    Shams, Tasrif & Jishan
    </b>

    </div>
    """,

    unsafe_allow_html=True

)