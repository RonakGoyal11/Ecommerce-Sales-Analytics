"""Project configuration, read from environment variables (optionally a .env file).

Nothing machine-specific or secret is stored in the repository. Copy
``.env.example`` to ``.env`` and edit it for your machine.
"""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote_plus

try:  # python-dotenv is optional at import time so the pure-logic tests run without it
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())
except ImportError:  # pragma: no cover
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent

# The nine CSV files shipped in the Kaggle "Brazilian E-Commerce Public Dataset by Olist".
EXPECTED_CSV_FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]


def get_data_dir() -> Path:
    """Folder holding the Olist CSVs. Defaults to ``<repo>/data/raw`` (git-ignored)."""
    raw = os.getenv("OLIST_DATA_DIR", "data/raw")
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path


def check_data_dir(path: Path | None = None) -> Path:
    """Return the data folder, or raise a clear error listing what is missing."""
    path = path or get_data_dir()
    if not path.is_dir():
        raise FileNotFoundError(
            f"Olist data folder not found: {path}\n"
            "Download the dataset (see README, 'Get the dataset') and either place the CSVs "
            "there or set OLIST_DATA_DIR in your .env file."
        )
    missing = [f for f in EXPECTED_CSV_FILES if not (path / f).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing Olist CSV files in {path}: {', '.join(missing)}")
    return path


def get_db_url() -> str:
    """Build the SQLAlchemy MySQL URL from DB_* environment variables."""
    password = os.getenv("DB_PASSWORD")
    if password is None:
        raise ValueError(
            "DB_PASSWORD is not set. Copy .env.example to .env and fill in your MySQL password."
        )
    user = os.getenv("DB_USER", "root")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "olist_ecommerce")
    return f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{name}"


def table_name_for(csv_file: str) -> str:
    """Map a CSV file name to its MySQL table name (e.g. olist_orders_dataset.csv -> orders)."""
    return csv_file.replace("olist_", "").replace("_dataset", "").replace(".csv", "")
