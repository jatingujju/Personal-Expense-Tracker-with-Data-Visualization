import pandas as pd
import os
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
# File Path
# =========================

processed_file_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_expenses.csv"
)

# =========================
# Load Cleaned Dataset
# =========================

logging.info("Loading cleaned dataset...")

df = pd.read_csv(processed_file_path)

logging.info("Dataset loaded successfully.")

# =========================
# Convert Date Column
# =========================

df["Date"] = pd.to_datetime(df["Date"])

# =========================
# Total Spending
# =========================

total_spending = df["Amount"].sum()

# =========================
# Category-wise Spending
# =========================

category_spending = (
    df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

# =========================
# Monthly Spending Trend
# =========================

monthly_spending = (
    df.groupby("Month")["Amount"]
    .sum()
)

# =========================
# Payment Method Analysis
# =========================

payment_analysis = (
    df.groupby("Payment_Method")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

# =========================
# Highest Spending Category
# =========================

highest_category = category_spending.idxmax()

highest_category_amount = category_spending.max()

# =========================
# Top Merchants
# =========================

top_merchants = (
    df.groupby("Merchant")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

# =========================
# Daily Average Spending
# =========================

daily_average = df["Amount"].mean()

# =========================
# Output Results
# =========================

print("\n💰 TOTAL SPENDING")

print(f"₹ {total_spending:,.2f}")

# -------------------------

print("\n📊 CATEGORY-WISE SPENDING\n")

print(category_spending)

# -------------------------

print("\n📅 MONTHLY SPENDING TREND\n")

print(monthly_spending)

# -------------------------

print("\n💳 PAYMENT METHOD ANALYSIS\n")

print(payment_analysis)

# -------------------------

print("\n🔥 HIGHEST SPENDING CATEGORY\n")

print(f"{highest_category} → ₹ {highest_category_amount:,.2f}")

# -------------------------

print("\n🏪 TOP 5 MERCHANTS\n")

print(top_merchants)

# -------------------------

print("\n📈 DAILY AVERAGE SPENDING\n")

print(f"₹ {daily_average:,.2f}")