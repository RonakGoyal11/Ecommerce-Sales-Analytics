"""
main.py
========
End-to-end pipeline entry point.

Run with:
    python -m src.main

Steps executed:
    1. Load raw Excel workbook (Orders, People, Returns) + data audit.
    2. Clean and merge data.
    3. Engineer features (time, profitability, customer, product).
    4. Run full EDA (business questions).
    5. Export processed CSVs for SQL / Power BI.
    6. Generate all chart images.
    7. Generate the written business insights report.
"""

from src import data_loader, data_cleaning, feature_engineering, eda, visualization, business_insights, export_data
from src.utils import get_logger, print_section

logger = get_logger(__name__)


def run_pipeline() -> None:
    print_section("STEP 1/7: LOADING RAW DATA")
    raw = data_loader.load_raw_workbook()
    data_loader.profile_raw_data(raw)

    print_section("STEP 2/7: CLEANING & MERGING DATA")
    df_clean = data_cleaning.run_cleaning_pipeline(raw)
    logger.info("Cleaned dataset shape: %s rows x %s columns", *df_clean.shape)

    print_section("STEP 3/7: FEATURE ENGINEERING")
    features = feature_engineering.run_feature_pipeline(df_clean)
    orders_enriched = features["orders_enriched"]
    customer_features = features["customer_features"]
    product_features = features["product_features"]

    print_section("STEP 4/7: EXPLORATORY DATA ANALYSIS")
    eda_results = eda.run_full_eda(orders_enriched, customer_features)
    for name, table in eda_results.items():
        print(f"\n--- {name} ---")
        print(table.head(10).to_string(index=False))

    print_section("STEP 5/7: EXPORTING PROCESSED DATA")
    export_data.export_all(orders_enriched, customer_features, product_features, eda_results)

    print_section("STEP 6/7: GENERATING VISUALIZATIONS")
    visualization.generate_all_visuals(orders_enriched, eda_results, customer_features)

    print_section("STEP 7/7: GENERATING BUSINESS INSIGHTS REPORT")
    report = business_insights.generate_insights(orders_enriched, eda_results, customer_features, product_features)
    business_insights.save_insights_report(report)

    print_section("PIPELINE COMPLETE")
    logger.info("All processed data, charts, and reports have been generated successfully.")


if __name__ == "__main__":
    run_pipeline()
