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
# Project Base Directory
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

file_path = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "expenses_raw.csv"
)

# =========================
# Expected Columns
# =========================

EXPECTED_COLUMNS = [
    "Date",
    "Category",
    "Merchant",
    "Amount",
    "Payment_Method",
    "Location",
    "Note"
]

# =========================
# Load Dataset Function
# =========================

def load_expense_data():

    try:

        logging.info("Loading dataset...")

        df = pd.read_csv(file_path)

        logging.info("Dataset loaded successfully.")

        # Validate columns
        missing_columns = [
            col for col in EXPECTED_COLUMNS
            if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing columns: {missing_columns}"
            )

        logging.info("Schema validation successful.")

        return df

    except FileNotFoundError:
        logging.error("Dataset file not found.")

    except pd.errors.EmptyDataError:
        logging.error("CSV file is empty.")

    except Exception as e:
        logging.error(f"Error: {e}")

    return None

# =========================
# Main Execution
# =========================

if __name__ == "__main__":

    expense_df = load_expense_data()

    if expense_df is not None:

        print("\n✅ Dataset Preview:\n")

        print(expense_df.head())

        print("\n📊 Dataset Shape:")

        print(expense_df.shape)

        print("\n📋 Dataset Info:\n")

        print(expense_df.info())