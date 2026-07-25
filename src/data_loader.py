"""
data_loader.py
================
Responsible for ONE thing: reading the raw Tableau Sample Superstore workbook
(Orders, People, Returns sheets) off disk and handing back raw, untouched
pandas DataFrames. No cleaning or transformation happens here.
"""

import pandas as pd

from src import config
from src.utils import get_logger, print_section

logger = get_logger(__name__)


def load_raw_workbook() -> dict:
    """
    Read all three sheets of the Sample Superstore workbook.

    Returns
    -------
    dict[str, pd.DataFrame]
        Keys: 'orders', 'people', 'returns'
    """
    if not config.RAW_EXCEL_FILE.exists():
        raise FileNotFoundError(
            f"Raw Excel file not found at {config.RAW_EXCEL_FILE}. "
            "Place the Sample Superstore workbook in data/raw/."
        )

    logger.info("Reading workbook: %s", config.RAW_EXCEL_FILE)
    excel_file = pd.ExcelFile(config.RAW_EXCEL_FILE)

    orders = pd.read_excel(excel_file, sheet_name=config.ORDERS_SHEET)
    people = pd.read_excel(excel_file, sheet_name=config.PEOPLE_SHEET)
    returns = pd.read_excel(excel_file, sheet_name=config.RETURNS_SHEET)

    logger.info("Orders sheet loaded: %s rows x %s columns", *orders.shape)
    logger.info("People sheet loaded: %s rows x %s columns", *people.shape)
    logger.info("Returns sheet loaded: %s rows x %s columns", *returns.shape)

    return {"orders": orders, "people": people, "returns": returns}


def profile_raw_data(data: dict) -> None:
    """
    Print a full data-quality audit of the raw sheets: schema, dtypes,
    missing values, duplicates, and a preview of the first rows.
    This is the mandatory "look before you touch" step run before any cleaning.
    """
    orders = data["orders"]

    print_section("SHEET NAMES")
    print(list(data.keys()))

    print_section("ORDERS: SHAPE")
    print(f"{orders.shape[0]} rows x {orders.shape[1]} columns")

    print_section("ORDERS: COLUMN NAMES")
    print(orders.columns.tolist())

    print_section("ORDERS: DATA TYPES")
    print(orders.dtypes)

    print_section("ORDERS: MISSING VALUES")
    missing = orders.isnull().sum()
    print(missing[missing > 0] if missing.any() else "No missing values found.")

    print_section("ORDERS: DUPLICATE ROWS")
    print(f"Full-row duplicates: {orders.duplicated().sum()}")
    print(f"Duplicate Row IDs:   {orders['Row ID'].duplicated().sum()}")

    print_section("ORDERS: FIRST 10 ROWS")
    print(orders.head(10).to_string())

    print_section("PEOPLE SHEET")
    print(data["people"].to_string())

    print_section("RETURNS SHEET: SAMPLE")
    print(data["returns"].head().to_string())
    print(f"\nDuplicate Order IDs in Returns (multi-line orders): "
          f"{data['returns']['Order ID'].duplicated().sum()}")


if __name__ == "__main__":
    raw = load_raw_workbook()
    profile_raw_data(raw)
