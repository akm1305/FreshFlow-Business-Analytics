
import numpy as np

# ============================================================
# 1. LOAD PROJECT DATA
# ============================================================

sales = np.genfromtxt(
    "../datasets/freshflow_sales_cleaned.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

daily = np.genfromtxt(
    "../datasets/freshflow_daily_trends.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

scenarios = np.genfromtxt(
    "../datasets/freshflow_scenario_analysis.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

anomalies = np.genfromtxt(
    "../datasets/freshflow_anomaly_register.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

# Convert sales columns into numeric arrays
quantity = sales["quantity"].astype(float)
price = sales["unit_price"].astype(float)
cost = sales["unit_cost"].astype(float)
discount = sales["discount_rate"].astype(float)

outlet_ids_data = sales["outlet_id"]
product_ids_data = sales["product_code"]
category_ids_data = sales["category_code"]

# ============================================================
# 2. CALCULATE BUSINESS METRICS
# ============================================================

gross_sales = quantity * price
discount_amount = gross_sales * discount
revenue = gross_sales - discount_amount
total_cost_per_transaction = quantity * cost
profit = revenue - total_cost_per_transaction

total_transactions = len(sales)
total_units = np.sum(quantity)
total_gross_sales = np.sum(gross_sales)
total_discount = np.sum(discount_amount)
total_revenue = np.sum(revenue)
total_cost = np.sum(total_cost_per_transaction)
total_profit = np.sum(profit)

# Weighted overall gross margin
overall_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0 else 0
)

average_transaction_value = (
    total_revenue / total_transactions
    if total_transactions != 0 else 0
)

# ============================================================
# 3. DATA QUALITY INFORMATION
# ============================================================

missing_ratings = 0

if "customer_rating" in sales.dtype.names:
    ratings = sales["customer_rating"].astype(float)
    missing_ratings = np.sum(~np.isfinite(ratings))
    valid_ratings = ratings[np.isfinite(ratings)]
else:
    valid_ratings = np.array([])

# ============================================================
# 4. DAILY PERFORMANCE
# ============================================================

daily_revenue = daily["daily_revenue"].astype(float)
day_numbers = daily["day_index"].astype(int)

best_day = int(day_numbers[np.argmax(daily_revenue)])
worst_day = int(day_numbers[np.argmin(daily_revenue)])

highest_daily_revenue = np.max(daily_revenue)
lowest_daily_revenue = np.min(daily_revenue)
average_daily_revenue = np.mean(daily_revenue)

# First half vs second half
first_half_average = np.mean(daily_revenue[:15])
second_half_average = np.mean(daily_revenue[15:])

if second_half_average < first_half_average:
    trend_direction = "Decreasing"
elif second_half_average > first_half_average:
    trend_direction = "Increasing"
else:
    trend_direction = "Stable"

# ============================================================
# 5. OUTLET PERFORMANCE
# ============================================================

outlet_ids = np.unique(outlet_ids_data)

outlet_results = []

for outlet in outlet_ids:
    mask = outlet_ids_data == outlet

    outlet_revenue = np.sum(revenue[mask])
    outlet_profit = np.sum(profit[mask])
    outlet_transactions = np.sum(mask)
    outlet_units = np.sum(quantity[mask])

    outlet_results.append(
        (
            int(outlet),
            outlet_transactions,
            outlet_units,
            outlet_revenue,
            outlet_profit
        )
    )

best_outlet_result = max(
    outlet_results,
    key=lambda x: x[3]
)

# ============================================================
# 6. PRODUCT AND CATEGORY PERFORMANCE
# ============================================================

product_names = {
    1: "Orange Juice",
    2: "Mango Juice",
    3: "Apple Juice",
    4: "Watermelon Juice",
    5: "Banana Smoothie",
    6: "Mixed Fruit Smoothie",
    7: "Lemonade",
    8: "Iced Tea"
}

category_names = {
    1: "Juices",
    2: "Smoothies",
    3: "Lemonade",
    4: "Iced Tea"
}

product_ids = np.unique(product_ids_data)
product_results = []

for product in product_ids:
    mask = product_ids_data == product

    product_revenue = np.sum(revenue[mask])
    product_profit = np.sum(profit[mask])
    product_units = np.sum(quantity[mask])

    product_results.append(
        (
            int(product),
            product_units,
            product_revenue,
            product_profit
        )
    )

best_product_result = max(
    product_results,
    key=lambda x: x[2]
)

lowest_product_result = min(
    product_results,
    key=lambda x: x[2]
)

category_ids = np.unique(category_ids_data)
category_results = []

for category in category_ids:
    mask = category_ids_data == category

    category_revenue = np.sum(revenue[mask])
    category_profit = np.sum(profit[mask])

    category_results.append(
        (
            int(category),
            category_revenue,
            category_profit
        )
    )

# ============================================================
# 7. DISCOUNT ANALYSIS
# ============================================================

discount_bands = [
    ("0% to below 10%", 0.00, 0.10),
    ("10% to below 20%", 0.10, 0.20),
    ("20% to below 30%", 0.20, 0.30),
    ("30% to 100%", 0.30, 1.01)
]

discount_results = []

for band_name, lower, upper in discount_bands:
    mask = (discount >= lower) & (discount < upper)

    band_transactions = np.sum(mask)
    band_units = np.sum(quantity[mask])
    band_revenue = np.sum(revenue[mask])
    band_profit = np.sum(profit[mask])

    band_margin = (
        band_profit / band_revenue * 100
        if band_revenue != 0 else 0
    )

    discount_results.append(
        (
            band_name,
            band_transactions,
            band_units,
            band_revenue,
            band_profit,
            band_margin
        )
    )

# ============================================================
# 8. ANOMALY ANALYSIS
# ============================================================

loss_making_count = np.sum(
    anomalies["reason_code"] == "LOSS_MAKING"
)

high_discount_count = np.sum(
    anomalies["reason_code"] == "HIGH_DISCOUNT"
)

missing_rating_count = np.sum(
    anomalies["reason_code"] == "MISSING_RATING"
)

high_price_count = np.sum(
    anomalies["reason_code"] == "HIGH_UNIT_PRICE"
)

total_anomaly_records = len(anomalies)

report = []

# ============================================================
# SCENARIO NAME FIELD
# ============================================================

scenario_fields = scenarios.dtype.names

scenario_name_field = None

for possible_name in [
    "scenario",
    "scenario_name",
    "name",
    "scenario_type"
]:
    if possible_name in scenario_fields:
        scenario_name_field = possible_name
        break

report.append("\n9. ANOMALY AND EXCEPTION ANALYSIS")
report.append("-" * 45)
report.append(f"Loss-making transactions: {loss_making_count}")
report.append(f"Transactions with discount above 20%: {high_discount_count}")
report.append(f"Missing customer ratings: {missing_rating_count}")
report.append(f"High unit-price transactions: {high_price_count}")
report.append(f"Total anomaly records: {total_anomaly_records}")
report.append(
    "Note: Each record represents an anomaly reason. "
    "A transaction may appear more than once."
)

# ============================================================
# 10. PREPARE FINAL REPORT
# ============================================================

report = []

report.append("FRESHFLOW JUICE COMPANY")
report.append("FINAL BUSINESS ANALYTICS REPORT")
report.append("=" * 65)

# ------------------------------------------------------------
# SECTION 1: DATASET OVERVIEW
# ------------------------------------------------------------

report.append("\n1. DATASET OVERVIEW")
report.append("-" * 45)
report.append(f"Total cleaned sales transactions: {total_transactions}")
report.append(f"Total units sold: {total_units:.0f}")
report.append("Daily operations records: 720")
report.append(f"Sales analysis period: {len(daily_revenue)} days")
report.append("Number of outlets: 3")
report.append("Number of products: 8")

# ------------------------------------------------------------
# SECTION 2: DATA QUALITY
# ------------------------------------------------------------

report.append("\n2. DATA QUALITY AND CLEANING")
report.append("-" * 45)
report.append("Original sales records: 5,000")
report.append(f"Cleaned sales records: {total_transactions}")
report.append("Duplicate transaction IDs removed: 5")
report.append("Invalid sales records removed: 20")
report.append("Product/category mismatches corrected: 4")
report.append(f"Missing customer ratings: {missing_rating_count}")
report.append("Operations records: 720")
report.append("Inventory formula errors after cleaning: 0")

# ------------------------------------------------------------
# SECTION 3: OVERALL BUSINESS PERFORMANCE
# ------------------------------------------------------------

report.append("\n3. OVERALL BUSINESS PERFORMANCE")
report.append("-" * 45)
report.append(f"Total gross sales: Rs. {total_gross_sales:.2f}")
report.append(f"Total discount amount: Rs. {total_discount:.2f}")
report.append(f"Total net revenue: Rs. {total_revenue:.2f}")
report.append(f"Total cost of goods sold: Rs. {total_cost:.2f}")
report.append(f"Total gross profit: Rs. {total_profit:.2f}")
report.append(f"Overall gross margin: {overall_margin:.2f}%")
report.append(
    f"Average revenue per transaction: Rs. "
    f"{average_transaction_value:.2f}"
)

# ------------------------------------------------------------
# SECTION 4: STATISTICAL SUMMARY
# ------------------------------------------------------------

report.append("\n4. STATISTICAL SUMMARY")
report.append("-" * 45)
report.append(f"Average quantity per transaction: {np.mean(quantity):.2f}")
report.append(f"Median quantity: {np.median(quantity):.2f}")
report.append(f"Minimum quantity: {np.min(quantity):.0f}")
report.append(f"Maximum quantity: {np.max(quantity):.0f}")
report.append(f"Average selling price: Rs. {np.mean(price):.2f}")
report.append(f"Average unit cost: Rs. {np.mean(cost):.2f}")

if len(valid_ratings) > 0:
    report.append(
        f"Average customer rating: {np.mean(valid_ratings):.2f}/5"
    )

# ------------------------------------------------------------
# SECTION 5: OUTLET PERFORMANCE
# ------------------------------------------------------------

report.append("\n5. OUTLET PERFORMANCE")
report.append("-" * 45)

for outlet, transactions, units, outlet_revenue, outlet_profit in outlet_results:
    report.append(
        f"Outlet {outlet}: Transactions={transactions}, "
        f"Units={units:.0f}, Revenue=Rs. {outlet_revenue:.2f}, "
        f"Profit=Rs. {outlet_profit:.2f}"
    )

report.append(
    f"Best performing outlet: Outlet {best_outlet_result[0]}"
)

# ------------------------------------------------------------
# SECTION 6: PRODUCT AND CATEGORY PERFORMANCE
# ------------------------------------------------------------

report.append("\n6. PRODUCT AND CATEGORY PERFORMANCE")
report.append("-" * 45)

for product, units, product_revenue, product_profit in product_results:
    report.append(
        f"{product_names[product]}: Units={units:.0f}, "
        f"Revenue=Rs. {product_revenue:.2f}, "
        f"Profit=Rs. {product_profit:.2f}"
    )

report.append(
    f"Highest revenue product: "
    f"{product_names[best_product_result[0]]}"
)

report.append(
    f"Lowest revenue product: "
    f"{product_names[lowest_product_result[0]]}"
)

report.append("\nCategory-wise revenue:")

for category, category_revenue, category_profit in category_results:
    report.append(
        f"{category_names.get(category, 'Unknown Category')}: "
        f"Revenue=Rs. {category_revenue:.2f}, "
        f"Profit=Rs. {category_profit:.2f}"
    )

# ------------------------------------------------------------
# SECTION 7: DAILY TREND ANALYSIS
# ------------------------------------------------------------

report.append("\n7. DAILY TREND ANALYSIS")
report.append("-" * 45)
report.append(f"Average daily revenue: Rs. {average_daily_revenue:.2f}")
report.append(
    f"Highest revenue day: Day {best_day} "
    f"(Rs. {highest_daily_revenue:.2f})"
)
report.append(
    f"Lowest revenue day: Day {worst_day} "
    f"(Rs. {lowest_daily_revenue:.2f})"
)
report.append(
    f"First 15 days average revenue: Rs. {first_half_average:.2f}"
)
report.append(
    f"Last 15 days average revenue: Rs. {second_half_average:.2f}"
)
report.append(f"Overall daily revenue trend: {trend_direction}")

report.append("\nDaily revenue changes:")

for i in range(len(daily)):
    if i == 0:
        continue

    absolute_change = daily["absolute_revenue_change"][i]
    percentage_change = daily["percentage_revenue_change"][i]

    report.append(
        f"Day {day_numbers[i]}: "
        f"Change=Rs. {absolute_change:.2f}, "
        f"Percentage change={percentage_change:.2f}%"
    )

# ------------------------------------------------------------
# SECTION 8: DISCOUNT ANALYSIS
# ------------------------------------------------------------

report.append("\n8. DISCOUNT ANALYSIS")
report.append("-" * 45)

for name, transactions, units, band_revenue, band_profit, margin in discount_results:
    report.append(
        f"{name}: Transactions={transactions}, "
        f"Units={units:.0f}, Revenue=Rs. {band_revenue:.2f}, "
        f"Profit=Rs. {band_profit:.2f}, "
        f"Gross Margin={margin:.2f}%"
    )

# ------------------------------------------------------------
# SECTION 9: ANOMALY ANALYSIS
# ------------------------------------------------------------

report.append("\n9. ANOMALY AND EXCEPTION ANALYSIS")
report.append("-" * 45)
report.append(f"Loss-making transactions: {loss_making_count}")
report.append(f"Transactions with discount above 20%: {high_discount_count}")
report.append(f"Missing customer ratings: {missing_rating_count}")
report.append(f"High unit-price transactions (above Rs. 180): {high_price_count}")
report.append(
    f"Total anomaly records across these categories: "
    f"{total_anomaly_records}"
)
report.append(
    "Note: A transaction may appear in more than one anomaly category."
)

# ------------------------------------------------------------
# SECTION 10: SCENARIO ANALYSIS
# ------------------------------------------------------------

report.append("\n10. BUSINESS SCENARIO ANALYSIS")
report.append("-" * 45)

for i in range(len(scenarios)):
    if scenario_name_field:
        scenario_name = str(scenarios[scenario_name_field][i])
    elif i < len(scenario_labels):
        scenario_name = scenario_labels[i]
    else:
        scenario_name = f"Scenario {i + 1}"

    scenario_revenue = float(scenarios["revenue"][i])
    scenario_profit = float(scenarios["gross_profit"][i])

    report.append(
        f"{scenario_name}: "
        f"Revenue=Rs. {scenario_revenue:.2f}, "
        f"Profit=Rs. {scenario_profit:.2f}"
    )

# ------------------------------------------------------------
# SECTION 11: BUSINESS RECOMMENDATIONS
# ------------------------------------------------------------

report.append("\n11. BUSINESS RECOMMENDATIONS")
report.append("-" * 45)

report.append(
    "1. Review high-discount strategies because gross margin "
    "declines as discount levels increase."
)

report.append(
    "2. Introduce approval limits for discounts above 20% "
    "and evaluate whether promotions generate additional sales."
)

report.append(
    "3. Investigate Outlet 3's lower revenue compared with "
    "the other outlets and review its product mix and sales practices."
)

report.append(
    "4. Maintain adequate stock of high-revenue products such as "
    "Mixed Fruit Smoothie and Mango Juice."
)

report.append(
    "5. Review Iced Tea's sales performance before making "
    "inventory, pricing or promotional decisions."
)

report.append(
    "6. Monitor daily revenue changes to identify declining "
    "performance early."
)

report.append(
    "7. Continue monitoring operating costs to protect "
    "overall business profitability."
)

# ------------------------------------------------------------
# SECTION 12: LIMITATIONS AND CONCLUSION
# ------------------------------------------------------------

report.append("\n12. LIMITATIONS AND CONCLUSION")
report.append("-" * 45)

report.append("LIMITATIONS:")
report.append(
    "1. The analysis covers only 30 days of sales data."
)
report.append(
    "2. Scenario analysis uses assumptions and does not guarantee "
    "future business results."
)
report.append(
    "3. Discount scenarios assume sales quantities remain unchanged."
)
report.append(
    "4. Associations in the data do not necessarily prove "
    "cause-and-effect relationships."
)

report.append("\nCONCLUSION:")
report.append(
    "The FreshFlow Juice Company dataset was analysed using NumPy. "
    "The project covered data auditing, cleaning, metric calculation, "
    "statistical analysis, outlet and product performance, daily trends, "
    "discount investigation, anomaly detection and business scenarios. "
    "The findings and recommendations can support better decisions "
    "about pricing, inventory, costs and sales performance."
)

report.append("\n" + "=" * 65)
report.append("END OF FRESHFLOW BUSINESS ANALYTICS REPORT")

# ============================================================
# 11. PRINT AND SAVE FINAL REPORT
# ============================================================

final_text = "\n".join(report)

print(final_text)

with open(
        "../freshflow_final_report.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write(final_text)

print("\nFinal report saved successfully!")
print("File: freshflow_final_report.txt")
print("D8 COMPLETED SUCCESSFULLY!")
