import pandas as pd
import random

random.seed(42)

data = []

for day in range(1, 31):
    for outlet in range(1, 4):
        for product in range(1, 9):

            opening_stock = random.randint(20, 150)
            stock_received = random.randint(0, 50)

            available_stock = opening_stock + stock_received

            units_sold = random.randint(0, available_stock)
            remaining_stock = available_stock - units_sold

            waste_units = random.randint(0, remaining_stock)

            closing_stock = (
                opening_stock
                + stock_received
                - units_sold
                - waste_units
            )
            data.append({
                'Day_Index': day,
                'Outlet_ID': outlet,
                'Product_Code': product,
                'Opening_Stock': opening_stock,
                'Stock_Received': stock_received,
                'Units_Sold': units_sold,
                'Waste_Units': waste_units,
                'Closing_Stock': closing_stock
            })

df = pd.DataFrame(data)
    
df.to_csv('retail_inventory_dataset.csv', index=False)

print("Dataset created successfully!")
print(df.head(10))

print("\nTotal Rows:", len(df))
print("\nDataset Information:")
print(df.info())
