
import numpy as np

# ---------------------------------------
# FRESHFLOW DAILY OPERATIONS DATASET
# ---------------------------------------

# Load the original sales dataset
sales = np.genfromtxt("freshflow_sales.csv",
    delimiter=",",
    names=True,
    dtype=float,
    encoding="utf-8"
)

# Random generator for reproducible results
rng = np.random.default_rng(42)

# Create an empty list for operations records
operations = []

# Remove duplicate transaction IDs and retain the first occurrence
transaction_ids = sales["transaction_id"]
seen_ids = set()

# Aggregate valid sales quantities by day, outlet and product
sales_summary = {}

for record in sales:

    transaction_id = record["transaction_id"]
    day = record["day_index"]
    outlet = record["outlet_id"]
    product = record["product_code"]
    quantity = record["quantity"]

    # Skip missing or invalid values
    if not all(np.isfinite(x) for x in
               [transaction_id, day, outlet, product, quantity]):
        continue

    # Skip duplicate transaction IDs
    if transaction_id in seen_ids:
        continue

    seen_ids.add(transaction_id)

    # Validate day, outlet, product and quantity
    if not (1 <= day <= 30):
        continue

    if not (1 <= outlet <= 3):
        continue

    if not (1 <= product <= 8):
        continue

    if quantity <= 0:
        continue

    key = (int(day), int(outlet), int(product))

    sales_summary[key] = (
        sales_summary.get(key, 0) + int(quantity)
    )


# Generate all 720 combinations
for day in range(1, 31):

    for outlet in range(1, 4):

        for product in range(1, 9):

            key = (day, outlet, product)

            # Sales quantity from the sales dataset
            units_sold = sales_summary.get(key, 0)

            # Generate opening stock
            opening_stock = int(rng.integers(35, 61))

            # Generate waste units
            waste_units = int(rng.integers(0, 4))

            # Generate stock received
            stock_received = int(rng.integers(0, 21))

            # Ensure sufficient stock is available
            required_stock = units_sold + waste_units

            if opening_stock + stock_received < required_stock:
                stock_received += (
                    required_stock - opening_stock - stock_received
                )

            # Calculate closing stock
            closing_stock = (
                opening_stock
                + stock_received
                - units_sold
                - waste_units
            )

            operations.append([
                day,
                outlet,
                product,
                opening_stock,
                stock_received,
                units_sold,
                waste_units,
                closing_stock
            ])


# Convert operations into a NumPy array
operations_array = np.array(operations, dtype=int)

# Define CSV column names
headers = [
    "day_index",
    "outlet_id",
    "product_code",
    "opening_stock",
    "stock_received",
    "units_sold",
    "waste_units",
    "closing_stock"
]

# Save the dataset as CSV
np.savetxt(
    "../datasets/freshflow_daily_operations.csv",
    operations_array,
    delimiter=",",
    header=",".join(headers),
    comments="",
    fmt="%d"
)

# ---------------------------------------
# VALIDATION
# ---------------------------------------

print("Daily operations dataset created successfully!")

print("Number of records:", len(operations_array))
print("Number of columns:", operations_array.shape[1])

# Verify stock calculation
check = (
    operations_array[:, 3]
    + operations_array[:, 4]
    - operations_array[:, 5]
    - operations_array[:, 6]
)

print(
    "Stock calculation valid:",
    np.array_equal(check, operations_array[:, 7])
)

print("\nFirst 5 records:")
print(operations_array[:5])
