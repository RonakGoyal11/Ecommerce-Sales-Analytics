"""
visualization.py
==================
Generates all chart images used in the README, reports, and presentation.
Every chart is saved as a PNG into the images/ directory at report-ready
resolution (150 DPI), with consistent styling defined in config.py.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

from src import config
from src.utils import get_logger

logger = get_logger(__name__)

sns.set_style(config.STYLE)
plt.rcParams["figure.dpi"] = config.FIG_DPI
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.titleweight"] = "bold"


def _save(fig, filename: str) -> None:
    path = config.IMAGES_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=config.FIG_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved chart: %s", path.name)


def plot_top_selling_products(top_products: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=config.FIG_SIZE_STANDARD)
    data = top_products.sort_values("total_sales")
    sns.barplot(data=data, x="total_sales", y="product_name", hue="product_name",
                palette=config.PALETTE, legend=False, ax=ax)
    ax.set_title("Top 10 Products by Revenue")
    ax.set_xlabel("Total Sales ($)")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    _save(fig, "top_selling_products.png")


def plot_lowest_profit_products(lowest_products: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=config.FIG_SIZE_STANDARD)
    data = lowest_products.sort_values("total_profit")
    sns.barplot(data=data, x="total_profit", y="product_name", hue="product_name",
                palette="rocket", legend=False, ax=ax)
    ax.set_title("Top 10 Profit-Destroying Products")
    ax.set_xlabel("Total Profit ($)")
    ax.set_ylabel("")
    ax.axvline(0, color="black", linewidth=0.8)
    _save(fig, "lowest_profit_products.png")


def plot_regional_analysis(regional: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=config.FIG_SIZE_WIDE)
    sns.barplot(data=regional, x="region", y="total_sales", hue="region",
                palette=config.PALETTE, legend=False, ax=axes[0])
    axes[0].set_title("Revenue by Region")
    axes[0].set_ylabel("Total Sales ($)")
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:,.0f}K"))

    sns.barplot(data=regional, x="region", y="profit_margin", hue="region",
                palette="mako", legend=False, ax=axes[1])
    axes[1].set_title("Profit Margin by Region")
    axes[1].set_ylabel("Profit Margin")
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x*100:.0f}%"))
    _save(fig, "regional_analysis.png")


def plot_category_analysis(category: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=config.FIG_SIZE_WIDE)
    cat_summary = category.groupby("category", observed=True)[["total_sales", "total_profit"]].sum().reset_index()
    cat_melt = cat_summary.melt(id_vars="category", var_name="metric", value_name="amount")
    sns.barplot(data=cat_melt, x="category", y="amount", hue="metric", palette="viridis", ax=ax)
    ax.set_title("Sales vs Profit by Category")
    ax.set_ylabel("Amount ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:,.0f}K"))
    ax.legend(title="")
    _save(fig, "category_analysis.png")


def plot_monthly_trend(monthly: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=config.FIG_SIZE_WIDE)
    ax.plot(monthly["order_year_month"], monthly["total_sales"], marker="o",
            color="#2E86AB", label="Sales")
    ax2 = ax.twinx()
    ax2.plot(monthly["order_year_month"], monthly["total_profit"], marker="s",
             color="#A23B72", label="Profit")
    ax.set_title("Monthly Sales & Profit Trend (2018-2021)")
    ax.set_ylabel("Sales ($)")
    ax2.set_ylabel("Profit ($)")
    ax.set_xticks(range(0, len(monthly), 3))
    ax.set_xticklabels(monthly["order_year_month"].iloc[::3], rotation=45, ha="right")
    fig.legend(loc="upper left", bbox_to_anchor=(0.08, 0.9))
    _save(fig, "monthly_trend.png")


def plot_discount_impact(discount_df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=config.FIG_SIZE_STANDARD)
    sns.barplot(data=discount_df, x="discount_tier", y="avg_profit_margin", hue="discount_tier",
                palette="rocket_r", legend=False, ax=ax)
    ax.set_title("Discount Level vs Average Profit Margin")
    ax.set_xlabel("Discount Tier")
    ax.set_ylabel("Average Profit Margin")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x*100:.0f}%"))
    _save(fig, "discount_impact.png")


def plot_customer_value_tiers(customer_features: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=config.FIG_SIZE_STANDARD)
    tier_summary = customer_features.groupby("value_tier", observed=True).agg(
        customers=("customer_id", "count"), total_sales=("total_sales", "sum")
    ).reset_index()
    sns.barplot(data=tier_summary, x="value_tier", y="total_sales", hue="value_tier",
                palette="crest", legend=False, ax=ax)
    ax.set_title("Revenue Contribution by Customer Value Tier")
    ax.set_xlabel("Customer Tier")
    ax.set_ylabel("Total Sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:,.0f}K"))
    _save(fig, "customer_value_tiers.png")


def plot_segment_profitability(segment_df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=config.FIG_SIZE_WIDE)
    pivot = segment_df.pivot_table(index="segment", columns="ship_mode",
                                    values="profit_margin", aggfunc="mean")
    sns.heatmap(pivot, annot=True, fmt=".1%", cmap="RdYlGn", center=0, ax=ax,
                cbar_kws={"label": "Profit Margin"})
    ax.set_title("Profit Margin: Segment x Ship Mode")
    _save(fig, "segment_profitability_heatmap.png")


def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=config.FIG_SIZE_STANDARD)
    numeric_cols = ["sales", "quantity", "discount", "profit", "profit_margin", "shipping_delay_days"]
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax, square=True)
    ax.set_title("Correlation Matrix: Key Numeric Features")
    _save(fig, "correlation_heatmap.png")


def generate_all_visuals(df: pd.DataFrame, eda_results: dict, customer_features: pd.DataFrame) -> None:
    """Generate and save every chart in the project."""
    plot_top_selling_products(eda_results["top_selling_products"])
    plot_lowest_profit_products(eda_results["lowest_profit_products"])
    plot_regional_analysis(eda_results["regional_analysis"])
    plot_category_analysis(eda_results["category_analysis"])
    plot_monthly_trend(eda_results["monthly_trend"])
    plot_discount_impact(eda_results["discount_impact"])
    plot_customer_value_tiers(customer_features)
    plot_segment_profitability(eda_results["profitability_by_segment"])
    plot_correlation_heatmap(df)
    logger.info("All visualizations generated in %s", config.IMAGES_DIR)
