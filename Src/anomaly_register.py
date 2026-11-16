
import numpy as np

# Load cleaned sales data
sales = np.genfromtxt(
    "../datasets/freshflow_sales_cleaned.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

# Extract columns
transaction_id = sales["transaction_id"]
day = sales["day_index"]
outlet = sales["outlet_id"]
product = sales["product_code"]

quantity = sales["quantity"].astype(float)
unit_price = sales["unit_price"].astype(float)
unit_cost = sales["unit_cost"].astype(float)
discount = sales["discount_rate"].astype(float)
rating = sales["customer_rating"].astype(float)

# Calculate financial metrics
gross_sales = quantity * unit_price
net_revenue = gross_sales * (1 - discount)
cogs = quantity * unit_cost
gross_profit = net_revenue - cogs

# Store anomaly records
anomalies = []

# Function to add flagged transactions
def add_anomalies(mask, reason_code, values):

    indexes = np.where(mask)[0]

    for i in indexes:
        anomalies.append([
            transaction_id[i],
            day[i],
            outlet[i],
            product[i],
            reason_code,
            values[i],
            net_revenue[i],
            gross_profit[i]
        ])


print("========== TASK I: ANOMALY REGISTER ==========")

# 1. Loss-making transactions
loss_mask = gross_profit < 0

add_anomalies(
    loss_mask,
    "LOSS_MAKING",
    gross_profit
)

# 2. High-discount transactions
high_discount_mask = discount > 0.20

add_anomalies(
    high_discount_mask,
    "HIGH_DISCOUNT",
    discount
)

# 3. Missing customer ratings
missing_rating_mask = ~np.isfinite(rating)

add_anomalies(
    missing_rating_mask,
    "MISSING_RATING",
    rating
)

# 4. Unusually high unit prices using IQR
q1 = np.percentile(unit_price, 25)
q3 = np.percentile(unit_price, 75)

iqr = q3 - q1
upper_limit = q3 + (1.5 * iqr)

high_price_mask = unit_price > upper_limit

add_anomalies(
    high_price_mask,
    "HIGH_UNIT_PRICE",
    unit_price
)

# Display summary
print("\nANOMALY SUMMARY")
print("Loss-making transactions:", np.sum(loss_mask))
print("High-discount transactions:", np.sum(high_discount_mask))
print("Missing customer ratings:", np.sum(missing_rating_mask))
print("High unit-price transactions:", np.sum(high_price_mask))

print("\nTotal anomaly records:", len(anomalies))

# Save anomaly register
header = (
    "transaction_id,day_index,outlet_id,product_code,"
    "reason_code,observed_value,net_revenue,gross_profit"
)

if len(anomalies) > 0:

    anomaly_array = np.array(anomalies, dtype=object)

    np.savetxt(
        "../datasets/freshflow_anomaly_register.csv",
        anomaly_array,
        delimiter=",",
        header=header,
        comments="",
        fmt="%s"
    )

else:
    with open(
            "../datasets/freshflow_anomaly_register.csv",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(header + "\n")

print("\nAnomaly register saved successfully!")
print("TASK I COMPLETED SUCCESSFULLY!")
