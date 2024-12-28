import unittest
from unittest.mock import patch
import pandas as pd
from datetime import datetime
from src.utils import calculate_date_range, calculate_expenses, calculate_income, get_currency_rate, get_stock_prices


class TestUtils(unittest.TestCase):

    def setUp(self):

        self.transactions = pd.DataFrame(
            [
                {"date": "2023-10-01", "amount": -200, "category": "Еда"},
                {"date": "2023-10-05", "amount": -150, "category": "Транспорт"},
                {"date": "2023-10-10", "amount": 300, "category": "Зарплата"},
                {"date": "2023-10-15", "amount": -50, "category": "Развлечения"},
            ]
        )

    def test_calculate_date_range(self):

        test_cases = [
            ("2023-10-15", "M", (datetime(2023, 10, 1), datetime(2023, 10, 31))),
            ("2023-10-15", "W", (datetime(2023, 10, 9), datetime(2023, 10, 15))),
            ("2023-10-15", "Y", (datetime(2023, 1, 1), datetime(2023, 12, 31))),
            ("2023-10-15", "ALL", (datetime.min, datetime(2023, 10, 15))),
        ]

        for date_str, range_type, expected in test_cases:
            with self.subTest(date_str=date_str, range_type=range_type):
                result = calculate_date_range(date_str, range_type)
                self.assertEqual(result, expected)

    @patch("src.utils.logging.info")
    def test_calculate_expenses(self, mock_logging):
        result = calculate_expenses(self.transactions, datetime(2023, 10, 1), datetime(2023, 10, 31))
        expected = {"total": 400, "main": {"Еда": 200, "Транспорт": 150}, "other": 50}
        self.assertEqual(result, expected)

    @patch("src.utils.logging.info")
    def test_calculate_income(self, mock_logging):
        result = calculate_income(self.transactions, datetime(2023, 10, 1), datetime(2023, 10, 31))
        expected = {"total": 300, "main": {"Зарплата": 300}}
        self.assertEqual(result, expected)

    @patch("requests.get")
    def test_get_currency_rate(self, mock_get):
        mock_get.return_value.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.85}}
        result = get_currency_rate("USD")
        expected = {"USD": 1.0, "EUR": 0.85}
        self.assertEqual(result, expected)

    @patch("requests.get")
    def test_get_stock_prices(self, mock_get):
        mock_get.return_value.json.return_value = {"Time Series (5min)": {"2023-10-01 12:00:00": {"1. open": "145"}}}
        result = get_stock_prices("IBM", api_key="dummy_api_key")
        expected = {"2023-10-01 12:00:00": {"1. open": "145"}}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
