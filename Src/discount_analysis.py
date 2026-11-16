
import numpy as np

# Load cleaned sales dataset
sales = np.genfromtxt(
    "../datasets/freshflow_sales_cleaned.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

# Extract required columns
quantity = sales["quantity"].astype(float)
unit_price = sales["unit_price"].astype(float)
unit_cost = sales["unit_cost"].astype(float)
discount_rate = sales["discount_rate"].astype(float)

# Keep only records with valid values for this analysis
valid_mask = (
    np.isfinite(quantity) &
    np.isfinite(unit_price) &
    np.isfinite(unit_cost) &
    np.isfinite(discount_rate) &
    (quantity > 0) &
    (unit_price > 0) &
    (unit_cost >= 0) &
    (discount_rate >= 0) &
    (discount_rate <= 1)
)

# Apply the same valid-record filter to every metric
quantity = quantity[valid_mask]
unit_price = unit_price[valid_mask]
unit_cost = unit_cost[valid_mask]
discount_rate = discount_rate[valid_mask]

print("========== TASK H: DISCOUNT INVESTIGATION ==========")
print("Total valid transactions:", len(quantity))
print("Excluded transactions:", len(sales) - len(quantity))

# Calculate financial metrics
gross_sales = quantity * unit_price
discount_amount = gross_sales * discount_rate
net_revenue = gross_sales - discount_amount
cogs = quantity * unit_cost
gross_profit = net_revenue - cogs

# Define discount bands
bands = [
    ("0% to below 10%", 0.00, 0.10),
    ("10% to below 20%", 0.10, 0.20),
    ("20% to below 30%", 0.20, 0.30),
    ("30% to 100%", 0.30, 1.01)
]

results = []

print("\nDISCOUNT BAND COMPARISON")

for label, lower, upper in bands:

    # Select transactions belonging to this band
    mask = (
        (discount_rate >= lower) &
        (discount_rate < upper)
    )

    # Calculate group metrics
    transaction_count = np.sum(mask)
    total_quantity = np.sum(quantity[mask])
    total_revenue = np.sum(net_revenue[mask])
    total_profit = np.sum(gross_profit[mask])

    # Calculate weighted gross margin
    if total_revenue > 0:
        gross_margin = (total_profit / total_revenue) * 100
    else:
        gross_margin = np.nan

    print("\nDiscount Band:", label)
    print("Transactions:", transaction_count)
    print("Quantity Sold:", total_quantity)
    print("Net Revenue:", round(total_revenue, 2))
    print("Gross Profit:", round(total_profit, 2))
    print("Gross Margin (%):", round(gross_margin, 2)
          if np.isfinite(gross_margin) else "Not calculable")

    results.append([
        label,
        transaction_count,
        total_quantity,
        total_revenue,
        total_profit,
        gross_margin
    ])

# Save results to CSV
results_array = np.array(results, dtype=object)

np.savetxt(
    "../datasets/freshflow_discount_analysis.csv",
    results_array,
    delimiter=",",
    header="discount_band,transactions,quantity_sold,net_revenue,gross_profit,gross_margin_percent",
    comments="",
    fmt="%s"
)

# Explain analytical limitations
print("\nANALYTICAL INTERPRETATION")

print(
    "\nSelection Bias:\n"
    "Discounts may not be randomly assigned. "
    "Management may give higher discounts to selected products, "
    "outlets or transactions. Therefore, discounted transactions "
    "may not represent all sales equally."
)

print(
    "\nConfounding:\n"
    "Product type, outlet, day, customer demand and selling price "
    "may influence both discount levels and sales performance. "
    "These factors can affect the observed relationship."
)

print(
    "\nConclusion:\n"
    "Discount-band comparisons show associations in the observed "
    "data. They do not prove that higher discounts cause higher "
    "quantity sold or lower gross margin."
)

print("\nDiscount analysis saved successfully!")
print("TASK H COMPLETED SUCCESSFULLY!")
