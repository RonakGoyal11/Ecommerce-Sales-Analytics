"""
config.py
==========
Centralized configuration for the E-Commerce Sales & Customer Analytics project.
No hardcoded paths or magic numbers should exist anywhere else in the codebase;
everything is defined once, here, and imported everywhere else.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# PROJECT ROOT & DIRECTORY LAYOUT
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

IMAGES_DIR = PROJECT_ROOT / "images"
REPORTS_DIR = PROJECT_ROOT / "reports"
SQL_DIR = PROJECT_ROOT / "sql"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"

for _dir in (PROCESSED_DATA_DIR, IMAGES_DIR, REPORTS_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# SOURCE FILE
# ---------------------------------------------------------------------------
RAW_EXCEL_FILE = RAW_DATA_DIR / "Sample_Superstore.xls"
ORDERS_SHEET = "Orders"
PEOPLE_SHEET = "People"
RETURNS_SHEET = "Returns"

# ---------------------------------------------------------------------------
# OUTPUT FILES
# ---------------------------------------------------------------------------
CLEANED_CSV = PROCESSED_DATA_DIR / "superstore_cleaned.csv"
CUSTOMER_SUMMARY_CSV = PROCESSED_DATA_DIR / "customer_summary.csv"
PRODUCT_SUMMARY_CSV = PROCESSED_DATA_DIR / "product_summary.csv"
MONTHLY_TREND_CSV = PROCESSED_DATA_DIR / "monthly_trend.csv"
KPI_SUMMARY_CSV = PROCESSED_DATA_DIR / "kpi_summary.csv"
INSIGHTS_MD = REPORTS_DIR / "business_insights.md"
EDA_SUMMARY_MD = REPORTS_DIR / "eda_summary.md"

# ---------------------------------------------------------------------------
# BUSINESS RULES / THRESHOLDS
# ---------------------------------------------------------------------------
HIGH_DISCOUNT_THRESHOLD = 0.30          # discounts above this are flagged "aggressive"
LOSS_MAKING_PROFIT_THRESHOLD = 0.0      # profit <= 0 is treated as a loss
TOP_N = 10                              # default "Top N" size for rankings
CHURN_INACTIVITY_DAYS = 180             # customers with no order in this window = at risk

# ---------------------------------------------------------------------------
# VISUAL STYLE
# ---------------------------------------------------------------------------
FIG_SIZE_STANDARD = (10, 6)
FIG_SIZE_WIDE = (14, 6)
FIG_DPI = 150
PALETTE = "viridis"
STYLE = "whitegrid"

CURRENCY_SYMBOL = "$"
RANDOM_STATE = 42
