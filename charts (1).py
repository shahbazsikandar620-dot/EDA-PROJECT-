"""
charts.py — All 10 chart/visualization functions
Solar Activity Analysis Dashboard
SAP ID: 70177688
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Consistent color palette ────────────────────────────────────────────────
PALETTE = {
    "primary":   "#E8450A",   # solar orange-red
    "secondary": "#F5A623",   # golden yellow
    "dark":      "#1A1A2E",   # deep navy
    "mid":       "#16213E",
    "accent":    "#0F3460",
    "light":     "#F0E6D3",
}

ACTIVITY_COLORS = {
    "Zero":     "#4A90D9",
    "Low":      "#7ED321",
    "Moderate": "#F5A623",
    "High":     "#E8450A",
    "Unknown":  "#9B9B9B",
}

SEASON_COLORS = ["#E8450A", "#F5A623", "#4A90D9", "#7ED321"]

sns.set_theme(style="darkgrid", palette="deep")

FIG_BG  = "#0F1923"
AX_BG   = "#162030"
TEXT_C  = "#F0E6D3"
GRID_C  = "#263248"


def _base_fig(w=10, h=5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(FIG_BG)
    ax.set_facecolor(AX_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_C)
    ax.tick_params(colors=TEXT_C, labelsize=9)
    ax.xaxis.label.set_color(TEXT_C)
    ax.yaxis.label.set_color(TEXT_C)
    ax.title.set_color(TEXT_C)
    ax.grid(color=GRID_C, linewidth=0.6)
    return fig, ax


# ── 1. PIE CHART ─────────────────────────────────────────────────────────────
def chart_pie(df: pd.DataFrame):
    counts = df["ActivityLevel"].value_counts()
    colors = [ACTIVITY_COLORS.get(l, "#888") for l in counts.index]
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor(FIG_BG)
    ax.set_facecolor(FIG_BG)
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        wedgeprops=dict(edgecolor=FIG_BG, linewidth=2),
    )
    for t in texts:
        t.set_color(TEXT_C)
        t.set_fontsize(10)
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(9)
        at.set_fontweight("bold")
    ax.set_title("Activity Level Distribution", color=TEXT_C, fontsize=13, pad=14)
    return fig


# ── 2. HISTOGRAM ─────────────────────────────────────────────────────────────
def chart_histogram(df: pd.DataFrame):
    data = df["SunspotNumber"].dropna()
    fig, ax = _base_fig(10, 4)
    ax.hist(data, bins=60, color=PALETTE["primary"], edgecolor=FIG_BG, alpha=0.9)
    ax.set_title("Histogram of Daily Sunspot Numbers", fontsize=13)
    ax.set_xlabel("Sunspot Number")
    ax.set_ylabel("Frequency")
    median_val = data.median()
    ax.axvline(median_val, color=PALETTE["secondary"], linewidth=1.8,
               linestyle="--", label=f"Median: {median_val:.0f}")
    ax.legend(facecolor=AX_BG, labelcolor=TEXT_C)
    return fig


# ── 3. LINE CHART ─────────────────────────────────────────────────────────────
def chart_line(df: pd.DataFrame):
    annual = (
        df.dropna(subset=["SunspotNumber"])
        .groupby("Year")["SunspotNumber"]
        .mean()
        .reset_index()
    )
    fig, ax = _base_fig(12, 4)
    ax.plot(annual["Year"], annual["SunspotNumber"],
            color=PALETTE["primary"], linewidth=1.5, alpha=0.9)
    ax.fill_between(annual["Year"], annual["SunspotNumber"],
                    alpha=0.15, color=PALETTE["primary"])
    ax.set_title("Annual Average Sunspot Number (1818–2026)", fontsize=13)
    ax.set_xlabel("Year")
    ax.set_ylabel("Avg Sunspot Number")
    return fig


# ── 4. BAR CHART ─────────────────────────────────────────────────────────────
def chart_bar(df: pd.DataFrame):
    month_avg = (
        df.dropna(subset=["SunspotNumber"])
        .groupby("Month")["SunspotNumber"]
        .mean()
        .reindex(range(1, 13))
    )
    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    fig, ax = _base_fig(10, 4)
    bars = ax.bar(month_names, month_avg.values,
                  color=PALETTE["primary"], edgecolor=FIG_BG, alpha=0.9)
    # gradient coloring
    for i, bar in enumerate(bars):
        bar.set_facecolor(plt.cm.YlOrRd(0.3 + 0.05 * i))
    ax.set_title("Average Sunspot Number by Month", fontsize=13)
    ax.set_xlabel("Month")
    ax.set_ylabel("Avg Sunspot Number")
    return fig


# ── 5. SCATTER PLOT ───────────────────────────────────────────────────────────
def chart_scatter(df: pd.DataFrame):
    sample = df.dropna(subset=["SunspotNumber", "Observations"]).sample(
        min(3000, len(df)), random_state=42
    )
    fig, ax = _base_fig(9, 5)
    sc = ax.scatter(
        sample["Observations"], sample["SunspotNumber"],
        c=sample["Year"], cmap="YlOrRd", alpha=0.5, s=12, edgecolors="none"
    )
    cbar = fig.colorbar(sc, ax=ax)
    cbar.ax.yaxis.set_tick_params(color=TEXT_C)
    cbar.ax.set_ylabel("Year", color=TEXT_C)
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color=TEXT_C)
    ax.set_title("Sunspot Number vs Observing Stations", fontsize=13)
    ax.set_xlabel("Number of Observing Stations")
    ax.set_ylabel("Sunspot Number")
    return fig


# ── 6. BOX PLOT ───────────────────────────────────────────────────────────────
def chart_box(df: pd.DataFrame):
    order = ["Spring", "Summer", "Autumn", "Winter"]
    valid = df.dropna(subset=["SunspotNumber"])
    fig, ax = _base_fig(9, 5)
    data_by_season = [valid[valid["Season"] == s]["SunspotNumber"].values for s in order]
    bp = ax.boxplot(
        data_by_season, labels=order, patch_artist=True,
        medianprops=dict(color=PALETTE["secondary"], linewidth=2),
        whiskerprops=dict(color=TEXT_C), capprops=dict(color=TEXT_C),
        flierprops=dict(marker="o", markersize=2, alpha=0.3, color=PALETTE["primary"])
    )
    for patch, color in zip(bp["boxes"], SEASON_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_title("Sunspot Number Distribution by Season", fontsize=13)
    ax.set_xlabel("Season")
    ax.set_ylabel("Sunspot Number")
    return fig


# ── 7. HEATMAP ────────────────────────────────────────────────────────────────
def chart_heatmap(df: pd.DataFrame):
    cols = ["SunspotNumber", "StdDev", "Observations", "Year", "Month"]
    corr = df[cols].dropna().corr()
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor(FIG_BG)
    ax.set_facecolor(AX_BG)
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="RdYlGn",
        ax=ax, linewidths=0.5, linecolor=FIG_BG,
        annot_kws={"size": 10, "color": "black"}
    )
    ax.set_title("Feature Correlation Matrix", color=TEXT_C, fontsize=13, pad=10)
    ax.tick_params(colors=TEXT_C)
    return fig


# ── 8. AREA CHART ─────────────────────────────────────────────────────────────
def chart_area(df: pd.DataFrame):
    decade_avg = (
        df.dropna(subset=["SunspotNumber"])
        .groupby("Decade")["SunspotNumber"]
        .mean()
        .reset_index()
    )
    fig, ax = _base_fig(11, 4)
    ax.fill_between(decade_avg["Decade"], decade_avg["SunspotNumber"],
                    alpha=0.5, color=PALETTE["primary"])
    ax.plot(decade_avg["Decade"], decade_avg["SunspotNumber"],
            color=PALETTE["secondary"], linewidth=2, marker="o", markersize=5)
    ax.set_title("Decade-Wise Average Sunspot Activity (Area Chart)", fontsize=13)
    ax.set_xlabel("Decade")
    ax.set_ylabel("Avg Sunspot Number")
    return fig


# ── 9. COUNT PLOT ─────────────────────────────────────────────────────────────
def chart_count(df: pd.DataFrame):
    order = ["Zero", "Low", "Moderate", "High", "Unknown"]
    counts = df["ActivityLevel"].value_counts().reindex(order).fillna(0)
    colors = [ACTIVITY_COLORS[l] for l in order]
    fig, ax = _base_fig(9, 4)
    bars = ax.bar(order, counts.values, color=colors, edgecolor=FIG_BG, alpha=0.9)
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
                f"{int(val):,}", ha="center", va="bottom", color=TEXT_C, fontsize=9)
    ax.set_title("Number of Days per Activity Level", fontsize=13)
    ax.set_xlabel("Activity Level")
    ax.set_ylabel("Day Count")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    return fig


# ── 10. VIOLIN PLOT ───────────────────────────────────────────────────────────
def chart_violin(df: pd.DataFrame):
    order = ["Spring", "Summer", "Autumn", "Winter"]
    valid = df.dropna(subset=["SunspotNumber"])
    fig, ax = _base_fig(10, 5)
    vp = ax.violinplot(
        [valid[valid["Season"] == s]["SunspotNumber"].values for s in order],
        positions=range(len(order)),
        showmedians=True,
        showextrema=True,
    )
    for i, (body, color) in enumerate(zip(vp["bodies"], SEASON_COLORS)):
        body.set_facecolor(color)
        body.set_alpha(0.7)
    vp["cmedians"].set_color(PALETTE["secondary"])
    vp["cmaxes"].set_color(TEXT_C)
    vp["cmins"].set_color(TEXT_C)
    vp["cbars"].set_color(TEXT_C)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, color=TEXT_C)
    ax.set_title("Sunspot Number Density by Season (Violin Plot)", fontsize=13)
    ax.set_xlabel("Season")
    ax.set_ylabel("Sunspot Number")
    return fig
