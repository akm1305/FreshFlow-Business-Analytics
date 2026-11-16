
import numpy as np

print("=" * 60)
print("FRESHFLOW JUICE COMPANY")
print("TASK J: BUSINESS SCENARIO ANALYSIS")
print("=" * 60)

# -------------------------------------------------
# 1. LOAD CLEANED SALES DATA
# -------------------------------------------------

sales = np.genfromtxt(
    "../datasets/freshflow_sales_cleaned.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

quantity = sales["quantity"].astype(float)
unit_price = sales["unit_price"].astype(float)
unit_cost = sales["unit_cost"].astype(float)
discount = sales["discount_rate"].astype(float)

# Retain only valid numerical records
valid = (
    np.isfinite(quantity) &
    np.isfinite(unit_price) &
    np.isfinite(unit_cost) &
    np.isfinite(discount)
)

quantity = quantity[valid]
unit_price = unit_price[valid]
unit_cost = unit_cost[valid]
discount = discount[valid]

print("\nValid transactions:", len(quantity))


# -------------------------------------------------
# 2. BASELINE BUSINESS PERFORMANCE
# -------------------------------------------------

gross_sales = quantity * unit_price
discount_amount = gross_sales * discount

baseline_revenue = np.sum(gross_sales - discount_amount)
baseline_cost = np.sum(quantity * unit_cost)
baseline_profit = baseline_revenue - baseline_cost

print("\nBASELINE PERFORMANCE")
print("Revenue:", round(baseline_revenue, 2))
print("Gross Profit:", round(baseline_profit, 2))


# -------------------------------------------------
# 3. SCENARIO CALCULATION FUNCTION
# -------------------------------------------------

results = []

def calculate_scenario(name, scenario_revenue, scenario_profit):

    revenue_change = scenario_revenue - baseline_revenue
    profit_change = scenario_profit - baseline_profit

    revenue_change_pct = (
        revenue_change / baseline_revenue * 100
        if baseline_revenue != 0 else 0
    )

    profit_change_pct = (
        profit_change / baseline_profit * 100
        if baseline_profit != 0 else 0
    )

    results.append([
        name,
        scenario_revenue,
        scenario_profit,
        revenue_change,
        revenue_change_pct,
        profit_change,
        profit_change_pct
    ])

    print("\n" + name)
    print("Revenue:", round(scenario_revenue, 2))
    print("Gross Profit:", round(scenario_profit, 2))
    print("Revenue Change:", round(revenue_change, 2))
    print("Revenue Change (%):", round(revenue_change_pct, 2), "%")
    print("Profit Change:", round(profit_change, 2))
    print("Profit Change (%):", round(profit_change_pct, 2), "%")


# Baseline scenario
calculate_scenario(
    "Original Business",
    baseline_revenue,
    baseline_profit
)


# -------------------------------------------------
# 4. SCENARIO 1: SALES VOLUME INCREASE BY 10%
# -------------------------------------------------

increased_quantity = quantity * 1.10

revenue_10 = np.sum(
    increased_quantity * unit_price * (1 - discount)
)

profit_10 = (
    revenue_10 -
    np.sum(increased_quantity * unit_cost)
)

calculate_scenario(
    "Sales Volume Increase by 10%",
    revenue_10,
    profit_10
)


# -------------------------------------------------
# 5. SCENARIO 2: COST INCREASE BY 5%
# -------------------------------------------------

increased_cost = unit_cost * 1.05

revenue_cost = baseline_revenue

profit_cost = (
    revenue_cost -
    np.sum(quantity * increased_cost)
)

calculate_scenario(
    "Operating Cost Increase by 5%",
    revenue_cost,
    profit_cost
)


# -------------------------------------------------
# 6. SCENARIO 3: DISCOUNT INCREASE BY 5 PERCENTAGE POINTS
# -------------------------------------------------

discount_5 = np.minimum(discount + 0.05, 1.0)

revenue_discount_5 = np.sum(
    quantity * unit_price * (1 - discount_5)
)

profit_discount_5 = (
    revenue_discount_5 -
    baseline_cost
)

calculate_scenario(
    "Discount Increase by 5 Percentage Points",
    revenue_discount_5,
    profit_discount_5
)


# -------------------------------------------------
# 7. SCENARIO 4: DISCOUNT INCREASE BY 10 PERCENTAGE POINTS
# -------------------------------------------------

discount_10 = np.minimum(discount + 0.10, 1.0)

revenue_discount_10 = np.sum(
    quantity * unit_price * (1 - discount_10)
)

profit_discount_10 = (
    revenue_discount_10 -
    baseline_cost
)

calculate_scenario(
    "Discount Increase by 10 Percentage Points",
    revenue_discount_10,
    profit_discount_10
)


# -------------------------------------------------
# 8. SAVE SCENARIO RESULTS
# -------------------------------------------------

header = (
    "scenario,revenue,gross_profit,"
    "revenue_change,revenue_change_pct,"
    "profit_change,profit_change_pct"
)

np.savetxt(
    "../datasets/freshflow_scenario_analysis.csv",
    np.array(results, dtype=object),
    delimiter=",",
    header=header,
    comments="",
    fmt="%s"
)

print("\n" + "=" * 60)
print("Scenario results saved successfully!")
print("File: freshflow_scenario_analysis.csv")
print("Total scenarios:", len(results))
print("TASK J SCENARIO ANALYSIS COMPLETED!")
print("=" * 60)


# -------------------------------------------------
# 9. BUSINESS INTERPRETATION
# -------------------------------------------------

print("\nBUSINESS INTERPRETATION")
print("1. A 5 percentage-point discount increase reduces")
print("   revenue and gross profit when sales volume is fixed.")

print("2. A 10 percentage-point discount increase has a")
print("   larger impact on revenue and gross profit.")

print("3. Higher sales volume may improve total profit,")
print("   depending on the additional sales and costs.")

print("4. Management should evaluate discounts carefully")
print("   to protect overall profitability.")

print("\nNOTE:")
print("These are mathematical scenarios, not sales forecasts.")
print("They assume that customer demand and sales quantities")
print("do not change in the alternative discount scenarios.")
