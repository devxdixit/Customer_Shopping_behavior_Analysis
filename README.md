# Customer_Shopping_behavior_Analysis
An end-to-end data analytics project exploring customer behavior using Python for ETL, SQL Server for advanced querying, and Power BI for executive-level visualization.
diff --git a/.gitignore b/.gitignore
new file mode 100644
--- /dev/null
+++ b/.gitignore
@@
+__pycache__/
+*.ipynb_checkpoints
+*.env
+data/processed/
+*.pbix
+
diff --git a/LICENSE b/LICENSE
new file mode 100644
--- /dev/null
+++ b/LICENSE
@@
+MIT License
+
+Copyright (c) 2026 Dev Dixit
+
+Permission is hereby granted, free of charge, to any person obtaining a copy
+of this software and associated documentation files (the "Software"), to deal
+in the Software without restriction.
+
diff --git a/requirements.txt b/requirements.txt
new file mode 100644
--- /dev/null
+++ b/requirements.txt
@@
+pandas
+sqlalchemy
+pyodbc
+
diff --git a/README.md b/README.md
new file mode 100644
--- /dev/null
+++ b/README.md
@@
+# Customer Shopping Behavior Analysis
+
+## 📊 Customer Behavior Dashboard
+
+This project analyzes **customer shopping patterns** and presents insights using  
+**Python, SQL Server, and Power BI**.
+
+![Dashboard](assets/dashboard.png)
+
+---
+
+## 🧠 Key Metrics
+
+- **3.9K Customers**
+- **$59.76 Avg Purchase Amount**
+- **3.75 Avg Review Rating**
+- **27% Subscription Rate**
+
+---
+
+## 📈 Insights Covered
+
+- Revenue & sales by category
+- Customer distribution by subscription status
+- Age-group based revenue and sales
+- Impact of discounts and purchase frequency
+
+---
+
+## 🛠 Tech Stack
+
+- **Python** – Data cleaning & ETL
+- **SQL Server** – Business analysis
+- **Power BI** – Interactive dashboard
+
+---
+
+## 📁 Project Structure
+
+```
+data/
+ ├── raw/
+ └── processed/
+python/
+sql/
+powerbi/
+assets/
+```
+
+---
+
+## 🚀 How to Run
+
+```bash
+pip install -r requirements.txt
+python python/etl.py
+```
+
+---
+
+## 👤 Author
+
+**Dev Dixit**  
+GitHub: https://github.com/devxdixit
+
diff --git a/python/etl.py b/python/etl.py
new file mode 100644
--- /dev/null
+++ b/python/etl.py
@@
+import pandas as pd
+
+RAW_PATH = "data/raw/customer_shopping_behavior.csv"
+PROCESSED_PATH = "data/processed/customer_shopping_behavior_clean.csv"
+
+def load_data():
+    return pd.read_csv(RAW_PATH)
+
+def clean_data(df):
+    df['Review Rating'] = df.groupby('Category')['Review Rating'] \
+        .transform(lambda x: x.fillna(x.median()))
+
+    df.columns = df.columns.str.lower().str.replace(' ', '_')
+    df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'}, inplace=True)
+
+    labels = ['Young Adult', 'Adult', 'Middle Aged', 'Senior']
+    df['age_group'] = pd.qcut(df['age'], 4, labels=labels)
+
+    frequency_mapping = {
+        'Weekly': 7,
+        'Bi-Weekly': 14,
+        'Fortnightly': 14,
+        'Monthly': 30,
+        'Quarterly': 90,
+        'Every 3 Months': 90,
+        'Annually': 365
+    }
+    df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
+
+    if 'promo_code_used' in df.columns:
+        df.drop('promo_code_used', axis=1, inplace=True)
+
+    return df
+
+def main():
+    df = load_data()
+    df = clean_data(df)
+    df.to_csv(PROCESSED_PATH, index=False)
+    print("ETL completed successfully.")
+
+if __name__ == "__main__":
+    main()
+
diff --git a/sql/business_queries.sql b/sql/business_queries.sql
new file mode 100644
--- /dev/null
+++ b/sql/business_queries.sql
@@
+-- Total customers
+SELECT COUNT(*) AS total_customers FROM customer;
+
+-- Revenue by category
+SELECT category, SUM(purchase_amount) AS revenue
+FROM customer
+GROUP BY category
+ORDER BY revenue DESC;
+
+-- Average review rating
+SELECT ROUND(AVG(review_rating), 2) AS avg_rating FROM customer;
+
+-- Subscription distribution
+SELECT subscription_status, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS percentage
+FROM customer
+GROUP BY subscription_status;
+
+-- Revenue by age group
+SELECT age_group, SUM(purchase_amount) AS revenue
+FROM customer
+GROUP BY age_group
+ORDER BY revenue DESC;
