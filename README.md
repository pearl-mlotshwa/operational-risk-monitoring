# Operational Risk & Performance Monitoring System

## Overview
Operational problems rarely announce themselves. By the time a business 
notices something is wrong, customers are already affected. This project 
was built to change that by creating a proactive monitoring system that 
catches performance drops and SLA breaches before they escalate.

## The Approach
I worked with 10,000+ operational records covering ticket response times, 
resolution times, SLA targets, and regional downtime data. The first 
step was calculating SLA compliance rates by region, which immediately 
revealed where the gaps were and how serious they were.

Rather than relying on overall averages which hide emerging problems, 
I calculated rolling 7-day performance averages using SQL window 
functions. A region could perform well for six months and terribly 
for the last two weeks and still look fine on an overall average. 
Rolling averages catch that shift in real time.

I then built anomaly detection logic in Python using a statistical 
threshold approach. Any response time that exceeded the rolling 7-day 
mean by more than two standard deviations was automatically flagged 
as an anomaly. The threshold adjusts dynamically as baseline performance 
changes, so it stays relevant over time without manual recalibration.

Regional performance was ranked using DENSE_RANK() in SQL across three 
metrics: SLA compliance rate, average response time, and total downtime. 
This made it immediately clear which regions were leading and which 
were struggling.

The Power BI dashboard used a RAG status system built with DAX SWITCH 
logic. Green above 95% SLA compliance, Amber between 85% and 95%, 
Red below 85%. Anyone could look at the dashboard and immediately know 
which regions needed attention without reading a single number.

## Tools Used
Python, Pandas, NumPy, SQL, Power BI, DAX

## Key Insight
Rolling averages are significantly more sensitive to emerging performance 
problems than overall averages. A monitoring system built on overall 
averages will always be too slow to catch problems before they become 
customer facing crises.

---
Built by Phumelele Pearl Mlotshwa
github.com/pearl-mlotshwa
pearlmlotshwa140@gmail.com

