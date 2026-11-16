
import numpy as np

# ==========================================
# D2 - DATA AUDIT
# ==========================================

# Load both datasets
sales = np.genfromtxt(
    "freshflow_sales.csv",
    delimiter=",",
    names=True,
    dtype=float,
    encoding="utf-8"
)

operations = np.genfromtxt(
    "../datasets/freshflow_daily_operations.csv",
    delimiter=",",
    names=True,
    dtype=float,
    encoding="utf-8"
)

print("========== DATA AUDIT ==========")

# ------------------------------------------
# 1. BASIC DATASET INFORMATION
# ------------------------------------------

print("\n1. DATASET INFORMATION")

print("Sales records:", len(sales))
print("Sales columns:", len(sales.dtype.names))

print("Operations records:", len(operations))
print("Operations columns:", len(operations.dtype.names))


# ------------------------------------------
# 2. CHECK MISSING VALUES
# ------------------------------------------

print("\n2. MISSING VALUES IN SALES DATA")

for column in sales.dtype.names:
    missing = np.sum(np.isnan(sales[column]))
    print(column, ":", missing)

print("\nMISSING VALUES IN OPERATIONS DATA")

for column in operations.dtype.names:
    missing = np.sum(np.isnan(operations[column]))
    print(column, ":", missing)


# ------------------------------------------
# 3. CHECK DUPLICATE TRANSACTION IDs
# ------------------------------------------

print("\n3. DUPLICATE TRANSACTION IDs")

valid_ids = sales["transaction_id"][
    np.isfinite(sales["transaction_id"])
]

unique_ids, counts = np.unique(
    valid_ids,
    return_counts=True
)

duplicate_ids = unique_ids[counts > 1]

print("Number of duplicate IDs:", len(duplicate_ids))
print("Duplicate IDs:", duplicate_ids)


# ------------------------------------------
# 4. CHECK INVALID VALUES
# ------------------------------------------

print("\n4. INVALID VALUES IN SALES DATA")

invalid_checks = {
    "Day index": (
        (sales["day_index"] < 1) |
        (sales["day_index"] > 30)
    ),

    "Outlet ID": (
        (sales["outlet_id"] < 1) |
        (sales["outlet_id"] > 3)
    ),

    "Product code": (
        (sales["product_code"] < 1) |
        (sales["product_code"] > 8)
    ),

    "Category code": (
        (sales["category_code"] < 1) |
        (sales["category_code"] > 4)
    ),

    "Quantity": sales["quantity"] <= 0,

    "Unit price": sales["unit_price"] <= 0,

    "Unit cost": sales["unit_cost"] <= 0,

    "Discount rate": (
        (sales["discount_rate"] < 0) |
        (sales["discount_rate"] > 1)
    ),

    "Stock before units": sales["stock_before_units"] < 0,

    "Payment code": (
        (sales["payment_code"] < 1) |
        (sales["payment_code"] > 4)
    ),

    "Customer rating": (
        (sales["customer_rating"] < 1) |
        (sales["customer_rating"] > 5)
    )
}

for name, condition in invalid_checks.items():

    invalid_count = np.sum(
        condition & np.isfinite(sales["transaction_id"])
    )

    print(name, ":", invalid_count)


# ------------------------------------------
# 5. CHECK PRODUCT AND CATEGORY MAPPING
# ------------------------------------------

print("\n5. PRODUCT CATEGORY MISMATCH")

product_category = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 4
}

mismatch_count = 0

for record in sales:

    product = record["product_code"]
    category = record["category_code"]

    if not np.isfinite(product) or not np.isfinite(category):
        continue

    expected_category = product_category.get(int(product))

    if expected_category != category:
        mismatch_count += 1

print("Product/category mismatches:", mismatch_count)


# ------------------------------------------
# 6. AUDIT DAILY OPERATIONS DATA
# ------------------------------------------

print("\n6. DAILY OPERATIONS AUDIT")

# Check negative values
stock_columns = [
    "opening_stock",
    "stock_received",
    "units_sold",
    "waste_units",
    "closing_stock"
]

for column in stock_columns:

    negative_count = np.sum(operations[column] < 0)

    print("Negative", column, ":", negative_count)


# Verify closing stock formula
calculated_closing = (
    operations["opening_stock"]
    + operations["stock_received"]
    - operations["units_sold"]
    - operations["waste_units"]
)

formula_errors = np.sum(
    calculated_closing != operations["closing_stock"]
)

print("Stock formula errors:", formula_errors)


# Check duplicate daily records
daily_keys = np.column_stack((
    operations["day_index"],
    operations["outlet_id"],
    operations["product_code"]
))

unique_daily_keys = np.unique(daily_keys, axis=0)

duplicate_daily_records = (
    len(operations) - len(unique_daily_keys)
)

print("Duplicate daily records:", duplicate_daily_records)


# ------------------------------------------
# 7. FINAL AUDIT SUMMARY
# ------------------------------------------

print("\n========== AUDIT COMPLETED ==========")

print("Sales dataset audited successfully.")
print("Daily operations dataset audited successfully.")
