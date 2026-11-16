
import numpy as np

# ==========================================
# D3: DATA CLEANING AND ANALYTICAL ARRAYS
# ==========================================

# Load original sales dataset
sales = np.genfromtxt(
    "freshflow_sales.csv",
    delimiter=",",
    names=True,
    dtype=float,
    encoding="utf-8"
)

# Load daily operations dataset
operations = np.genfromtxt(
    "../datasets/freshflow_daily_operations.csv",
    delimiter=",",
    names=True,
    dtype=float,
    encoding="utf-8"
)

print("========== D3: DATA CLEANING ==========")

print("\nOriginal sales records:", len(sales))


# ------------------------------------------
# STEP 1: REMOVE DUPLICATE TRANSACTIONS
# ------------------------------------------

# Find first occurrence of every transaction ID
valid_id_rows = np.isfinite(sales["transaction_id"])

sales_with_ids = sales[valid_id_rows]

_, first_indices = np.unique(
    sales_with_ids["transaction_id"],
    return_index=True
)

# Keep the first occurrence of each ID
unique_indices = np.sort(first_indices)

sales_unique = sales_with_ids[unique_indices]

print("\nAfter removing duplicate IDs:", len(sales_unique))
print("Duplicates removed:", len(sales) - len(sales_unique))


# ------------------------------------------
# STEP 2: CHECK ESSENTIAL VALUES
# ------------------------------------------

# Required columns must not contain missing values
required_columns = [
    "day_index",
    "outlet_id",
    "product_code",
    "category_code",
    "quantity",
    "unit_price",
    "unit_cost",
    "discount_rate",
    "stock_before_units",
    "payment_code"
]

valid_rows = np.ones(len(sales_unique), dtype=bool)

for column in required_columns:
    valid_rows &= np.isfinite(sales_unique[column])

# Customer rating is optional, so missing ratings are retained.


# ------------------------------------------
# STEP 3: REMOVE INVALID VALUES
# ------------------------------------------

valid_rows &= (
    (sales_unique["day_index"] >= 1) &
    (sales_unique["day_index"] <= 30)
)

valid_rows &= (
    (sales_unique["outlet_id"] >= 1) &
    (sales_unique["outlet_id"] <= 3)
)

valid_rows &= (
    (sales_unique["product_code"] >= 1) &
    (sales_unique["product_code"] <= 8)
)

valid_rows &= sales_unique["quantity"] > 0

valid_rows &= sales_unique["unit_price"] > 0

valid_rows &= sales_unique["unit_cost"] > 0

valid_rows &= (
    (sales_unique["discount_rate"] >= 0) &
    (sales_unique["discount_rate"] <= 1)
)

valid_rows &= sales_unique["stock_before_units"] >= 0

valid_rows &= (
    (sales_unique["payment_code"] >= 1) &
    (sales_unique["payment_code"] <= 4)
)

# Keep only valid records
clean_sales = sales_unique[valid_rows].copy()

print("\nAfter removing invalid records:", len(clean_sales))
print("Invalid records removed:", len(sales_unique) - len(clean_sales))


# ------------------------------------------
# STEP 4: CORRECT PRODUCT CATEGORY MISMATCH
# ------------------------------------------

# Product to category mapping
expected_category = np.array([
    1, 1, 1, 1, 2, 2, 3, 4
])

product_codes = clean_sales["product_code"].astype(int)

correct_categories = expected_category[product_codes - 1]

mismatch_count = np.sum(
    clean_sales["category_code"] != correct_categories
)

# Correct the category according to product code
clean_sales["category_code"] = correct_categories

print("\nProduct-category mismatches corrected:", mismatch_count)


# ------------------------------------------
# STEP 5: HANDLE MISSING CUSTOMER RATINGS
# ------------------------------------------

missing_ratings = np.sum(
    ~np.isfinite(clean_sales["customer_rating"])
)

print("\nMissing customer ratings retained:", missing_ratings)

# Handle invalid customer ratings
invalid_ratings = (
    np.isfinite(clean_sales["customer_rating"]) &
    (
        (clean_sales["customer_rating"] < 1) |
        (clean_sales["customer_rating"] > 5)
    )
)

print(
    "Invalid ratings converted to missing:",
    np.sum(invalid_ratings)
)

clean_sales["customer_rating"][invalid_ratings] = np.nan

# ------------------------------------------
# STEP 6: CREATE NUMPY ANALYTICAL ARRAY
# ------------------------------------------

# Convert structured data into a regular NumPy array
clean_sales_array = np.column_stack([
    clean_sales[column]
    for column in sales.dtype.names
])

print("\nClean sales array shape:", clean_sales_array.shape)


# ------------------------------------------
# STEP 7: PREPARE OPERATIONS ARRAY
# ------------------------------------------

operations_array = np.column_stack([
    operations[column]
    for column in operations.dtype.names
])

print("Operations array shape:", operations_array.shape)


# ------------------------------------------
# STEP 8: SAVE CLEANED DATA
# ------------------------------------------

np.savetxt(
    "../datasets/freshflow_sales_cleaned.csv",
    clean_sales_array,
    delimiter=",",
    header=",".join(sales.dtype.names),
    comments="",
    fmt="%.2f"
)

# Save operations data separately without modifying it
np.savetxt(
    "../datasets/freshflow_operations_cleaned.csv",
    operations_array,
    delimiter=",",
    header=",".join(operations.dtype.names),
    comments="",
    fmt="%.2f"
)


# ------------------------------------------
# STEP 9: FINAL SUMMARY
# ------------------------------------------

print("\n========== CLEANING SUMMARY ==========")

print("Original sales records:", len(sales))
print("Clean sales records:", len(clean_sales))
print("Records removed:", len(sales) - len(clean_sales))

print("Operations records:", len(operations))

print("\nCleaned sales file saved successfully!")
print("Cleaned operations file saved successfully!")

print("\nD3 COMPLETED SUCCESSFULLY!")
