import pandas as pd
import numpy as np
import sqlite3
import os

np.random.seed(99)
n = 10000

regions = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Mpumalanga', 'Limpopo']
teams = ['Field Ops', 'Tech Support', 'Logistics', 'Customer Service', 'Infrastructure']
incident_types = ['SLA Breach', 'System Downtime', 'Response Delay', 'Equipment Fault', 'None']

dates = pd.date_range('2023-01-01', '2024-12-31', freq='h')
sampled_dates = np.random.choice(dates, n, replace=False)

response_times = np.abs(np.random.normal(45, 30, n))  # minutes
downtime = np.abs(np.random.normal(15, 20, n))         # minutes
sla_target = 60  # minutes

df = pd.DataFrame({
    'record_id': [f'OPS{str(i).zfill(6)}' for i in range(1, n+1)],
    'timestamp': sorted(sampled_dates),
    'region': np.random.choice(regions, n),
    'team': np.random.choice(teams, n),
    'response_time_mins': np.round(response_times, 1),
    'downtime_mins': np.round(downtime, 1),
    'tickets_resolved': np.random.randint(1, 20, n),
    'tickets_open': np.random.randint(0, 10, n),
})

df['sla_breached'] = (df['response_time_mins'] > sla_target).astype(int)
df['incident_type'] = np.where(
    df['response_time_mins'] > 90, 'SLA Breach',
    np.where(df['downtime_mins'] > 60, 'System Downtime',
    np.where(df['response_time_mins'] > sla_target, 'Response Delay',
    np.where(df['downtime_mins'] > 30, 'Equipment Fault', 'None'))))

df['efficiency_score'] = np.round(
    100 - (df['response_time_mins'] / sla_target * 30) -
          (df['tickets_open'] / (df['tickets_resolved'] + 1) * 20), 1
).clip(0, 100)

os.makedirs('data', exist_ok=True)
df.to_csv('data/operations.csv', index=False)

conn = sqlite3.connect('data/operations.db')
df.to_sql('operations', conn, if_exists='replace', index=False)
conn.close()

print(f"Generated {len(df):,} operational records")
print(f"SLA breach rate: {df['sla_breached'].mean():.1%}")
print(f"Avg response time: {df['response_time_mins'].mean():.1f} mins")
