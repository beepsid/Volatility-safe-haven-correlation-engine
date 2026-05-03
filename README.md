# Market Volatility and Safe-Haven Correlation Engine

A end-to-end financial data pipeline that analyzes the relationship between Nifty 50 equity volatility and Gold ETF performance during market stress periods. Built to demonstrate a full data engineering workflow: Python extraction, SQL modeling, and Power BI visualization.

---

## Business Case

A core question in portfolio risk management is whether gold acts as a reliable safe haven when equity markets drop. This project quantifies that relationship using 5 years of daily market data, engineers financial features from raw prices, and surfaces the findings through an interactive dashboard.

The central hypothesis: on days when Nifty 50 drops more than 1.5%, does gold tend to hold or gain value?

---

## Project Architecture

```
yfinance API
    |
    v
Python Pipeline (feature engineering)
    |
    v
CSV / PostgreSQL (market_data table)
    |
    v
Power BI Dashboard (correlation analysis)
```

---

## Tech Stack

- Python 3.13 (yfinance, pandas, numpy)
- PostgreSQL (optional, CSV works directly)
- Power BI Desktop
- SQL (window functions, views)

---

## Phase 1: Python Data Pipeline

**Script:** `script/data_pipeline.py`

Pulls 5 years of daily data for:
- Nifty 50 Index (`^NSEI`)
- GOLDBEES ETF (`GOLDBEES.NS`) as the gold proxy

Engineered features:

| Feature | Description |
|---|---|
| `nifty_return` | Daily percentage return of Nifty 50 |
| `gold_return` | Daily percentage return of Gold ETF |
| `nifty_vol_30d` | 30-day rolling standard deviation of Nifty returns |
| `nifty_rsi_14` | 14-day Relative Strength Index |
| `high_vol_flag` | True if Nifty daily return <= -1.5% |
| `gold_on_crash_days` | Gold return on flagged crash days, NaN otherwise |

**Run the pipeline:**

```bash
pip install yfinance pandas numpy
python script/data_pipeline.py
```

Output is saved to `data/market_data.csv`.

---

## Phase 2: SQL Database Architecture

**Scripts:** `sql/`

### Table

```sql
-- sql/create_table.sql
CREATE TABLE market_data (
    trade_date DATE PRIMARY KEY,
    ...
);
CREATE INDEX idx_trade_date ON market_data(trade_date);
```

### Views

**`vw_moving_averages`** (`sql/view_moving_averages.sql`)
Uses `AVG() OVER()` window functions to compute 50-day and 200-day moving averages and classify each day as a Golden Cross or Death Cross signal.

**`vw_gold_price_during_crash`** (`sql/view_gold_crash.sql`)
Aggregates average gold return week-by-week, filtered strictly to high volatility days.

**`sql/advanced_analysis.sql`** includes:
- Overall vs crash-period correlation between Nifty and Gold returns
- Volatility bucket segmentation (low / medium / high)
- Monthly trend aggregation

---

## Phase 3: Power BI Dashboard

**File:** `dashboard/PowerBI_Dashboard.pbix`

### Dashboard Layout

- KPI cards: avg gold return, avg Nifty return, crash day count, avg gold return on crash days
- Market Trend by Month: dual-axis line chart of average Nifty price and 30-day rolling volatility
- Golden Cross / Death Cross: continuous MA-50 vs MA-200 line chart by trade date, with signal indicator cards. The MA-50 crossing above MA-200 in mid-2023 is clearly visible as a Golden Cross, with a potential Death Cross forming in 2026
- Crash Day Scatter: Nifty return vs Gold return filtered to high volatility days, with date range slicer and high_vol_flag filter
- Avg gold and nifty by month: inverse correlation line chart showing safe-haven behavior
- Volatility vs Gold by Year: dual-axis trend of volatility and gold returns
- Crash Days Gold Behavior per Year: bar chart of gold return on crash days aggregated by year

### Screenshots

**Full Dashboard**
![Power BI Dashboard](screenshots/powerbi%20dashboard.png)

**Moving Averages (Golden Cross / Death Cross)**
![Moving Averages](screenshots/moving%20averages.png)

**Gold Return During Market Crashes**
![Gold Return During Crash](screenshots/gold%20return%20during%20crash.png)

**Advanced SQL Analysis**
![Analysis Query](screenshots/analysis%20query.png)

---

## Key Findings

- Gold showed positive or flat returns on the majority of Nifty crash days (daily drop > 1.5%)
- The inverse correlation between Nifty and Gold returns is stronger during high volatility periods than during normal market conditions
- The 30-day rolling volatility spikes align with known market stress events visible in the trend chart

---

## How to Run Locally

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install yfinance pandas numpy
   ```
3. Run the pipeline:
   ```bash
   python script/data_pipeline.py
   ```
4. Load `data/market_data.csv` into Power BI via Get Data > Text/CSV
5. Open `dashboard/PowerBI_Dashboard.pbix`

To use with PostgreSQL, run `sql/create_table.sql` first, then load the CSV into the table using your preferred method (pgAdmin, COPY command, etc.).

---

## Project Structure

```
.
├── script/
│   └── data_pipeline.py       # Python extraction and feature engineering
├── sql/
│   ├── create_table.sql        # Table schema and index
│   ├── view_moving_averages.sql
│   ├── view_gold_crash.sql
│   └── advanced_analysis.sql
├── data/
│   └── market_data.csv         
├── dashboard/
│   └── PowerBI_Dashboard.pbix
├── screenshots/
│   ├── powerbi dashboard.png
│   ├── moving averages.png
│   ├── gold return during crash.png
│   └── analysis query.png
└── README.md
```

---

## Author

Built as a portfolio project to demonstrate end-to-end financial data engineering skills across Python, SQL, and BI tooling.
