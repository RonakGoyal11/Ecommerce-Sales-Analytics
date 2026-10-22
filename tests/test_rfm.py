"""Unit tests for python/rfm.py.

ALL DATA HERE IS SYNTHETIC and exists only to test the logic. None of it is Olist data and
none of it may be quoted as a business finding.
"""
import datetime as dt
import itertools
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "python"))

import rfm  # noqa: E402


def _row(order_id, customer, date, price, freight, item=1):
    return {
        "order_id": order_id,
        "order_item_id": item,
        "customer_unique_id": customer,
        "purchase_date": date,
        "product_price": price,
        "delivery_cost": freight,
    }


@pytest.fixture
def synthetic_items():
    rows = [
        # cust_multi_item: ONE order with THREE item rows -> Frequency must be 1
        _row("o1", "cust_multi_item", "2018-08-01", 10.0, 1.0, item=1),
        _row("o1", "cust_multi_item", "2018-08-01", 20.0, 2.0, item=2),
        _row("o1", "cust_multi_item", "2018-08-01", 30.0, 3.0, item=3),
        # cust_repeat: TWO distinct orders -> Frequency 2
        _row("o2", "cust_repeat", "2018-01-10", 100.0, 10.0),
        _row("o3", "cust_repeat", "2018-08-29", 100.0, 10.0),
        # cust_old: one old order
        _row("o4", "cust_old", "2017-01-01", 5.0, 1.0),
        # cust_new: one very recent order (defines the max date 2018-08-30)
        _row("o5", "cust_new", "2018-08-30", 7.0, 1.0),
    ]
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ frequency / recency / monetary
def test_frequency_counts_distinct_orders_not_item_rows(synthetic_items):
    out = rfm.compute_rfm(synthetic_items).set_index("customer_unique_id")
    assert out.loc["cust_multi_item", "Frequency"] == 1  # 3 item rows, 1 order
    assert out.loc["cust_repeat", "Frequency"] == 2


def test_monetary_sums_price_plus_freight_over_all_items(synthetic_items):
    out = rfm.compute_rfm(synthetic_items).set_index("customer_unique_id")
    assert out.loc["cust_multi_item", "Monetary"] == pytest.approx(66.0)  # 10+20+30 + 1+2+3
    assert out.loc["cust_repeat", "Monetary"] == pytest.approx(220.0)


def test_recency_uses_max_date_plus_one_day_by_default(synthetic_items):
    out = rfm.compute_rfm(synthetic_items).set_index("customer_unique_id")
    # reference date = 2018-08-31
    assert out.loc["cust_new", "Recency"] == 1
    assert out.loc["cust_multi_item", "Recency"] == 30
    assert out.loc["cust_repeat", "Recency"] == 2  # uses the LAST of its two orders


def test_explicit_reference_date(synthetic_items):
    out = rfm.compute_rfm(synthetic_items, reference_date=dt.date(2018, 9, 30)).set_index("customer_unique_id")
    assert out.loc["cust_new", "Recency"] == 31


def test_one_row_per_customer(synthetic_items):
    out = rfm.compute_rfm(synthetic_items)
    assert out["customer_unique_id"].is_unique
    assert len(out) == 4


# ------------------------------------------------------------------ scoring helpers
def test_frequency_score_caps_at_four():
    assert [rfm.score_frequency(n) for n in (1, 2, 3, 4, 9)] == [1, 2, 3, 4, 4]


