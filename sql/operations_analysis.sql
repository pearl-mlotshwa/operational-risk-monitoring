-- ============================================================
-- Operational Risk & Performance Monitoring System - SQL
-- Author: Phumelele Pearl Mlotshwa
-- Tools: SQLite | Python | Power BI
-- ============================================================

-- ── 1. SLA COMPLIANCE OVERVIEW ────────────────────────────────
SELECT
    region,
    team,
    COUNT(*) AS total_records,
    SUM(sla_breached) AS sla_breaches,
    ROUND(100.0 * SUM(sla_breached) / COUNT(*), 1) AS breach_rate_pct,
    ROUND(AVG(response_time_mins), 1) AS avg_response_time,
    ROUND(AVG(efficiency_score), 1) AS avg_efficiency
FROM operations
GROUP BY region, team
ORDER BY breach_rate_pct DESC;

-- ── 2. ROLLING 7-DAY PERFORMANCE AVERAGE (Window Function) ────
SELECT
    date(timestamp) AS day,
    ROUND(AVG(response_time_mins), 1) AS daily_avg_response,
    SUM(sla_breached) AS daily_breaches,
    ROUND(AVG(AVG(response_time_mins)) OVER (
        ORDER BY date(timestamp)
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 1) AS rolling_7d_avg_response
FROM operations
GROUP BY day
ORDER BY day;

-- ── 3. REGIONAL PERFORMANCE RANKING ───────────────────────────
SELECT
    region,
    COUNT(*) AS total_records,
    ROUND(AVG(response_time_mins), 1) AS avg_response_mins,
    ROUND(AVG(efficiency_score), 1) AS avg_efficiency,
    ROUND(AVG(downtime_mins), 1) AS avg_downtime,
    RANK() OVER (ORDER BY AVG(efficiency_score) DESC) AS performance_rank
FROM operations
GROUP BY region
ORDER BY performance_rank;

-- ── 4. ANOMALY DETECTION: Response time outliers ──────────────
WITH stats AS (
    SELECT
        AVG(response_time_mins) AS mean_rt,
        AVG(response_time_mins * response_time_mins) - AVG(response_time_mins) * AVG(response_time_mins) AS variance_rt
    FROM operations
)
SELECT
    o.record_id,
    o.timestamp,
    o.region,
    o.team,
    o.response_time_mins,
    o.incident_type,
    ROUND((o.response_time_mins - s.mean_rt) / MAX(SQRT(s.variance_rt), 1), 2) AS z_score,
    CASE
        WHEN (o.response_time_mins - s.mean_rt) / MAX(SQRT(s.variance_rt), 1) > 2 THEN 'Anomaly'
        ELSE 'Normal'
    END AS anomaly_flag
FROM operations o, stats s
WHERE (o.response_time_mins - s.mean_rt) / MAX(SQRT(s.variance_rt), 1) > 2
ORDER BY o.response_time_mins DESC
LIMIT 50;

-- ── 5. INCIDENT TYPE DISTRIBUTION ─────────────────────────────
SELECT
    incident_type,
    COUNT(*) AS occurrences,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_total,
    ROUND(AVG(response_time_mins), 1) AS avg_response_time,
    ROUND(AVG(downtime_mins), 1) AS avg_downtime
FROM operations
GROUP BY incident_type
ORDER BY occurrences DESC;

-- ── 6. MONTHLY OPERATIONAL TREND ─────────────────────────────
SELECT
    strftime('%Y-%m', timestamp) AS year_month,
    COUNT(*) AS records,
    SUM(sla_breached) AS sla_breaches,
    ROUND(100.0 * SUM(sla_breached) / COUNT(*), 1) AS breach_rate_pct,
    ROUND(AVG(response_time_mins), 1) AS avg_response_mins,
    ROUND(AVG(efficiency_score), 1) AS avg_efficiency_score
FROM operations
GROUP BY year_month
ORDER BY year_month;
