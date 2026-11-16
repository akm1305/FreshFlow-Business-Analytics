
import numpy as np

print("=" * 60)
print("FRESHFLOW JUICE COMPANY")
print("TASK G: TREND AND ANOMALY ANALYSIS")
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

day = sales["day_index"].astype(int)
quantity = sales["quantity"].astype(float)
price = sales["unit_price"].astype(float)
cost = sales["unit_cost"].astype(float)
discount = sales["discount_rate"].astype(float)

# -------------------------------------------------
# 2. CALCULATE TRANSACTION REVENUE AND PROFIT
# -------------------------------------------------

gross_sales = quantity * price
net_revenue = gross_sales * (1 - discount)
cogs = quantity * cost
gross_profit = net_revenue - cogs

# -------------------------------------------------
# 3. CALCULATE DAILY REVENUE
# -------------------------------------------------

daily_revenue = np.zeros(30)

np.add.at(daily_revenue, day - 1, net_revenue)

days = np.arange(1, 31)

print("\nDAILY REVENUE SUMMARY")
print("Total days:", len(days))
print("Total revenue:", round(np.sum(daily_revenue), 2))
print("Average daily revenue:", round(np.mean(daily_revenue), 2))

highest_day = np.argmax(daily_revenue) + 1
lowest_day = np.argmin(daily_revenue) + 1

print("Highest revenue day:", highest_day)
print("Highest daily revenue:", round(np.max(daily_revenue), 2))
print("Lowest revenue day:", lowest_day)
print("Lowest daily revenue:", round(np.min(daily_revenue), 2))

# -------------------------------------------------
# 4. DAILY ABSOLUTE REVENUE CHANGE
# -------------------------------------------------

absolute_change = np.full(30, np.nan)

absolute_change[1:] = (
    daily_revenue[1:] - daily_revenue[:-1]
)

# -------------------------------------------------
# 5. DAILY PERCENTAGE REVENUE CHANGE
# -------------------------------------------------

percentage_change = np.full(30, np.nan)

previous_revenue = daily_revenue[:-1]

percentage_change[1:] = np.divide(
    absolute_change[1:] * 100,
    previous_revenue,
    out=np.full(29, np.nan),
    where=previous_revenue != 0
)

print("\nDAILY CHANGE ANALYSIS")

for i in range(30):
    print(
        "Day:", days[i],
        "| Revenue:", round(daily_revenue[i], 2),
        "| Absolute Change:", (
            round(absolute_change[i], 2)
            if np.isfinite(absolute_change[i]) else "N/A"
        ),
        "| Percentage Change:", (
            str(round(percentage_change[i], 2)) + "%"
            if np.isfinite(percentage_change[i]) else "N/A"
        )
    )

# -------------------------------------------------
# 6. 7-DAY MOVING AVERAGE
# -------------------------------------------------

moving_average_7 = np.full(30, np.nan)

for i in range(6, 30):
    moving_average_7[i] = np.mean(daily_revenue[i-6:i+1])

print("\n7-DAY MOVING AVERAGE")

for i in range(30):
    if np.isfinite(moving_average_7[i]):
        print(
            "Day:", days[i],
            "| 7-day average revenue:",
            round(moving_average_7[i], 2)
        )

# -------------------------------------------------
# 7. FIRST HALF VS SECOND HALF COMPARISON
# -------------------------------------------------

first_half_average = np.mean(daily_revenue[:15])
second_half_average = np.mean(daily_revenue[15:])

print("\nHALF-MONTH COMPARISON")
print("First 15 days average:", round(first_half_average, 2))
print("Last 15 days average:", round(second_half_average, 2))

if second_half_average > first_half_average:
    print("Revenue trend: Increasing")
else:
    print("Revenue trend: Decreasing")

# -------------------------------------------------
# 8. DAILY REVENUE ANOMALY DETECTION USING IQR
# -------------------------------------------------

q1 = np.percentile(daily_revenue, 25)
q3 = np.percentile(daily_revenue, 75)

iqr = q3 - q1

lower_limit = q1 - 1.5 * iqr
upper_limit = q3 + 1.5 * iqr

unusual_days = (
    (daily_revenue < lower_limit) |
    (daily_revenue > upper_limit)
)

print("\nDAILY REVENUE ANOMALY ANALYSIS")
print("Q1:", round(q1, 2))
print("Q3:", round(q3, 2))
print("IQR:", round(iqr, 2))
print("Lower limit:", round(lower_limit, 2))
print("Upper limit:", round(upper_limit, 2))
print("Unusual revenue days:", np.sum(unusual_days))

for i in np.where(unusual_days)[0]:
    print(
        "Unusual Day:", days[i],
        "| Revenue:", round(daily_revenue[i], 2)
    )

# -------------------------------------------------
# 9. TRANSACTION-LEVEL EXCEPTION SUMMARY
# -------------------------------------------------

loss_mask = gross_profit < 0
high_discount_mask = discount > 0.20

print("\nTRANSACTION EXCEPTION SUMMARY")
print("Loss-making transactions:", np.sum(loss_mask))
print("Transactions with discount above 20%:",
      np.sum(high_discount_mask))
print("Revenue from transactions with discount above 20%:",
      round(np.sum(net_revenue[high_discount_mask]), 2))
print("Total loss from loss-making transactions:",
      round(np.sum(gross_profit[loss_mask]), 2))

# -------------------------------------------------
# 10. SAVE DAILY TREND RESULTS
# -------------------------------------------------

daily_results = np.column_stack((
    days,
    daily_revenue,
    absolute_change,
    percentage_change,
    moving_average_7
))

header = (
    "day_index,daily_revenue,"
    "absolute_revenue_change,"
    "percentage_revenue_change,"
    "moving_average_7_day"
)

np.savetxt(
    "../datasets/freshflow_daily_trends.csv",
    daily_results,
    delimiter=",",
    header=header,
    comments="",
    fmt="%.4f"
)

print("\nDaily trend data saved successfully!")
print("File: freshflow_daily_trends.csv")

print("\n" + "=" * 60)
print("TASK G: TREND AND ANOMALY ANALYSIS COMPLETED!")
print("=" * 60)
