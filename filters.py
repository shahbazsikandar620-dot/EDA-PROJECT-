"""
filters.py — Data loading & filtering logic
Solar Activity Analysis Dashboard
SAP ID: 70177688
"""

import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data
def load_data(filepath: str = "data/SN_d_tot_V2_0.csv") -> pd.DataFrame:
    """Load and clean the SILSO daily sunspot dataset."""
    df = pd.read_csv(
        filepath,
        sep=";",
        header=None,
        names=["Year", "Month", "Day", "DecimalDate",
               "SunspotNumber", "StdDev", "Observations", "Definitive"],
    )

    # Replace missing sentinels
    df["SunspotNumber"] = df["SunspotNumber"].replace(-1, np.nan)
    df["StdDev"] = df["StdDev"].replace(-1.0, np.nan)

    # Build a proper date column
    df["Date"] = pd.to_datetime(
        df[["Year", "Month", "Day"]].rename(
            columns={"Year": "year", "Month": "month", "Day": "day"}
        ),
        errors="coerce",
    )

    # Season
    df["Season"] = df["Month"].map(
        {12: "Winter", 1: "Winter", 2: "Winter",
         3: "Spring", 4: "Spring", 5: "Spring",
         6: "Summer", 7: "Summer", 8: "Summer",
         9: "Autumn", 10: "Autumn", 11: "Autumn"}
    )

    # Activity level
    def classify(n):
        if pd.isna(n):
            return "Unknown"
        if n == 0:
            return "Zero"
        if n < 30:
            return "Low"
        if n < 100:
            return "Moderate"
        return "High"

    df["ActivityLevel"] = df["SunspotNumber"].apply(classify)

    # Decade column for area chart
    df["Decade"] = (df["Year"] // 10) * 10

    return df


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply all sidebar filters and return filtered dataframe."""
    dff = df.copy()

    # Year range
    yr = filters.get("year_range")
    if yr:
        dff = dff[(dff["Year"] >= yr[0]) & (dff["Year"] <= yr[1])]

    # Season multi-select
    seasons = filters.get("seasons")
    if seasons:
        dff = dff[dff["Season"].isin(seasons)]

    # Activity level multi-select
    levels = filters.get("activity_levels")
    if levels:
        dff = dff[dff["ActivityLevel"].isin(levels)]

    # Observations range
    obs = filters.get("obs_range")
    if obs:
        dff = dff[(dff["Observations"] >= obs[0]) & (dff["Observations"] <= obs[1])]

    # Keyword search (year, month, activity)
    kw = filters.get("keyword", "").strip()
    if kw:
        mask = (
            dff["Year"].astype(str).str.contains(kw, case=False)
            | dff["Season"].str.contains(kw, case=False)
            | dff["ActivityLevel"].str.contains(kw, case=False)
        )
        dff = dff[mask]

    return dff


def build_sidebar_filters(df: pd.DataFrame) -> dict:
    """Render sidebar widgets and return a dict of filter values."""
    st.sidebar.header("🔭 Dashboard Filters")

    # Year range slider
    min_yr, max_yr = int(df["Year"].min()), int(df["Year"].max())
    year_range = st.sidebar.slider(
        "📅 Year Range",
        min_value=min_yr,
        max_value=max_yr,
        value=(min_yr, max_yr),
        step=1,
    )

    # Season multi-select
    all_seasons = ["Spring", "Summer", "Autumn", "Winter"]
    seasons = st.sidebar.multiselect(
        "🌸 Season",
        options=all_seasons,
        default=all_seasons,
    )

    # Activity level multi-select
    all_levels = ["Zero", "Low", "Moderate", "High", "Unknown"]
    activity_levels = st.sidebar.multiselect(
        "⚡ Activity Level",
        options=all_levels,
        default=["Zero", "Low", "Moderate", "High"],
    )

    # Observations range slider
    obs_min = int(df["Observations"].min())
    obs_max = int(df["Observations"].max())
    obs_range = st.sidebar.slider(
        "🔭 Observing Stations",
        min_value=obs_min,
        max_value=obs_max,
        value=(obs_min, obs_max),
        step=1,
    )

    # Keyword search
    keyword = st.sidebar.text_input("🔍 Keyword Search", placeholder="e.g. Summer, High, 1989")

    # Reset button
    if st.sidebar.button("🔄 Reset All Filters"):
        st.rerun()

    return {
        "year_range": year_range,
        "seasons": seasons,
        "activity_levels": activity_levels,
        "obs_range": obs_range,
        "keyword": keyword,
    }
