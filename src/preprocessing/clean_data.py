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
# File Paths
# =========================

raw_file_path = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "expenses_raw.csv"
)

processed_file_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_expenses.csv"
)

# =========================
# Load Dataset
# =========================

logging.info("Loading raw dataset...")

df = pd.read_csv(raw_file_path)

logging.info("Dataset loaded successfully.")

# =========================
# Data Cleaning
# =========================

logging.info("Starting data cleaning process...")

# Remove duplicates
initial_rows = len(df)

df.drop_duplicates(inplace=True)

duplicates_removed = initial_rows - len(df)

logging.info(f"Duplicates removed: {duplicates_removed}")

# Handle missing values
missing_values = df.isnull().sum().sum()

logging.info(f"Missing values found: {missing_values}")

df.dropna(inplace=True)

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Normalize category names
df["Category"] = df["Category"].str.strip().str.title()

# Ensure amount is positive
df = df[df["Amount"] > 0]

# =========================
# Outlier Detection
# =========================

Q1 = df["Amount"].quantile(0.25)

Q3 = df["Amount"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR

upper_bound = Q3 + 1.5 * IQR

outliers = df[
    (df["Amount"] < lower_bound) |
    (df["Amount"] > upper_bound)
]

logging.info(f"Outliers detected: {len(outliers)}")

# =========================
# Feature Engineering
# =========================

df["Year"] = df["Date"].dt.year

df["Month"] = df["Date"].dt.month_name()

df["Day"] = df["Date"].dt.day_name()

# =========================
# Save Cleaned Dataset
# =========================

os.makedirs(
    os.path.dirname(processed_file_path),
    exist_ok=True
)

df.to_csv(processed_file_path, index=False)

logging.info("Cleaned dataset saved successfully.")

# =========================
# Output Information
# =========================

print("\n✅ Data Cleaning Completed Successfully!\n")

print("📊 Cleaned Dataset Shape:")

print(df.shape)

print("\n📋 Dataset Preview:\n")

print(df.head())

print("\n🚨 Outlier Summary:")

print(outliers[["Category", "Amount"]].head())