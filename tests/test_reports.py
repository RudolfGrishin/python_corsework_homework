import pytest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
import pandas as pd
from src.reports import expenses_by_category


data = {
    "date": pd.date_range(start="2023-01-01", periods=100, freq="D"),
    "amount": [100, 200, 150, 300, 250] * 20,  # Примерные значения
    "category": ["food", "transport", "entertainment", "food", "transport"] * 20,
}

transactions_df = pd.DataFrame(data)


def calculate_expected_totals(transactions_df, date):
    three_months_ago = date - timedelta(days=90)
    filtered_df = transactions_df[(transactions_df["date"] >= three_months_ago) & (transactions_df["date"] <= date)]
    return {
        "food": filtered_df[filtered_df["category"] == "food"]["amount"].sum(),
        "transport": filtered_df[filtered_df["category"] == "transport"]["amount"].sum(),
        "entertainment": filtered_df[filtered_df["category"] == "entertainment"]["amount"].sum(),
    }


date_for_tests = datetime(2023, 4, 1)
expected_totals = calculate_expected_totals(transactions_df, date_for_tests)


@pytest.mark.parametrize(
    "category, expected_total",
    [
        ("food", expected_totals["food"]),
        ("transport", expected_totals["transport"]),
        ("entertainment", expected_totals["entertainment"]),
    ],
)
@patch("builtins.open", new_callable=mock_open)
def test_expenses_by_category(mock_file, category, expected_total):

    date = date_for_tests

    report = expenses_by_category(transactions_df, category, date)

    assert report["category"] == category
    assert report["total_expenses"] == expected_total


if __name__ == "__main__":
    pytest.main()
