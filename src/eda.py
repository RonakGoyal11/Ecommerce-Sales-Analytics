"""
eda.py
=======
Exploratory Data Analysis functions that answer the core business questions:
top/bottom products, customer analysis, regional analysis, category analysis,
monthly trends, discount impact, profitability, and executive KPIs.

Each function returns a tidy DataFrame so it can be reused by visualization.py,
exported to CSV for Power BI, or printed directly for reports.
"""

import pandas as pd

from src import config
from src.utils import get_logger

logger = get_logger(__name__)


def executive_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Headline KPIs for the executive summary / Power BI KPI cards."""
    total_orders = df["order_id"].nunique()
    kpis = {
        "Total Revenue": df["sales"].sum(),
        "Total Profit": df["profit"].sum(),
        "Overall Profit Margin": df["profit"].sum() / df["sales"].sum(),
        "Total Orders": total_orders,
        "Total Line Items": len(df),
        "Total Customers": df["customer_id"].nunique(),
        "Total Products Sold": df["product_id"].nunique(),
        "Average Order Value": df["sales"].sum() / total_orders,
        "Average Discount": df["discount"].mean(),
        "Return Rate (%)": 100 * df["is_returned"].mean(),
        "Loss-Making Order Lines (%)": 100 * df["is_loss_making"].mean(),
    }
    return pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"])


def top_selling_products(df: pd.DataFrame, n: int = config.TOP_N) -> pd.DataFrame:
    """Top N products by revenue."""
    return (
        df.groupby("product_name", observed=True)
        .agg(total_sales=("sales", "sum"), total_quantity=("quantity", "sum"),
             total_profit=("profit", "sum"))
        .sort_values("total_sales", ascending=False)
        .head(n)
        .reset_index()
    )


def lowest_profit_products(df: pd.DataFrame, n: int = config.TOP_N) -> pd.DataFrame:
    """Products destroying the most profit (biggest cumulative losses)."""
    return (
        df.groupby("product_name", observed=True)
        .agg(total_sales=("sales", "sum"), total_profit=("profit", "sum"),
             avg_discount=("discount", "mean"))
        .sort_values("total_profit")
        .head(n)
        .reset_index()
    )


def customer_analysis(customer_features: pd.DataFrame, n: int = config.TOP_N) -> pd.DataFrame:
    """Top N customers by lifetime revenue."""
    cols = ["customer_name", "segment", "total_orders", "total_sales",
            "total_profit", "avg_order_value", "value_tier"]
    return customer_features.sort_values("total_sales", ascending=False)[cols].head(n)


def regional_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Sales, profit, and margin broken down by region."""
    out = df.groupby("region", observed=True).agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique"),
        avg_discount=("discount", "mean"),
    ).reset_index()
    out["profit_margin"] = out["total_profit"] / out["total_sales"]
    return out.sort_values("total_sales", ascending=False)


def category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Sales, profit, and margin broken down by category and sub-category."""
    out = df.groupby(["category", "sub_category"], observed=True).agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        avg_discount=("discount", "mean"),
    ).reset_index()
    out["profit_margin"] = out["total_profit"] / out["total_sales"]
    return out.sort_values("total_sales", ascending=False)


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly revenue, profit, and order-count trend across the full date range."""
    out = df.groupby("order_year_month", observed=True).agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique"),
    ).reset_index().sort_values("order_year_month")
    out["mom_sales_growth"] = out["total_sales"].pct_change()
    return out


def discount_impact(df: pd.DataFrame) -> pd.DataFrame:
    """How profit margin behaves across discount tiers -- the discount/profit trade-off."""
    out = df.groupby("discount_tier", observed=True).agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        avg_profit_margin=("profit_margin", "mean"),
        order_lines=("order_id", "count"),
    ).reset_index()
    tier_order = ["No Discount", "Low (0-20%)", "Medium (20-40%)", "High (40%+)"]
    out["discount_tier"] = pd.Categorical(out["discount_tier"], categories=tier_order, ordered=True)
    return out.sort_values("discount_tier")


def profitability_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    """Profitability broken down by customer segment and ship mode."""
    out = df.groupby(["segment", "ship_mode"], observed=True).agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique"),
    ).reset_index()
    out["profit_margin"] = out["total_profit"] / out["total_sales"]
    return out.sort_values("total_sales", ascending=False)


def return_rate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Return rate by category -- quality / customer-satisfaction proxy."""
    out = df.groupby("category", observed=True).agg(
        order_lines=("order_id", "count"),
        returned_lines=("is_returned", "sum"),
    ).reset_index()
    out["return_rate_pct"] = 100 * out["returned_lines"] / out["order_lines"]
    return out.sort_values("return_rate_pct", ascending=False)


def run_full_eda(df: pd.DataFrame, customer_features: pd.DataFrame) -> dict:
    """Run every EDA function and return results keyed by analysis name."""
    results = {
        "executive_kpis": executive_kpis(df),
        "top_selling_products": top_selling_products(df),
        "lowest_profit_products": lowest_profit_products(df),
        "customer_analysis": customer_analysis(customer_features),
        "regional_analysis": regional_analysis(df),
        "category_analysis": category_analysis(df),
        "monthly_trend": monthly_trend(df),
        "discount_impact": discount_impact(df),
        "profitability_by_segment": profitability_by_segment(df),
        "return_rate_by_category": return_rate_by_category(df),
    }
    logger.info("EDA complete: %s analyses generated.", len(results))
    return results
