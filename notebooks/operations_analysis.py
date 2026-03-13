#!/usr/bin/env python3
"""
Operational Risk & Performance Monitoring System
Author: Phumelele Pearl Mlotshwa
Tools: Python (Pandas, NumPy, Matplotlib, Seaborn), SQLite
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

os.makedirs('outputs', exist_ok=True)
sns.set_theme(style='whitegrid')

# ── 1. Load Data ───────────────────────────────────────────────
conn = sqlite3.connect('data/operations.db')
df = pd.read_sql('SELECT * FROM operations', conn)
conn.close()

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['year_month'] = df['timestamp'].dt.to_period('M')

print("=" * 55)
print("  Operational Risk & Performance Monitoring Report")
print("=" * 55)
print(f"\nTotal records     : {len(df):,}")
print(f"SLA breach rate   : {df['sla_breached'].mean():.1%}")
print(f"Avg response time : {df['response_time_mins'].mean():.1f} mins")
print(f"Avg efficiency    : {df['efficiency_score'].mean():.1f}/100")

# ── 2. Anomaly Detection ───────────────────────────────────────
mean_rt = df['response_time_mins'].mean()
std_rt = df['response_time_mins'].std()
df['z_score'] = (df['response_time_mins'] - mean_rt) / std_rt
df['anomaly'] = df['z_score'].abs() > 2

anomalies = df[df['anomaly']]
print(f"\nAnomalies detected: {len(anomalies):,}  ({len(anomalies)/len(df):.1%} of records)")

# ── 3. Rolling 7-day Average ───────────────────────────────────
daily = df.groupby('date').agg(
    avg_response=('response_time_mins', 'mean'),
    sla_breaches=('sla_breached', 'sum'),
    avg_efficiency=('efficiency_score', 'mean')
).reset_index()
daily['rolling_7d'] = daily['avg_response'].rolling(7, min_periods=1).mean()

# ── 4. Regional Rankings ───────────────────────────────────────
regional = df.groupby('region').agg(
    avg_response=('response_time_mins', 'mean'),
    breach_rate=('sla_breached', 'mean'),
    avg_efficiency=('efficiency_score', 'mean'),
    avg_downtime=('downtime_mins', 'mean')
).sort_values('avg_efficiency', ascending=False).reset_index()
regional['rank'] = range(1, len(regional) + 1)

print("\nRegional Performance Rankings:")
for _, row in regional.iterrows():
    print(f"  #{int(row['rank'])} {row['region']:<20} Efficiency: {row['avg_efficiency']:.1f}  "
          f"SLA Breach: {row['breach_rate']:.1%}")

# ── 5. Visualisations ─────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Operational Risk & Performance Monitoring Dashboard', fontsize=15, fontweight='bold')

# 5a. Rolling response time with anomalies
sample_daily = daily.set_index('date')
axes[0, 0].plot(daily['date'], daily['avg_response'], alpha=0.4, color='#3498db', label='Daily Avg')
axes[0, 0].plot(daily['date'], daily['rolling_7d'], color='#2c3e50', linewidth=2, label='7-Day Rolling Avg')
axes[0, 0].axhline(60, color='red', linestyle='--', linewidth=1.2, label='SLA Target (60 min)')
axes[0, 0].set_title('Response Time Trend with SLA Target')
axes[0, 0].set_ylabel('Response Time (mins)')
axes[0, 0].legend()
axes[0, 0].tick_params(axis='x', rotation=30)

# 5b. SLA breach rate by region
regional.plot(x='region', y='breach_rate', kind='bar', ax=axes[0, 1],
              color='#e74c3c', edgecolor='white', legend=False)
axes[0, 1].set_title('SLA Breach Rate by Region')
axes[0, 1].set_ylabel('Breach Rate')
axes[0, 1].yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
axes[0, 1].tick_params(axis='x', rotation=20)

# 5c. Efficiency score by team
team_eff = df.groupby('team')['efficiency_score'].mean().sort_values(ascending=True)
team_eff.plot(kind='barh', ax=axes[1, 0], color='#27ae60', edgecolor='white')
axes[1, 0].set_title('Average Efficiency Score by Team')
axes[1, 0].set_xlabel('Efficiency Score (0-100)')
axes[1, 0].axvline(70, color='red', linestyle='--', linewidth=1.2, label='Target (70)')
axes[1, 0].legend()

# 5d. Incident type breakdown
inc = df['incident_type'].value_counts()
inc = inc[inc.index != 'None']
inc.plot(kind='bar', ax=axes[1, 1], color='#e67e22', edgecolor='white')
axes[1, 1].set_title('Incident Type Distribution')
axes[1, 1].set_ylabel('Occurrences')
axes[1, 1].tick_params(axis='x', rotation=20)

plt.tight_layout()
plt.savefig('outputs/operations_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nDashboard saved to outputs/operations_dashboard.png")

# ── 6. Export for Power BI ────────────────────────────────────
monthly = df.groupby('year_month').agg(
    breach_rate=('sla_breached', 'mean'),
    avg_response=('response_time_mins', 'mean'),
    avg_efficiency=('efficiency_score', 'mean'),
    total_records=('record_id', 'count')
).reset_index()
monthly['year_month'] = monthly['year_month'].astype(str)
monthly.to_csv('outputs/monthly_ops_kpis.csv', index=False)
df[df['anomaly']].to_csv('outputs/anomalies_flagged.csv', index=False)
print("Exported: monthly_ops_kpis.csv, anomalies_flagged.csv")
print("\nAnalysis complete.")
