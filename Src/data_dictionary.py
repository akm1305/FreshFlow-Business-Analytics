
import numpy as np

# Load sales dataset
sales = np.genfromtxt(
    "freshflow_sales.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

# Load daily operations dataset
operations = np.genfromtxt(
    "../datasets/freshflow_daily_operations.csv",
    delimiter=",",
    names=True,
    dtype=None,
    encoding="utf-8"
)

# Display Sales Dataset Dictionary
print("========== SALES DATASET ==========")

for column in sales.dtype.names:
    print(column)

print("\nSales Dataset Shape:", sales.shape)

# Display Operations Dataset Dictionary
print("\n===== DAILY OPERATIONS DATASET =====")

for column in operations.dtype.names:
    print(column)

print("\nOperations Dataset Shape:", operations.shape)
