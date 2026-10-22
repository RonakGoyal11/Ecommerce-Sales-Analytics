"""RFM (Recency, Frequency, Monetary) logic for the Olist project.

Pure pandas/numpy so it can be unit-tested without a database.

Input grain: one row per ORDER ITEM (the grain of ``vw_master_sales``), with columns
``order_id``, ``customer_unique_id``, ``purchase_date``, ``product_price``, ``delivery_cost``.

Metric definitions (see README "Metric definitions"):
* Recency   - days from the customer's last purchase to ``reference_date``
              (reference date = latest purchase in the data + 1 day).
* Frequency - number of DISTINCT order_id values per customer (not item rows).
* Monetary  - sum of (product_price + delivery_cost) over all the customer's items.
"""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["order_id", "customer_unique_id", "purchase_date", "product_price", "delivery_cost"]

SEGMENT_ORDER = [
    "Champions",
    "Loyal Customers",
    "Potential Loyalists",
    "New Customers",
    "At Risk",
    "Lost / One-Time",
]


# --------------------------------------------------------------------------- data quality
def data_quality_report(df: pd.DataFrame) -> dict:
    """Run basic checks on the extract and return a dict of counts.

    Keys prefixed ``critical_`` make ``assert_data_quality`` fail; the rest are informational.
    """
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing required columns: {missing_cols}")
    
    dates = pd.to_datetime(df["purchase_date"], errors="coerce", format="mixed")
    report = {
        "rows": int(len(df)),
        "distinct_orders": int(df["order_id"].nunique()),
        "distinct_customers": int(df["customer_unique_id"].nunique()),
        "critical_missing_keys": int(df[["order_id", "customer_unique_id"]].isna().any(axis=1).sum()),
        "critical_invalid_or_missing_dates": int(dates.isna().sum()),
        "critical_negative_values": int(((df["product_price"] < 0) | (df["delivery_cost"] < 0)).sum()),
        "missing_price_or_freight": int(df[["product_price", "delivery_cost"]].isna().any(axis=1).sum()),
        "orders_with_multiple_customers": int(
            (df.groupby("order_id")["customer_unique_id"].nunique() > 1).sum()
        ),
        "orders_with_multiple_dates": int(
            (pd.Series(dates, index=df.index).groupby(df["order_id"]).nunique() > 1).sum()
        ),
    }
    if "order_item_id" in df.columns:
        report["critical_duplicate_order_item_keys"] = int(
            df.duplicated(subset=["order_id", "order_item_id"]).sum()
        )
    else:
        report["fully_duplicated_rows"] = int(df.duplicated().sum())
    if len(df) and dates.notna().any():
        report["date_min"] = str(dates.min().date())
        report["date_max"] = str(dates.max().date())
    return report


def assert_data_quality(report: dict) -> None:
    """Raise ValueError if any ``critical_`` check is non-zero."""
    problems = {k: v for k, v in report.items() if k.startswith("critical_") and v}
    if problems:
        raise ValueError(f"Data-quality checks failed: {problems}")


# --------------------------------------------------------------------------- RFM metrics
def compute_rfm(df: pd.DataFrame, reference_date: dt.date | pd.Timestamp | None = None) -> pd.DataFrame:
    """Return one row per customer_unique_id with Recency, Frequency, Monetary."""
    work = df.copy()
    work["purchase_date"] = pd.to_datetime(work["purchase_date"])
    work["total_value"] = work["product_price"].fillna(0) + work["delivery_cost"].fillna(0)

    if reference_date is None:
        reference_date = work["purchase_date"].max() + dt.timedelta(days=1)
    reference_date = pd.Timestamp(reference_date)

    grouped = work.groupby("customer_unique_id")
    rfm = pd.DataFrame(
        {
            "Recency": (reference_date - grouped["purchase_date"].max()).dt.days,
            "Frequency": grouped["order_id"].nunique(),  # distinct orders, NOT item rows
            "Monetary": grouped["total_value"].sum(),
        }
    ).reset_index()
    return rfm


def _quartile_score(values: pd.Series, higher_is_better: bool) -> pd.Series:
    """Score 1-4 using quartile cut-offs. Tied values always get the same score.

    Equivalent to ``pd.qcut(values, 4)`` when the quartile edges are unique, but never fails on
    duplicate edges and never splits identical values across groups.
    """
    q25, q50, q75 = np.quantile(values, [0.25, 0.5, 0.75])
    score = 1 + (values > q25).astype(int) + (values > q50).astype(int) + (values > q75).astype(int)
    return score if higher_is_better else 5 - score


def score_frequency(orders: int) -> int:
    """1, 2, 3 orders -> 1, 2, 3; four or more orders -> 4."""
    return int(min(max(orders, 1), 4))


def assign_segment(recency_score: int, frequency_orders: int, total_score: int) -> str:
    """Segment rules, evaluated top to bottom.

    One-time buyers (exactly 1 distinct order) can never be Champions or Loyal Customers:
      * R=4            -> New Customers
      * R=3            -> Potential Loyalists
      * R<=2           -> Lost / One-Time
    Repeat buyers (2+ distinct orders):
      * R<=2           -> At Risk (repeat customer who has gone quiet)
      * R>=3, total RFM score >= 10 -> Champions
      * R>=3, total RFM score >= 8  -> Loyal Customers
      * otherwise      -> Potential Loyalists
    """
    if frequency_orders <= 1:
        if recency_score == 4:
            return "New Customers"
        if recency_score == 3:
            return "Potential Loyalists"
        return "Lost / One-Time"
    if recency_score <= 2:
        return "At Risk"
    if total_score >= 10:
        return "Champions"
    if total_score >= 8:
        return "Loyal Customers"
    return "Potential Loyalists"


def add_scores_and_segments(rfm: pd.DataFrame) -> pd.DataFrame:
    """Add R/F/M scores, concatenated score, total score and Customer_Segment."""
    out = rfm.copy()
    out["R_Score"] = _quartile_score(out["Recency"], higher_is_better=False)
    out["M_Score"] = _quartile_score(out["Monetary"], higher_is_better=True)
    out["F_Score"] = out["Frequency"].apply(score_frequency)
    out["RFM_Concat"] = (
        out["R_Score"].astype(str) + out["F_Score"].astype(str) + out["M_Score"].astype(str)
    )
    out["RFM_Total_Score"] = out["R_Score"] + out["F_Score"] + out["M_Score"]
    out["Customer_Segment"] = [
        assign_segment(r, f, s)
        for r, f, s in zip(out["R_Score"], out["Frequency"], out["RFM_Total_Score"])
    ]
    return out


def build_rfm(df: pd.DataFrame, reference_date=None) -> pd.DataFrame:
    """Convenience wrapper: item-level extract -> scored, segmented customer table."""
    return add_scores_and_segments(compute_rfm(df, reference_date))
