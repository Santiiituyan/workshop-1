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

According to the project requirements, I implemented a **Star Schema** dimensional model. This decision was based on the following engineering principles:

### 1. Choice of Dimensional Modeling (Star Schema)
The Star Schema was chosen over a flat table to:
* **Improve Query Performance**: By separating descriptive attributes into dimensions, we reduce data redundancy and improve join efficiency for Power BI.
* **Maintainability**: Changes in technology names or candidate levels only need to be updated in one place (the dimension table) without affecting millions of rows in the fact table.

### 2. Surrogate Keys vs. Natural Keys
* **Decision**: As per the "Important" guidelines, I avoided using natural keys from the CSV as primary keys.
* **Implementation**: I generated **Surrogate Keys (SK)** for all tables (e.g., `Application_SK`, `Candidate_SK`, `Location_SK`). 
* **Reasoning**: Surrogate keys insulate the Data Warehouse from changes in the source system's business logic and improve join performance by using integer data types instead of strings.

### 3. Defining the Grain
* **Definition**: The grain of the Data Warehouse is explicitly defined as **one row per candidate application**.
* **Justification**: This is the lowest level of detail available in the source data, allowing HR to perform granular analysis on individual scores while still enabling high-level aggregations like hiring rates by country or year.

### 4. Handling Data Quality (The "Relaxed Threshold" Strategy)
* **Context**: Initial transformation rules led to significant data loss.
* **Action**: I adjusted the cleaning logic to accommodate the statistical variance of the randomly generated dataset.
* **Result**: This decision successfully increased the valid data sample from 31,524 to **37,348 records**, a critical gain for the reliability of the 13.36% Hiring Rate metric.

<img width="6920" height="3765" alt="star_schema" src="https://github.com/user-attachments/assets/1cdd7474-1e79-4941-9a82-0878093cdeb1" />

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

<img width="1163" height="650" alt="Captura de pantalla 2026-02-27 031429" src="https://github.com/user-attachments/assets/2b0f5564-cc64-486c-9ebc-28b9fc0f9fe6" />


---

## 🛠️ Technological Stack & Dependencies

The project leverages a robust Python-based data ecosystem to manage the end-to-end ETL process and the subsequent analytical layer:

### 🐍 Python Backend
* **Python 3.x**: The core engine for scripting and automation.
* **Pandas**: Utilized for high-performance data manipulation, filtering, and the complex transformation logic required to clean the 50,000 source records.
* **SQLAlchemy**: Acts as the SQL toolkit and Object-Relational Mapper (ORM), providing a standardized interface to interact with the database.
* **PyMySQL**: The database driver used to facilitate communication between Python and the MySQL server.
* **python-dotenv**: Employed for secure credential management, ensuring database passwords and hosts are handled through environmental variables for security.

### 🗄️ Data Warehouse (DW)
* **MySQL**: Selected as the Relational Data Warehouse to host the Star Schema architecture.
* **Dimensional Modeling**: Implemented using **Surrogate Keys** and an explicit **Grain** definition to comply with professional DW standards.

### 📊 Business Intelligence (BI)
* **Power BI Desktop**: The primary BI tool used to ingest the Data Warehouse tables and visualize the 6 key recruitment KPIs.
* **MySQL Connector/NET**: Version 8.0.28, specifically chosen to ensure stable connectivity and resolve "None" value errors during data ingestion.

## 🛠️ Future Improvements

* **Automated Scalability**: Migrating the local MySQL instance to a cloud-based solution like AWS RDS.
* **Predictive Analytics**: Implementing a Machine Learning model to predict candidate success based on historical interview scores.
* **Real-time Pipeline**: Integrating Airflow for workflow orchestration and automated daily refreshes.

## 🛠️ How to Run the Project

Follow these steps to replicate the ETL process and the Dashboard:

1.  **Database Setup**: Create a schema in MySQL (e.g., `etl_workshop`).
2.  **Environment Configuration**: Create a `.env` file in the root directory with your credentials:
    ```text
    DB_USER=root
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_NAME=etl_workshop
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute Pipeline**: Run the main script to process and load the data:
    ```bash
    python main.py
    ```
5.  **BI Visualization**: Open Power BI and connect to the MySQL database to view the updated dashboard.

---
