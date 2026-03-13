# Operational Risk & Performance Monitoring System

## Project Overview
End-to-end operational analytics pipeline processing **10,000+ records** to monitor SLA compliance, detect performance anomalies, rank regional efficiency, and enable proactive risk management.

**Tools:** SQL (SQLite) | Python (Pandas, NumPy, Matplotlib, Seaborn) | Power BI

---

## Business Problem
Operations teams struggle to proactively detect underperformance before SLAs are breached. This project builds a monitoring system that flags anomalies, tracks rolling KPIs, and ranks teams and regions on performance.

## Key Results
| Metric | Value |
|--------|-------|
| Records Processed | 10,000+ operational logs |
| SLA Target | 60 minutes response time |
| Anomaly Detection | Z-score based flagging (>2 std dev) |
| Analysis Dimensions | Region, Team, Time, Incident Type |

## Project Structure
```
operational-risk-monitoring/
│
├── data/
│   ├── generate_data.py        # Synthetic operational data generator
│   └── operations.csv          # Generated records (after running)
│
├── sql/
│   └── operations_analysis.sql # SQL: SLA compliance, rolling avg, anomaly detection
│
├── notebooks/
│   └── operations_analysis.py  # Python: anomaly detection, KPI dashboard, export
│
├── outputs/                    # Charts and exports (after running)
│
└── README.md
```

## How to Run

### 1. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn
```

### 2. Generate the dataset
```bash
cd data
python generate_data.py
cd ..
```

### 3. Run the Python analysis
```bash
cd notebooks
python operations_analysis.py
```

### 4. Run SQL queries
```bash
sqlite3 data/operations.db < sql/operations_analysis.sql
```

## Analysis Highlights

### SLA Compliance Monitoring
- SLA target: 60 minutes response time
- Breach rate calculated per region and team
- Monthly trend tracked to identify deteriorating performance

### Rolling Performance Averages
- 7-day rolling average of response times using SQL `ROWS BETWEEN` window clause
- Smooths daily noise to reveal true performance trends

### Anomaly Detection
- Z-score calculated for response time per record
- Records with |z| > 2 flagged as anomalies
- Exported to `anomalies_flagged.csv` for operational review

### Regional Performance Ranking
- All regions ranked by average efficiency score
- Efficiency score = composite of response time, downtime, and open ticket ratio

## Power BI Dashboard
Import these files from `outputs/` into Power BI:
- `monthly_ops_kpis.csv` — monthly KPI tracking (breach rate, response time, efficiency)
- `anomalies_flagged.csv` — anomaly log for drill-through reporting

**Suggested visuals:**
- KPI cards: Avg response time, SLA breach rate, avg efficiency
- Line chart: Rolling 7-day response time vs SLA target
- Bar chart: Breach rate by region
- Table: Anomaly log with drill-through

---
*Project by Phumelele Pearl Mlotshwa | Junior Data Analyst*
*GitHub: [pearl-mlotshwa](https://github.com/pearl-mlotshwa)*
