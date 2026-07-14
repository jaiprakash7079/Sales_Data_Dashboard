import pandas as pd
import matplotlib.pyplot as plt

# Read CSV
df = pd.read_csv("Data/sales_data.csv")

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Create Sales Column
df["Sales"] = df["Quantity"] * df["Price"]

# Daily Sales
daily_sales = df.groupby("Date")["Sales"].sum()

print(daily_sales)

# Plot Graph
plt.figure(figsize=(10,5))

plt.plot(
    daily_sales.index,
    daily_sales.values,
    marker="o",
    linewidth=2
)

plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.grid(True)

plt.show()

# Category Wise Sales
category_sales = df.groupby("Category")["Sales"].sum()

print(category_sales)

plt.figure(figsize=(6,5))

plt.bar(category_sales.index, category_sales.values)

plt.title("Category Wise Sales")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.show()

plt.figure(figsize=(6,6))

plt.pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%"
)

plt.title("Sales Distribution")

plt.show()