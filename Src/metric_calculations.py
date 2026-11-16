
import numpy as np

# ==========================================
# D4: FINANCIAL METRIC CALCULATIONS
# ==========================================

# Load cleaned sales dataset
sales = np.genfromtxt(
    "../datasets/freshflow_sales_cleaned.csv",
    delimiter=",",
    names=True,
    dtype=float,
    encoding="utf-8"
)

print("========== D4: METRIC CALCULATIONS ==========")

print("\nTotal transactions:", len(sales))

# ------------------------------------------
# STEP 1: EXTRACT REQUIRED COLUMNS
# ------------------------------------------

quantity = sales["quantity"]
unit_price = sales["unit_price"]
unit_cost = sales["unit_cost"]
discount_rate = sales["discount_rate"]

# ------------------------------------------
# STEP 2: CALCULATE GROSS SALES
# ------------------------------------------

gross_sales = quantity * unit_price

# ------------------------------------------
# STEP 3: CALCULATE DISCOUNT AMOUNT
# ------------------------------------------

discount_amount = gross_sales * discount_rate

# ------------------------------------------
# STEP 4: CALCULATE NET REVENUE
# ------------------------------------------

net_revenue = gross_sales - discount_amount

# ------------------------------------------
# STEP 5: CALCULATE COST OF GOODS SOLD
# ------------------------------------------

cogs = quantity * unit_cost

# ------------------------------------------
# STEP 6: CALCULATE GROSS PROFIT
# ------------------------------------------

gross_profit = net_revenue - cogs

# ------------------------------------------
# STEP 7: CALCULATE GROSS MARGIN
# ------------------------------------------

gross_margin = np.divide(
    gross_profit,
    net_revenue,
    out=np.full(len(net_revenue), np.nan),
    where=net_revenue != 0
) * 100

# ------------------------------------------
# STEP 8: CALCULATE AVERAGE SELLING PRICE
# ------------------------------------------

asp = np.divide(
    net_revenue,
    quantity,
    out=np.zeros(len(quantity)),
    where=quantity != 0
)

# ------------------------------------------
# STEP 9: DISPLAY FIRST 5 TRANSACTIONS
# ------------------------------------------

print("\nFIRST 5 TRANSACTION METRICS")

print(
    "Gross Sales:", gross_sales[:5]
)

print(
    "Discount Amount:", discount_amount[:5]
)

print(
    "Net Revenue:", net_revenue[:5]
)

print(
    "COGS:", cogs[:5]
)

print(
    "Gross Profit:", gross_profit[:5]
)

print(
    "Gross Margin (%):", gross_margin[:5]
)

print(
    "ASP:", asp[:5]
)

# ------------------------------------------
# STEP 10: CALCULATE TOTAL BUSINESS METRICS
# ------------------------------------------

total_gross_sales = np.sum(gross_sales)
total_discount = np.sum(discount_amount)
total_net_revenue = np.sum(net_revenue)
total_cogs = np.sum(cogs)
total_gross_profit = np.sum(gross_profit)

overall_margin = (
    total_gross_profit / total_net_revenue * 100
    if total_net_revenue != 0 else np.nan
)

average_asp = np.mean(asp)

print("\n========== BUSINESS PERFORMANCE ==========")

print("Total Gross Sales:", round(total_gross_sales, 2))
print("Total Discount:", round(total_discount, 2))
print("Total Net Revenue:", round(total_net_revenue, 2))
print("Total COGS:", round(total_cogs, 2))
print("Total Gross Profit:", round(total_gross_profit, 2))
print("Overall Gross Margin (%):", round(overall_margin, 2))
print("Average Selling Price:", round(average_asp, 2))

# ------------------------------------------
# STEP 11: CREATE METRICS ARRAY
# ------------------------------------------

metrics_array = np.column_stack((
    sales["transaction_id"],
    gross_sales,
    discount_amount,
    net_revenue,
    cogs,
    gross_profit,
    gross_margin,
    asp
))

# ------------------------------------------
# STEP 12: SAVE METRICS TO CSV
# ------------------------------------------

headers = [
    "transaction_id",
    "gross_sales",
    "discount_amount",
    "net_revenue",
    "cogs",
    "gross_profit",
    "gross_margin",
    "asp"
]

np.savetxt(
    "../datasets/freshflow_metrics.csv",
    metrics_array,
    delimiter=",",
    header=",".join(headers),
    comments="",
    fmt="%.2f"
)

print("\nMetrics array shape:", metrics_array.shape)

print("\nFinancial metrics saved successfully!")
print("D4 COMPLETED SUCCESSFULLY!")
