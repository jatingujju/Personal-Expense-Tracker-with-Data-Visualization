import pandas as pd
import os
import plotly.express as px
import logging

# =========================
# Logging Configuration
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# Base Directory
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# =========================
# File Paths
# =========================

processed_file_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_expenses.csv"
)

charts_output_path = os.path.join(
    BASE_DIR,
    "outputs",
    "charts"
)

os.makedirs(charts_output_path, exist_ok=True)

# =========================
# Load Dataset
# =========================

logging.info("Loading cleaned dataset...")

df = pd.read_csv(processed_file_path)

logging.info("Dataset loaded successfully.")

# =========================
# Category-wise Spending
# =========================

category_spending = (
    df.groupby("Category")["Amount"]
    .sum()
    .reset_index()
)

# =========================
# Monthly Spending
# =========================

monthly_spending = (
    df.groupby("Month")["Amount"]
    .sum()
    .reset_index()
)

# =========================
# Payment Method Analysis
# =========================

payment_spending = (
    df.groupby("Payment_Method")["Amount"]
    .sum()
    .reset_index()
)

# =========================
# Category Donut Chart
# =========================

fig1 = px.pie(
    category_spending,
    names="Category",
    values="Amount",
    hole=0.5,
    title="Category-wise Expense Distribution"
)

fig1.write_html(
    os.path.join(
        charts_output_path,
        "category_distribution.html"
    )
)

# =========================
# Monthly Trend Chart
# =========================

fig2 = px.line(
    monthly_spending,
    x="Month",
    y="Amount",
    markers=True,
    title="Monthly Expense Trend"
)

fig2.write_html(
    os.path.join(
        charts_output_path,
        "monthly_trend.html"
    )
)

# =========================
# Payment Method Bar Chart
# =========================

fig3 = px.bar(
    payment_spending,
    x="Payment_Method",
    y="Amount",
    title="Payment Method Analysis",
    text_auto=True
)

fig3.write_html(
    os.path.join(
        charts_output_path,
        "payment_analysis.html"
    )
)

# =========================
# Success Messages
# =========================

print("\n✅ Visualizations Generated Successfully!\n")

print("📊 Charts Saved In:")

print(charts_output_path)

print("\n📁 Generated Files:")

print("1. category_distribution.html")
print("2. monthly_trend.html")
print("3. payment_analysis.html")