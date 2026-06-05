"""
app.py — Main Streamlit Dashboard
☀️ Solar Activity Analysis Dashboard
Dataset: SN_d_tot_V2_0.csv — SILSO Daily Sunspot Numbers (1818–2026)
SAP ID: 70177688
"""

import streamlit as st
import pandas as pd
import numpy as np

from filters import load_data, build_sidebar_filters, apply_filters
from charts import (
    chart_pie, chart_histogram, chart_line, chart_bar,
    chart_scatter, chart_box, chart_heatmap, chart_area,
    chart_count, chart_violin,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="☀️ Solar Activity Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0F1923; color: #F0E6D3; }
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #162030; }
    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #1a2a3a, #162030);
        border: 1px solid #263248;
        border-radius: 12px;
        padding: 18px 22px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #F5A623; }
    .kpi-label { font-size: 0.85rem; color: #9EB3CC; margin-top: 4px; }
    /* Section header */
    .section-header {
        background: linear-gradient(90deg, #E8450A22, transparent);
        border-left: 4px solid #E8450A;
        padding: 8px 16px;
        border-radius: 0 8px 8px 0;
        margin: 24px 0 12px 0;
        color: #F0E6D3;
        font-size: 1.1rem;
        font-weight: 600;
    }
    /* Streamlit widget label */
    label { color: #9EB3CC !important; }
    .stSelectbox > div, .stMultiSelect > div { background-color: #162030; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
df_raw = load_data("data/SN_d_tot_V2_0.csv")

# ── Sidebar filters ───────────────────────────────────────────────────────────
filters = build_sidebar_filters(df_raw)
df = apply_filters(df_raw, filters)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 10px 0 20px 0;'>
    <h1 style='color:#F5A623; font-size:2.4rem; margin-bottom:4px;'>
        ☀️ Solar Activity Analysis Dashboard
    </h1>
    <p style='color:#9EB3CC; font-size:1rem;'>
        200+ Years of Daily Sunspot Observations · SILSO Dataset · Royal Observatory of Belgium
    </p>
    <p style='color:#5A7A9A; font-size:0.85rem;'>SAP ID: 70177688 &nbsp;|&nbsp; Submission: 05-June-2026</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
total = len(df)
valid = df.dropna(subset=["SunspotNumber"])
avg_ss  = valid["SunspotNumber"].mean()
max_ss  = valid["SunspotNumber"].max()
max_yr  = int(valid.loc[valid["SunspotNumber"].idxmax(), "Year"])
zero_pct = (df["ActivityLevel"] == "Zero").mean() * 100

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total:,}</div><div class="kpi-label">Total Records</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{avg_ss:.1f}</div><div class="kpi-label">Avg Sunspot No.</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{int(max_ss)}</div><div class="kpi-label">Peak Daily Count</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{max_yr}</div><div class="kpi-label">Peak Activity Year</div></div>', unsafe_allow_html=True)
with c5:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{zero_pct:.1f}%</div><div class="kpi-label">Zero-Activity Days</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────

# Row 1: Trend overview
st.markdown('<div class="section-header">📈 Long-Term Trend</div>', unsafe_allow_html=True)
st.pyplot(chart_line(df), use_container_width=True)

# Row 2: Distribution pair
st.markdown('<div class="section-header">📊 Distribution Analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.pyplot(chart_histogram(df), use_container_width=True)
with col2:
    st.pyplot(chart_pie(df), use_container_width=True)

# Row 3: Monthly & Area
st.markdown('<div class="section-header">📅 Temporal Patterns</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    st.pyplot(chart_bar(df), use_container_width=True)
with col4:
    st.pyplot(chart_area(df), use_container_width=True)

# Row 4: Seasonal analysis
st.markdown('<div class="section-header">🌸 Seasonal Breakdown</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)
with col5:
    st.pyplot(chart_box(df), use_container_width=True)
with col6:
    st.pyplot(chart_violin(df), use_container_width=True)

# Row 5: Correlation & Count
st.markdown('<div class="section-header">🔗 Correlations & Counts</div>', unsafe_allow_html=True)
col7, col8 = st.columns([1, 1.3])
with col7:
    st.pyplot(chart_heatmap(df), use_container_width=True)
with col8:
    st.pyplot(chart_count(df), use_container_width=True)

# Row 6: Scatter
st.markdown('<div class="section-header">🔭 Station vs Activity</div>', unsafe_allow_html=True)
st.pyplot(chart_scatter(df), use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#263248; margin-top:40px;'>
<p style='text-align:center; color:#5A7A9A; font-size:0.8rem;'>
    ☀️ Solar Activity Analysis Dashboard · EDA Course · Instructor: Ali Hassan Sherazi · SAP ID: 70177688
</p>
""", unsafe_allow_html=True)
