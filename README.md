---

# 📊 IT Recruitment ETL Pipeline & Data Warehouse

This repository contains a full-scale Data Engineering project designed to process, clean, and analyze recruitment data. The project transforms raw, randomly generated candidate data into a structured **Relational Data Warehouse** to drive strategic HR decision-making.

## 🎯 Project Objective

The goal was to build an automated pipeline that ingests a dataset of 50,000 candidates, applies complex business logic for data validation, and loads the refined data into a **Star Schema** to power a high-level Business Intelligence (BI) dashboard.

---

## 🏗️ Technical Architecture

### 1. Data Extraction (Extract)

* **Source**: A raw CSV file containing 50,000 records of candidate applications.
* **Method**: Python-based ingestion using the `Pandas` library for efficient data handling.

### 2. Advanced Transformation & Data Quality (Transform)

This stage involved critical engineering decisions to balance data integrity with sample size.

* **Initial Challenge**: Strict validation rules were discarding significant amounts of data due to inconsistencies in the randomly generated source file.
* **Strategic Adjustment**: I implemented a **"Relaxed Threshold"** logic. Instead of a "one-size-fits-all" filter, I adjusted validation to allow $0$ years of experience for *Trainee* and *Junior* roles while maintaining strict quality checks for *Architect* and *Lead* positions.
* **Efficiency Gain**: This adjustment salvaged **5,824 records**, increasing the valid dataset from 31,524 to **37,348 records** (an **18% increase** in usable data).

### 3. Star Schema Modeling & Loading (Load)

I designed a **Star Schema** in MySQL to ensure optimal query performance:

* **Fact Table (`fact_applications`)**: Centralizes metrics like interview scores and hiring status.
* **Dimension Tables**: `dim_candidate`, `dim_technology`, `dim_location`, and `dim_date`.

---

## 📈 Business Intelligence & KPI Analysis

The following 6 KPIs were developed to provide a 360-degree view of the recruitment process:

### Core Recruitment KPIs

1. **Hiring by Technology**: Identifies which tech stacks are attracting the most talent (e.g., *DevOps* and *Game Development*).
2. **Hiring by Year**: Tracks recruitment trends over time, showing a peak in 2020 followed by a stabilization phase.
3. **Hiring by Seniority**: Analyzes the distribution of hires across experience levels, ensuring a balanced team structure.
4. **Hiring by Country**: Focuses on strategic regions: **USA, Brazil, Colombia, and Ecuador**.

### Advanced Analytical KPIs (Extra Value)

5. **Hiring Rate % (Conversion Rate)**:
* **Formula**: $(Total Hires / Total Applicants) * 100$
* **Result**: **13.36%**. This metric measures the efficiency of the funnel and the selectivity of the process.


6. **Avg. Scores by Seniority**:
* **Metric**: Compares `Code Challenge` vs. `Technical Interview` averages.
* **Insight**: Validates if higher seniority levels actually correlate with better technical performance, ensuring the "Senior" label matches technical reality.



---

## 💻 Tech Stack

* **Language**: Python 3.x (Pandas)
* **Database**: MySQL Server
* **BI Tool**: Power BI Desktop
* **Connectivity**: MySQL Connector/NET 8.0.28 (Optimized for Power BI compatibility)

## 🛠️ Future Improvements

* **Automated Scalability**: Migrating the local MySQL instance to a cloud-based solution like AWS RDS.
* **Predictive Analytics**: Implementing a Machine Learning model to predict candidate success based on historical interview scores.
* **Real-time Pipeline**: Integrating Airflow for workflow orchestration and automated daily refreshes.

---
