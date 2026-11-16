
import numpy as np

# ==========================================
# D5: STATISTICAL ANALYSIS
# ==========================================

# Load cleaned sales dataset
sales = np.genfromtxt(
    "../datasets/freshflow_sales_cleaned.csv",
    delimiter=",",
    names=True,
    dtype=float,
    encoding="utf-8"
)

# Load financial metrics
metrics = np.genfromtxt(
    "../datasets/freshflow_metrics.csv",
    delimiter=",",
    names=True,
    dtype=float,
    encoding="utf-8"
)

print("========== D5: STATISTICAL ANALYSIS ==========")

# ------------------------------------------
# STEP 1: DESCRIPTIVE STATISTICS
# ------------------------------------------

columns = {
    "Quantity": sales["quantity"],
    "Unit Price": sales["unit_price"],
    "Unit Cost": sales["unit_cost"],
    "Gross Sales": metrics["gross_sales"],
    "Net Revenue": metrics["net_revenue"],
    "Gross Profit": metrics["gross_profit"],
    "Gross Margin": metrics["gross_margin"],
    "Customer Rating": sales["customer_rating"]
}

print("\n1. DESCRIPTIVE STATISTICS")

for name, data in columns.items():

    # Remove missing or infinite values
    valid_data = data[np.isfinite(data)]

    print("\n", name)

    print("Count:", len(valid_data))
    print("Mean:", round(np.mean(valid_data), 2))
    print("Median:", round(np.median(valid_data), 2))
    print("Standard Deviation:", round(np.std(valid_data), 2))
    print("Minimum:", round(np.min(valid_data), 2))
    print("Maximum:", round(np.max(valid_data), 2))
    print("25th Percentile:", round(np.percentile(valid_data, 25), 2))
    print("75th Percentile:", round(np.percentile(valid_data, 75), 2))


# ------------------------------------------
# STEP 2: OUTLET-WISE PERFORMANCE
# ------------------------------------------

print("\n2. OUTLET-WISE PERFORMANCE")

for outlet in range(1, 4):

    mask = sales["outlet_id"] == outlet

    print("\nOutlet", outlet)

    print("Transactions:", np.sum(mask))

    print(
        "Total Net Revenue:",
        round(np.sum(metrics["net_revenue"][mask]), 2)
    )

    print(
        "Total Gross Profit:",
        round(np.sum(metrics["gross_profit"][mask]), 2)
    )


# ------------------------------------------
# STEP 3: PRODUCT-WISE PERFORMANCE
# ------------------------------------------

print("\n3. PRODUCT-WISE PERFORMANCE")

product_names = [
    "Orange Juice",
    "Mango Juice",
    "Apple Juice",
    "Watermelon Juice",
    "Banana Smoothie",
    "Mixed Fruit Smoothie",
    "Lemonade",
    "Iced Tea"
]

for product in range(1, 9):

    mask = sales["product_code"] == product

    print("\nProduct:", product_names[product - 1])

    print("Units Sold:", int(np.sum(sales["quantity"][mask])))

    print(
        "Net Revenue:",
        round(np.sum(metrics["net_revenue"][mask]), 2)
    )

    print(
        "Gross Profit:",
        round(np.sum(metrics["gross_profit"][mask]), 2)
    )


# ------------------------------------------
# STEP 4: CUSTOMER RATING ANALYSIS
# ------------------------------------------

print("\n4. CUSTOMER RATING ANALYSIS")

ratings = sales["customer_rating"]

valid_ratings = ratings[np.isfinite(ratings)]

print("Valid ratings:", len(valid_ratings))
print("Missing ratings:", np.sum(~np.isfinite(ratings)))
print("Average rating:", round(np.mean(valid_ratings), 2))
print("Median rating:", round(np.median(valid_ratings), 2))


# ------------------------------------------
# STEP 5: OVERALL ASP
# ------------------------------------------

print("\n5. AVERAGE SELLING PRICE ANALYSIS")

total_net_revenue = np.sum(metrics["net_revenue"])
total_quantity = np.sum(sales["quantity"])

weighted_asp = total_net_revenue / total_quantity

average_transaction_asp = np.mean(
    metrics["asp"]
) if "asp" in metrics.dtype.names else np.nan

print("Total quantity sold:", int(total_quantity))
print("Weighted average selling price:", round(weighted_asp, 2))


# ------------------------------------------
# STEP 6: FINAL SUMMARY
# ------------------------------------------

print("\n========== STATISTICAL ANALYSIS COMPLETED ==========")
