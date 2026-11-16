
import numpy as np

print("=" * 55)
print("TASK K: HAND CALCULATIONS AND VALIDATION TESTS")
print("=" * 55)

# -------------------------------------------------
# 1. LOAD CLEANED DATASETS
# -------------------------------------------------

sales = np.genfromtxt(
    "../datasets/freshflow_sales_cleaned.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

operations = np.genfromtxt(
    "../datasets/freshflow_operations_cleaned.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

metrics = np.genfromtxt(
    "../datasets/freshflow_metrics.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

print("\n1. DATASET DIMENSIONS")
print("Sales records:", len(sales))
print("Operations records:", len(operations))
print("Metrics records:", len(metrics))

# -------------------------------------------------
# 2. FIVE INDEPENDENT HAND CALCULATIONS
# -------------------------------------------------

print("\n2. FIVE HAND-CALCULATED TRANSACTIONS")

for i in range(5):

    quantity = float(sales["quantity"][i])
    price = float(sales["unit_price"][i])
    cost = float(sales["unit_cost"][i])
    discount = float(sales["discount_rate"][i])

    # Independent calculations using scalar arithmetic
    gross_sales = quantity * price
    discount_amount = gross_sales * discount
    net_revenue = gross_sales - discount_amount
    cogs = quantity * cost
    gross_profit = net_revenue - cogs

    print("\nTransaction ID:", sales["transaction_id"][i])
    print("Gross Sales:", round(gross_sales, 2))
    print("Discount Amount:", round(discount_amount, 2))
    print("Net Revenue:", round(net_revenue, 2))
    print("Cost of Goods Sold:", round(cogs, 2))
    print("Gross Profit:", round(gross_profit, 2))

    # Compare hand calculations with metric CSV
    np.testing.assert_allclose(
        gross_sales, metrics["gross_sales"][i], rtol=1e-5, atol=0.01
    )
    np.testing.assert_allclose(
        discount_amount, metrics["discount_amount"][i], rtol=1e-5, atol=0.01
    )
    np.testing.assert_allclose(
        net_revenue, metrics["net_revenue"][i], rtol=1e-5, atol=0.01
    )
    np.testing.assert_allclose(
        cogs, metrics["cogs"][i], rtol=1e-5, atol=0.01
    )
    np.testing.assert_allclose(
        gross_profit, metrics["gross_profit"][i], rtol=1e-5, atol=0.01
    )

print("\nAll five hand calculations match the metrics CSV.")

# -------------------------------------------------
# 3. DATASET VALIDATION TESTS
# -------------------------------------------------

print("\n3. VALIDATION TESTS")

# Check expected dataset dimensions
assert len(sales) == 4975
assert len(operations) == 720
assert len(metrics) == len(sales)

print("PASS: Dataset dimensions are correct.")

# Check duplicate transaction IDs
assert len(np.unique(sales["transaction_id"])) == len(sales)

print("PASS: No duplicate transaction IDs.")

# Check valid day range
assert np.all((sales["day_index"] >= 1) & (sales["day_index"] <= 30))

print("PASS: Day index is between 1 and 30.")

# Check outlet IDs
assert np.all((sales["outlet_id"] >= 1) & (sales["outlet_id"] <= 3))

print("PASS: Outlet IDs are valid.")

# Check product codes
assert np.all((sales["product_code"] >= 1) & (sales["product_code"] <= 8))

print("PASS: Product codes are valid.")

# Check quantity and prices
assert np.all(sales["quantity"] > 0)
assert np.all(sales["unit_price"] > 0)
assert np.all(sales["unit_cost"] > 0)

print("PASS: Quantity, unit price and unit cost are positive.")

# Check discount range
assert np.all(
    (sales["discount_rate"] >= 0) &
    (sales["discount_rate"] <= 1)
)

print("PASS: Discount rates are between 0 and 1.")

# Check customer ratings: missing values allowed
ratings = sales["customer_rating"].astype(float)
valid_ratings = ratings[np.isfinite(ratings)]

assert np.all((valid_ratings >= 1) & (valid_ratings <= 5))

print("PASS: All available customer ratings are between 1 and 5.")

# -------------------------------------------------
# 4. INVENTORY FORMULA VALIDATION
# -------------------------------------------------

expected_closing = (
    operations["opening_stock"]
    + operations["stock_received"]
    - operations["units_sold"]
    - operations["waste_units"]
)

np.testing.assert_array_equal(
    expected_closing,
    operations["closing_stock"]
)

assert np.all(operations["closing_stock"] >= 0)

print("PASS: Inventory closing-stock formula is correct.")
print("PASS: No negative closing stock.")

# -------------------------------------------------
# 5. METRIC VALIDATION
# -------------------------------------------------

quantity = sales["quantity"].astype(float)
price = sales["unit_price"].astype(float)
cost = sales["unit_cost"].astype(float)
discount = sales["discount_rate"].astype(float)

expected_net_revenue = quantity * price * (1 - discount)
expected_profit = expected_net_revenue - quantity * cost

np.testing.assert_allclose(
    expected_net_revenue,
    metrics["net_revenue"],
    rtol=1e-5, atol=0.01
)

np.testing.assert_allclose(
    expected_profit,
    metrics["gross_profit"],
    rtol=1e-5, atol=0.01
)

print("PASS: Net revenue calculations are correct.")
print("PASS: Gross profit calculations are correct.")

# -------------------------------------------------
# FINAL RESULT
# -------------------------------------------------

print("\n" + "=" * 55)
print("ALL VALIDATION TESTS PASSED SUCCESSFULLY!")
print("TASK K COMPLETED SUCCESSFULLY!")
print("=" * 55)
