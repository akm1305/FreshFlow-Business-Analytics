
# FreshFlow Juice Company – Business Analytics Project

## 1. Project Overview

This project analyses FreshFlow Juice Company's sales and daily inventory data using Python and NumPy.

The project focuses on data auditing, data cleaning, business metric calculations, statistical analysis, outlet and product performance, daily trends, discount analysis, anomaly detection, scenario analysis, validation, and business recommendations.

The analysis covers 30 days, three outlets, and eight products.

## 2. Project Objectives

- Identify data quality issues in the sales dataset.
- Remove duplicate and invalid records.
- Correct product and category mismatches.
- Generate daily inventory and operations data.
- Calculate revenue, discounts, costs, profit, and gross margin.
- Analyse outlet-wise and product-wise performance.
- Study daily revenue trends.
- Investigate discount strategies.
- Detect unusual transactions and anomalies.
- Perform business scenario analysis.
- Validate calculations and generate a final report.

## 3. Technologies Used

- Python 3
- NumPy
- PyCharm IDE

## 4. Project Folder Structure

```text
FreshFlow/
│
├── datasets/
│   ├── freshflow_sales.csv
│   ├── freshflow_sales_cleaned.csv
│   ├── freshflow_cleaned.csv
│   ├── freshflow_daily_operations.csv
│   ├── freshflow_operations_cleaned.csv
│   ├── freshflow_metrics.csv
│   ├── freshflow_daily_trends.csv
│   ├── freshflow_discount_analysis.csv
│   ├── freshflow_anomaly_register.csv
│   ├── freshflow_scenario_analysis.csv
│   └── retail_inventory_dataset.csv
│
├── Src/
│   ├── generate_operations.py
│   ├── data_dictionary.py
│   ├── data_audit.py
│   ├── data_cleaning.py
│   ├── metric_calculations.py
│   ├── statistical_analysis.py
│   ├── trend_anomaly_analysis.py
│   ├── discount_analysis.py
│   ├── anomaly_register.py
│   ├── scenario_analysis.py
│   ├── validation_tests.py
│   ├── final_report.py
│   ├── run_all.py
│   ├── inventory.py
│   └── main.py
│
├── data_generation_log.txt
├── freshflow_final_report.txt
├── Recommendation.txt
└── README.md
```

## 5. Dataset Information

### Sales Dataset

- File: `freshflow_sales.csv`
- Original records: 5,000
- Contains transaction, outlet, product, quantity, price, cost, discount, stock, payment, and customer-rating information.

### Daily Operations Dataset

- File: `freshflow_daily_operations.csv`
- Generated using Python and NumPy.
- Contains 720 records.
- Covers 30 days, three outlets, and eight products.
- Includes opening stock, stock received, units sold, waste, and closing stock.

### Inventory Calculation

Closing stock is calculated using:

```text
Closing Stock = Opening Stock + Stock Received - Units Sold - Waste Units
```

## 6. Data Cleaning

The data cleaning process includes:

- Removing duplicate transaction IDs.
- Removing invalid sales records.
- Correcting product/category mismatches.
- Handling missing customer ratings.
- Validating numerical values and ranges.
- Checking inventory calculations.

## 7. Business Metrics

The project calculates the following metrics:

- Gross Sales
- Discount Amount
- Net Revenue
- Cost of Goods Sold (COGS)
- Gross Profit
- Gross Margin
- Average Selling Price (ASP)

## 8. How to Run the Project

Follow these steps to execute the project:

1. Open the FreshFlow project in PyCharm.
2. Make sure Python is installed and configured.
3. Install NumPy if required:

```bash
pip install numpy
```

4. Verify that the `datasets` and `Src` folders exist.
5. Make sure `freshflow_sales.csv` is inside the `datasets` folder.
6. Open `Src/run_all.py`.
7. Right-click and select Run.
8. Wait for all project scripts to execute.

Successful execution displays:

```text
ALL PROJECT SCRIPTS EXECUTED SUCCESSFULLY!
FRESHFLOW BUSINESS ANALYTICS PROJECT COMPLETED!
Process finished with exit code 0
```

## 9. Script Execution Order

The main execution file runs the following scripts:

1. `generate_operations.py` – Generates daily operations data.
2. `data_dictionary.py` – Displays dataset information.
3. `data_audit.py` – Performs data quality auditing.
4. `data_cleaning.py` – Cleans the datasets.
5. `metric_calculations.py` – Calculates business metrics.
6. `statistical_analysis.py` – Performs statistical analysis.
7. `trend_anomaly_analysis.py` – Analyses trends and anomalies.
8. `discount_analysis.py` – Analyses discount performance.
9. `anomaly_register.py` – Generates an anomaly register.
10. `scenario_analysis.py` – Performs business scenario analysis.
11. `validation_tests.py` – Validates calculations and datasets.
12. `final_report.py` – Generates the final business report.

## 10. Main Project Results

The latest successful execution produced the following results:

| Metric | Result |
|---|---:|
| Original sales records | 5,000 |
| Cleaned transactions | 4,975 |
| Daily operations records | 720 |
| Total units sold | 22,430 |
| Net revenue | Rs. 2,157,560.13 |
| Gross profit | Rs. 1,096,241.70 |
| Overall gross margin | 50.81% |
| Anomaly records | 326 |

## 11. Generated Output Files

The project generates the following files:

- `freshflow_sales_cleaned.csv`
- `freshflow_operations_cleaned.csv`
- `freshflow_metrics.csv`
- `freshflow_daily_trends.csv`
- `freshflow_discount_analysis.csv`
- `freshflow_anomaly_register.csv`
- `freshflow_scenario_analysis.csv`
- `freshflow_final_report.txt`

## 12. Validation

The validation script checks:

- Dataset dimensions.
- Duplicate transaction IDs.
- Valid day, outlet, and product codes.
- Positive quantities, unit prices, and unit costs.
- Valid discount rates.
- Customer-rating ranges.
- Inventory closing-stock calculations.
- Revenue and gross-profit calculations.

The latest recorded execution completed with:

```text
ALL VALIDATION TESTS PASSED SUCCESSFULLY!
```

## 13. Project Documentation

The project includes:

- `data_generation_log.txt` – Documents dataset generation and its methodology.
- `freshflow_final_report.txt` – Contains the final business analytics report.
- `Recommendation.txt` – Contains business recommendations.
- `README.md` – Provides project information and execution instructions.

## 14. Conclusion

The FreshFlow Juice Company Business Analytics Project uses Python and NumPy to analyse sales and inventory data.

The project demonstrates data auditing, data cleaning, numerical calculations, statistical analysis, trend analysis, discount investigation, anomaly detection, and scenario analysis.

The results provide useful insights into business performance and support better decisions related to pricing, inventory management, discounts, costs, and sales performance.
