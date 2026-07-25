"""
data_cleaning.py
==================
Cleans the raw Orders sheet and merges in People (regional managers) and
Returns (return status) so downstream modules work off one tidy DataFrame.

Cleaning steps performed (in order):
    1. Standardize column names to snake_case.
    2. Enforce correct dtypes (dates, categoricals).
    3. Handle missing Postal Code values.
    4. Remove exact duplicate rows (defensive - none expected in this dataset).
    5. Merge Region -> Regional Manager from the People sheet.
    6. Merge Order ID -> Returned flag from the Returns sheet.
    7. Trim whitespace on all text columns.
    8. Validate value ranges (Discount 0-1, Quantity > 0, Sales > 0).
"""

import pandas as pd

from src.utils import get_logger

logger = get_logger(__name__)

COLUMN_RENAME_MAP = {
    "Row ID": "row_id",
    "Order ID": "order_id",
    "Order Date": "order_date",
    "Ship Date": "ship_date",
    "Ship Mode": "ship_mode",
    "Customer ID": "customer_id",
    "Customer Name": "customer_name",
    "Segment": "segment",
    "Country/Region": "country",
    "City": "city",
    "State": "state",
    "Postal Code": "postal_code",
    "Region": "region",
    "Product ID": "product_id",
    "Category": "category",
    "Sub-Category": "sub_category",
    "Product Name": "product_name",
    "Sales": "sales",
    "Quantity": "quantity",
    "Discount": "discount",
    "Profit": "profit",
}


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Standardize dtypes, names, and handle missing/invalid values in Orders."""
    df = orders.copy()

    # 1. Standardize column names
    df = df.rename(columns=COLUMN_RENAME_MAP)

    # 2. Enforce dtypes
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])
    for col in ["ship_mode", "segment", "country", "city", "state", "region",
                "category", "sub_category"]:
        df[col] = df[col].astype("category")

    # 3. Missing Postal Code -> known ZIP for Burlington, VT (the only city
    #    in this dataset with nulls here) - documented, not silently dropped.
    missing_before = df["postal_code"].isnull().sum()
    if missing_before:
        burlington_mask = (df["city"] == "Burlington") & (df["state"] == "Vermont")
        df.loc[burlington_mask & df["postal_code"].isnull(), "postal_code"] = 5401
        remaining = df["postal_code"].isnull().sum()
        logger.info(
            "Postal Code: %s missing values found, %s resolved via city/state lookup, "
            "%s left as null.", missing_before, missing_before - remaining, remaining
        )
    df["postal_code"] = df["postal_code"].astype("Int64")

    # 4. Drop exact duplicate rows (defensive)
    before = len(df)
    df = df.drop_duplicates()
    logger.info("Duplicate rows removed: %s", before - len(df))

    # 7. Trim whitespace on text columns
    text_cols = df.select_dtypes(include="object").columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # 8. Validate business-rule ranges
    invalid_discount = ((df["discount"] < 0) | (df["discount"] > 1)).sum()
    invalid_quantity = (df["quantity"] <= 0).sum()
    invalid_sales = (df["sales"] <= 0).sum()
    if invalid_discount or invalid_quantity or invalid_sales:
        logger.warning(
            "Validation flags -> discount out of [0,1]: %s | quantity<=0: %s | sales<=0: %s",
            invalid_discount, invalid_quantity, invalid_sales
        )
    else:
        logger.info("Validation passed: discount, quantity, and sales are within expected ranges.")

    return df


def merge_reference_data(orders_clean: pd.DataFrame, people: pd.DataFrame,
                          returns: pd.DataFrame) -> pd.DataFrame:
    """Enrich cleaned orders with regional manager and return status."""
    df = orders_clean.copy()

    # Merge regional manager (People sheet)
    people_clean = people.rename(columns={
        "Regional Manager": "regional_manager", "Region": "region"
    })
    df = df.merge(people_clean, on="region", how="left")

    # Merge return status (Returns sheet, one row per Order ID, deduplicated)
    returns_clean = returns.rename(columns={"Returned": "returned", "Order ID": "order_id"})
    returns_unique = returns_clean.drop_duplicates(subset="order_id")
    df = df.merge(returns_unique, on="order_id", how="left")
    df["returned"] = df["returned"].fillna("No")
    df["is_returned"] = (df["returned"] == "Yes").astype(int)

    logger.info(
        "Reference data merged. Returned orders: %s of %s line items (%.2f%%)",
        df["is_returned"].sum(), len(df), 100 * df["is_returned"].mean()
    )
    return df


def run_cleaning_pipeline(raw_data: dict) -> pd.DataFrame:
    """Full cleaning pipeline: clean Orders, then enrich with People + Returns."""
    orders_clean = clean_orders(raw_data["orders"])
    full = merge_reference_data(orders_clean, raw_data["people"], raw_data["returns"])
    return full
