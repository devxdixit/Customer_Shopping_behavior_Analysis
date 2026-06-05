# Customer_Shopping_behavior_Analysis
An end-to-end data analytics project exploring customer behavior using Python for ETL, SQL Server for advanced querying, and Power BI for executive-level visualization.

# 📊 Customer Shopping Behavior Analysis

An end-to-end data analytics project exploring customer purchasing habits. This repository demonstrates a complete data pipeline lifecycle: from raw data cleaning using Python, data warehousing and advanced querying in SQL Server, to building an executive-level interactive dashboard in Power BI.

---

## 🛠️ Tech Stack & Project Architecture
* **Data Processing & ETL:** Python (Pandas)
* **Database Pipeline:** SQLAlchemy & PyODBC
* **Data Warehouse Engine:** Microsoft SQL Server (T-SQL)
* **Business Intelligence Reporting:** Microsoft Power BI Desktop

---

## 💻 Project Workflow & Implementation

### Phase 1: ETL & Data Cleaning (Python)
The raw dataset (`customer_shopping_behavior.csv`) was processed in Python to handle missing data, fix formatting issues, and engineer features for deeper business insights:
* **Missing Value Imputation:** Fixed null values in `Review Rating` by dynamically replacing them with the median rating of their specific product category.
* **Data Normalization:** Standardized all columns into clean `snake_case` syntax and renamed complex headers (e.g., converting `purchase_amount_(usd)` to `purchase_amount`).
* **Feature Engineering:** * Binned user ages into distinct demographic groups: `Young Adult`, `Adult`, `Middle Aged`, and `Senior`.
  * Mapped string text frequencies (e.g., *Weekly*, *Fortnightly*) into clear numeric intervals (`purchase_frequency_days`).
* **Data Redundancy Cleanup:** Dropped the `promo_code_used` column after validating it was a 100% exact duplicate of the `discount_applied` field.
* **Database Migration:** Programmatically exported the final cleaned dataset into a local SQL Server instance via `sqlalchemy`.

```python
from sqlalchemy import create_engine

# Establishing connection to local MS SQL Server Staging Instance
engine = create_engine(
    r"mssql+pyodbc://@DESKTOP-OABAA6P\SQLEXPRESS/customer_behavior"
    r"?driver=ODBC+Driver+17+for+SQL+Server"
    r"&trusted_connection=yes"
)

# Uploading clean dataframe as our structural base table
df.to_sql(name='customer', con=engine, if_exists='replace', index=False)

-- Figuring out total revenue contributions across our engineered age buckets
SELECT 
    age_group,
    SUM(purchase_amount) AS total_revenue
FROM customer
GROUP BY age_group
ORDER BY total_revenue DESC;
-- Segmenting customers based on lifetime transaction depth
WITH customer_type AS (
    SELECT customer_id, previous_purchases,
    CASE 
        WHEN previous_purchases = 1 THEN 'New'
        WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
        ELSE 'Loyal'
    END AS customer_segment
    FROM customer
)
SELECT customer_segment, COUNT(*) AS "Number of Customers" 
FROM customer_type 
GROUP BY customer_segment;
├── data/
│   └── customer_shopping_behavior.csv    # Raw dataset file
├── scripts/
│   ├── customer_cleaning.py              # Python ETL automation code
│   └── analysis_queries.sql              # Cleaned SQL query script
├── dashboard/
│   └── customer_behavior_report.pbix     # Interactive Power BI report file
├── Screenshot 2026-06-05 193549.png       # Front-facing portfolio visualization
└── README.md                              # Technical documentation
