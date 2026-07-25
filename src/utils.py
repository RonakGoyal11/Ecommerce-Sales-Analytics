"""
utils.py
=========
Reusable, generic helper functions shared across the pipeline
(logging, formatting, saving artifacts). Nothing business-specific lives here.
"""

import logging
import sys
from pathlib import Path

import pandas as pd


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger that writes to stdout with a consistent format."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def format_currency(value: float, symbol: str = "$") -> str:
    """Format a number as a currency string with thousands separators.
    Negative values render as -$1,234.56 rather than $-1,234.56."""
    sign = "-" if value < 0 else ""
    return f"{sign}{symbol}{abs(value):,.2f}"


def format_percent(value: float, decimals: int = 1) -> str:
    """Format a fraction (0.15) as a percentage string ('15.0%')."""
    return f"{value * 100:.{decimals}f}%"


def save_dataframe(df: pd.DataFrame, path: Path, index: bool = False) -> None:
    """Save a DataFrame to CSV, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)


def print_section(title: str) -> None:
    """Print a visually distinct section header to the console/log."""
    bar = "=" * 70
    print(f"\n{bar}\n{title}\n{bar}")


def pct_change(new: float, old: float) -> float:
    """Safely compute percentage change, guarding against a zero denominator."""
    if old == 0:
        return 0.0
    return (new - old) / abs(old)
