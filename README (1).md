# ☀️ Solar Activity Analysis Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**SAP ID:** 70177688  
**Submission Date:** 05-June-2026  

---

## 📌 Project Overview

An interactive data visualization dashboard analyzing **200+ years of daily solar sunspot observations** (1818–2026) using the SILSO dataset provided by the Royal Observatory of Belgium. The dashboard presents 10 chart types with fully linked interactive filters.

---

## 📁 Project Structure

```
dashboard_project/
├── data/
│   └── SN_d_tot_V2_0.csv        ← Dataset (DO NOT rename)
├── notebooks/
│   └── analysis.ipynb            ← EDA notebook
├── app.py                        ← Main Streamlit dashboard
├── charts.py                     ← All 10 chart functions
├── filters.py                    ← Data loading & filter logic
├── requirements.txt              ← Python dependencies
└── README.md                     ← This file
```

---

## ⚙️ Installation & Setup

### Step 1 — Prerequisites
Make sure you have **Python 3.8+** installed.

### Step 2 — Install dependencies
Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### Step 3 — Run the dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## 📊 Dataset Description

| Column | Description |
|---|---|
| Year | Year of observation |
| Month | Month (1–12) |
| Day | Day of month |
| DecimalDate | Fractional year (e.g. 1818.001) |
| SunspotNumber | Daily international sunspot number (-1 = missing) |
| StdDev | Standard deviation of station counts |
| Observations | Number of observing stations |
| Definitive | 1 = definitive data, 0 = provisional |

**Total records:** ~76,000 daily observations  
**Missing values:** -1 sentinel replaced with NaN during cleaning

---

## 🔍 Key Insights

1. **Solar cycles (~11 years)** are clearly visible in the line chart — regular peaks and troughs in sunspot activity since 1818.
2. **Most days have low activity** — the pie and count charts show the majority of days fall in the "Zero" or "Low" category.
3. **No strong seasonal pattern** — box and violin plots show similar distributions across seasons, confirming sunspot activity is not driven by Earth's position.
4. **Strong correlation** between sunspot number and number of observing stations in modern records — more stations = more reliable counts.
5. **Activity has increased** in the 20th century compared to the 19th century, visible in the area chart's cumulative growth.

---

## 📈 Charts Included

| # | Chart Type | Insight Shown |
|---|---|---|
| 1 | Pie Chart | Activity level proportions |
| 2 | Histogram | Frequency distribution of sunspot numbers |
| 3 | Line Chart | Annual trend over 200 years |
| 4 | Bar Chart | Average sunspot by month |
| 5 | Scatter Plot | Sunspot number vs observing stations |
| 6 | Box Plot | Spread by season |
| 7 | Heatmap | Feature correlation matrix |
| 8 | Area Chart | Cumulative decade-wise activity |
| 9 | Count Plot | Days per activity level |
| 10 | Violin Plot | Density distribution by season |

---

## 🎛️ Dashboard Filters

All filters are **linked** — changing any filter updates all 10 charts simultaneously.

| Filter | Type |
|---|---|
| Year Range | Slider (date range) |
| Season | Multi-select dropdown |
| Activity Level | Multi-select dropdown |
| Observing Stations | Numerical range slider |
| Keyword Search | Text input |
| Reset | Button to clear all filters |

---

## 📦 Dependencies

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- streamlit