def test_quartile_score_ties_get_same_score_and_range_is_1_to_4():
    s = pd.Series([1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    scores = rfm._quartile_score(s, higher_is_better=True)
    assert set(scores.unique()) <= {1, 2, 3, 4}
    assert scores[s == 1].nunique() == 1  # identical values never split across groups
    assert scores.iloc[-1] == 4


def test_quartile_score_direction():
    s = pd.Series(range(1, 101))
    high_good = rfm._quartile_score(s, higher_is_better=True)
    low_good = rfm._quartile_score(s, higher_is_better=False)
    assert high_good.iloc[0] == 1 and high_good.iloc[-1] == 4
    assert low_good.iloc[0] == 4 and low_good.iloc[-1] == 1


def test_quartile_score_matches_qcut_when_edges_unique():
    s = pd.Series(range(1, 101))
    expected = pd.qcut(s, q=4, labels=[1, 2, 3, 4]).astype(int)
    assert (rfm._quartile_score(s, higher_is_better=True) == expected).all()


# ------------------------------------------------------------------ segmentation rules
def test_one_time_buyer_can_never_be_champion_or_loyal():
    """Exhaustive: for every R (1-4), M (1-4) with exactly 1 order, check the segment."""
    for r, m in itertools.product(range(1, 5), range(1, 5)):
        total = r + 1 + m  # F score for 1 order is 1
        seg = rfm.assign_segment(r, 1, total)
        assert seg not in ("Champions", "Loyal Customers"), (r, m, seg)
        assert seg != "At Risk"  # At Risk is reserved for repeat customers


def test_one_time_buyer_segments_by_recency():
    assert rfm.assign_segment(4, 1, 9) == "New Customers"  # previously mis-labelled Loyal
    assert rfm.assign_segment(3, 1, 8) == "Potential Loyalists"
    assert rfm.assign_segment(2, 1, 5) == "Lost / One-Time"
    assert rfm.assign_segment(1, 1, 3) == "Lost / One-Time"


def test_repeat_buyer_segments():
    assert rfm.assign_segment(4, 4, 12) == "Champions"
    assert rfm.assign_segment(3, 3, 10) == "Champions"
    assert rfm.assign_segment(3, 2, 8) == "Loyal Customers"
    assert rfm.assign_segment(3, 2, 7) == "Potential Loyalists"
    assert rfm.assign_segment(2, 3, 9) == "At Risk"
    assert rfm.assign_segment(1, 2, 4) == "At Risk"


def test_every_segment_is_a_known_label():
    for r, f, m in itertools.product(range(1, 5), range(1, 6), range(1, 5)):
        total = r + rfm.score_frequency(f) + m
        assert rfm.assign_segment(r, f, total) in rfm.SEGMENT_ORDER


def test_end_to_end_multi_item_single_order_is_not_repeat(synthetic_items):
    out = rfm.build_rfm(synthetic_items).set_index("customer_unique_id")
    assert out.loc["cust_multi_item", "Frequency"] == 1
    assert out.loc["cust_multi_item", "Customer_Segment"] not in ("Champions", "Loyal Customers")
    assert out.loc["cust_repeat", "Frequency"] == 2


def test_output_columns_match_what_power_bi_expects(synthetic_items):
    out = rfm.build_rfm(synthetic_items)
    assert list(out.columns) == [
        "customer_unique_id", "Recency", "Frequency", "Monetary",
        "R_Score", "M_Score", "F_Score", "RFM_Concat", "RFM_Total_Score", "Customer_Segment",
    ]


# ------------------------------------------------------------------ data quality
def test_quality_report_clean_data_passes(synthetic_items):
    report = rfm.data_quality_report(synthetic_items)
    rfm.assert_data_quality(report)
    assert report["rows"] == 7 and report["distinct_orders"] == 5 and report["distinct_customers"] == 4


def test_quality_flags_invalid_dates(synthetic_items):
    bad = synthetic_items.copy()
    bad.loc[0, "purchase_date"] = "not-a-date"
    report = rfm.data_quality_report(bad)
    assert report["critical_invalid_or_missing_dates"] == 1
    with pytest.raises(ValueError):
        rfm.assert_data_quality(report)


def test_quality_flags_missing_keys_and_duplicates_and_negatives(synthetic_items):
    bad = pd.concat([synthetic_items, synthetic_items.iloc[[0]]], ignore_index=True)  # duplicate item key
    bad.loc[1, "customer_unique_id"] = None
    bad.loc[2, "product_price"] = -5.0
    report = rfm.data_quality_report(bad)
    assert report["critical_missing_keys"] == 1
    assert report["critical_duplicate_order_item_keys"] == 1
    assert report["critical_negative_values"] == 1


def test_quality_reports_missing_columns():
    with pytest.raises(KeyError):
        rfm.data_quality_report(pd.DataFrame({"order_id": ["a"]}))


def test_quality_flags_orders_spanning_customers(synthetic_items):
    bad = synthetic_items.copy()
    bad.loc[1, "customer_unique_id"] = "someone_else"  # same order_id o1, different customer
    assert rfm.data_quality_report(bad)["orders_with_multiple_customers"] == 1
