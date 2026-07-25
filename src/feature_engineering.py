"""
feature_engineering.py
========================
Derives analytical features from the cleaned Orders table:
time features, profitability metrics, customer-level RFM-style features,
and discount/loss flags used throughout EDA, SQL modelling, and Power BI.
"""

import pandas as pd

from src import config
from src.utils import get_logger

logger = get_logger(__name__)


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add order-date derived calendar features."""
    df = df.copy()
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["order_month_name"] = df["order_date"].dt.strftime("%b")
    df["order_year_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["order_quarter"] = df["order_date"].dt.quarter
    df["order_weekday"] = df["order_date"].dt.day_name()
    df["shipping_delay_days"] = (df["ship_date"] - df["order_date"]).dt.days
    return df


def add_profitability_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add margin, loss flags, and discount-tier features."""
    df = df.copy()
    df["profit_margin"] = df["profit"] / df["sales"].replace(0, pd.NA)
    df["is_loss_making"] = (df["profit"] <= config.LOSS_MAKING_PROFIT_THRESHOLD).astype(int)
    df["is_high_discount"] = (df["discount"] >= config.HIGH_DISCOUNT_THRESHOLD).astype(int)

    def discount_tier(discount: float) -> str:
        if discount == 0:
            return "No Discount"
        elif discount <= 0.20:
            return "Low (0-20%)"
        elif discount <= 0.40:
            return "Medium (20-40%)"
        else:
            return "High (40%+)"

    df["discount_tier"] = df["discount"].apply(discount_tier)
    return df


def build_customer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate to one row per customer: RFM-style features used for
    customer segmentation and the Power BI "Top Customers" view.
    """
    snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)

    customer = df.groupby(["customer_id", "customer_name", "segment"], observed=True).agg(
        total_orders=("order_id", "nunique"),
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        avg_discount=("discount", "mean"),
        first_order_date=("order_date", "min"),
        last_order_date=("order_date", "max"),
    ).reset_index()

    customer["recency_days"] = (snapshot_date - customer["last_order_date"]).dt.days
    customer["customer_lifetime_days"] = (
        customer["last_order_date"] - customer["first_order_date"]
    ).dt.days
    customer["avg_order_value"] = customer["total_sales"] / customer["total_orders"]
    customer["is_at_risk"] = (customer["recency_days"] > config.CHURN_INACTIVITY_DAYS).astype(int)

    # Simple value tiering by total sales quartile
    customer["value_tier"] = pd.qcut(
        customer["total_sales"], q=4, labels=["Bronze", "Silver", "Gold", "Platinum"]
    )

    return customer.sort_values("total_sales", ascending=False)


def build_product_features(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate to one row per product for product-performance analysis.

    Note: this groups by (product_id, product_name, category, sub_category).
    32 product_ids in the raw Superstore data map to two slightly different
    product_name strings (a known upstream data quirk, not a pipeline bug),
    so this table has slightly more rows than the KPI table's distinct
    product_id count. See reports/business_insights.md for the verified count.
    """
    product = df.groupby(
        ["product_id", "product_name", "category", "sub_category"], observed=True
    ).agg(
        total_orders=("order_id", "nunique"),
        total_quantity_sold=("quantity", "sum"),
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        avg_discount=("discount", "mean"),
        return_count=("is_returned", "sum"),
    ).reset_index()

    product["profit_margin"] = product["total_profit"] / product["total_sales"]
    product["return_rate"] = product["return_count"] / product["total_orders"]

    return product.sort_values("total_sales", ascending=False)


def run_feature_pipeline(df_clean: pd.DataFrame) -> dict:
    """Run the full feature-engineering pipeline and return all derived tables."""
    df = add_time_features(df_clean)
    df = add_profitability_features(df)

    customer_features = build_customer_features(df)
    product_features = build_product_features(df)

    logger.info("Feature engineering complete: %s order-level features, "
                "%s customer profiles, %s product profiles.",
                df.shape[1], len(customer_features), len(product_features))

    return {
        "orders_enriched": df,
        "customer_features": customer_features,
        "product_features": product_features,
    }
