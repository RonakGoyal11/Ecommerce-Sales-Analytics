"""
export_data.py
================
Writes every processed dataset the project produces to data/processed/,
in the exact form consumed by Power BI, SQL loading scripts, and the README.
"""

import pandas as pd

from src import config
from src.utils import get_logger, save_dataframe

logger = get_logger(__name__)


def export_all(orders_enriched: pd.DataFrame, customer_features: pd.DataFrame,
                product_features: pd.DataFrame, eda_results: dict) -> None:
    """Persist the cleaned/enriched dataset and every summary table used downstream."""
    save_dataframe(orders_enriched, config.CLEANED_CSV)
    save_dataframe(customer_features, config.CUSTOMER_SUMMARY_CSV)
    save_dataframe(product_features, config.PRODUCT_SUMMARY_CSV)
    save_dataframe(eda_results["monthly_trend"], config.MONTHLY_TREND_CSV)
    save_dataframe(eda_results["executive_kpis"], config.KPI_SUMMARY_CSV)

    logger.info("Exported cleaned dataset -> %s (%s rows)", config.CLEANED_CSV.name, len(orders_enriched))
    logger.info("Exported customer summary -> %s (%s rows)", config.CUSTOMER_SUMMARY_CSV.name, len(customer_features))
    logger.info("Exported product summary  -> %s (%s rows)", config.PRODUCT_SUMMARY_CSV.name, len(product_features))
    logger.info("Exported monthly trend    -> %s (%s rows)", config.MONTHLY_TREND_CSV.name, len(eda_results["monthly_trend"]))
    logger.info("Exported KPI summary      -> %s (%s rows)", config.KPI_SUMMARY_CSV.name, len(eda_results["executive_kpis"]))
