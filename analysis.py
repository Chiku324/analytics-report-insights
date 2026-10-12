"""
Analytics Report & Insights Documentation
Dataset: ecommerce_sales_sample.csv (synthetic demonstration data)
Run: pip install pandas matplotlib
     python analysis.py
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "ecommerce_sales_sample.csv", parse_dates=["Order_Date"])
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# Basic data-quality checks
print("Rows:", len(df))
print("Duplicate order IDs:", df["Order_ID"].duplicated().sum())
print("Missing values by column:\\n", df.isna().sum())
print("Negative revenue rows:", (df["Revenue_INR"] < 0).sum())

# Key performance indicators
revenue = df["Revenue_INR"].sum()
profit = df["Profit_INR"].sum()
orders = df["Order_ID"].nunique()
units = df["Quantity"].sum()
print(f"Total revenue: INR {revenue:,.2f}")
print(f"Total profit: INR {profit:,.2f}")
print(f"Orders: {orders:,}")
print(f"Units sold: {units:,}")
print(f"Average order revenue: INR {revenue / orders:,.2f}")
print(f"Profit margin: {profit / revenue * 100:.2f}%")

# Grouped summaries
print("\\nRevenue and profit by category:")
print(df.groupby("Category")[["Revenue_INR", "Profit_INR"]].sum().sort_values("Revenue_INR", ascending=False))
print("\\nRevenue by region:")
print(df.groupby("Region")["Revenue_INR"].sum().sort_values(ascending=False))
print("\\nRevenue by sales channel:")
print(df.groupby("Sales_Channel")["Revenue_INR"].sum().sort_values(ascending=False))

# Save reproducible charts
out = ROOT / "charts"
out.mkdir(exist_ok=True)
monthly = df.groupby("Month")["Revenue_INR"].sum()
monthly.plot(marker="o", title="Monthly Revenue Trend")
plt.ylabel("Revenue (INR)"); plt.tight_layout()
plt.savefig(out / "monthly_revenue.png", dpi=160); plt.close()

df.groupby("Category")["Revenue_INR"].sum().sort_values().plot(kind="barh", title="Revenue by Category")
plt.xlabel("Revenue (INR)"); plt.tight_layout()
plt.savefig(out / "category_revenue.png", dpi=160); plt.close()
