import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import json
from src.views import (
    calculate_date_range,
    calculate_expenses,
    calculate_income,
    get_currency_rate,
    get_stock_prices,
    main,
)


class TestFinancialFunctions(unittest.TestCase):

    def setUp(self):
        # Фикстуры для тестовых данных
        self.transactions = [
            {"date": "2023-10-01", "amount": -200, "category": "Еда"},
            {"date": "2023-10-05", "amount": -150, "category": "Транспорт"},
            {"date": "2023-10-10", "amount": 300, "category": "Зарплата"},
            {"date": "2023-10-15", "amount": -50, "category": "Развлечения"},
            {"date": "2023-10-20", "amount": -100, "category": "Еда"},
            {"date": "2023-10-25", "amount": 200, "category": "Бонус"},
            {"date": "2023-10-30", "amount": -75, "category": "Наличные"},
        ]

    @patch("src.views.monthrange")
    def test_calculate_date_range_week(self, mock_monthrange):
        date_str = "2023-10-15"
        range_type = "W"
        start_date, end_date = calculate_date_range(date_str, range_type)
        self.assertEqual(start_date, datetime(2023, 10, 9))
        self.assertEqual(end_date, datetime(2023, 10, 15))

    @patch("src.views.monthrange")
    def test_calculate_date_range_month(self, mock_monthrange):
        mock_monthrange.return_value = (1, 31)
        date_str = "2023-10-15"
        range_type = "M"
        start_date, end_date = calculate_date_range(date_str, range_type)
        self.assertEqual(start_date, datetime(2023, 10, 1))
        self.assertEqual(end_date, datetime(2023, 10, 31))

    def test_calculate_expenses(self):
        start_date = datetime(2023, 10, 1)
        end_date = datetime(2023, 10, 31)
        result = calculate_expenses(self.transactions, start_date, end_date)
        self.assertEqual(result["total"], 575)
        self.assertIn("Еда", result["main"])
        self.assertEqual(result["main"]["Еда"], 300)

    def test_calculate_income(self):
        start_date = datetime(2023, 10, 1)
        end_date = datetime(2023, 10, 31)
        result = calculate_income(self.transactions, start_date, end_date)
        self.assertEqual(result["total"], 500)
        self.assertIn("Зарплата", result["main"])
        self.assertEqual(result["main"]["Зарплата"], 300)

    @patch("src.views.requests.get")
    def test_get_currency_rate(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"EUR": 0.85, "GBP": 0.75}}
        mock_get.return_value = mock_response

        rates = get_currency_rate("USD")
        self.assertEqual(rates["EUR"], 0.85)
        self.assertEqual(rates["GBP"], 0.75)

    @patch("src.views.requests.get")
    def test_get_stock_prices(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Time Series (5min)": {"2023-10-01 10:00:00": {"1. open": "100", "2. high": "110"}}
        }
        mock_get.return_value = mock_response

        prices = get_stock_prices("IBM")
        self.assertIn("2023-10-01 10:00:00", prices)

    @patch("src.views.calculate_date_range")
    @patch("src.views.calculate_expenses")
    @patch("src.views.calculate_income")
    @patch("src.views.get_currency_rate")
    @patch("src.views.get_stock_prices")
    def test_main(
        self,
        mock_get_stock_prices,
        mock_get_currency_rate,
        mock_calculate_income,
        mock_calculate_expenses,
        mock_calculate_date_range,
    ):
        mock_calculate_date_range.return_value = (datetime(2023, 10, 1), datetime(2023, 10, 31))
        mock_calculate_expenses.return_value = {"total": 575, "main": {"Еда": 300}, "other": 225}
        mock_calculate_income.return_value = {"total": 500, "main": {"Зарплата": 300}}
        mock_get_currency_rate.return_value = {"EUR": 0.85, "GBP": 0.75}
        mock_get_stock_prices.return_value = {"2023-10-01 10:00:00": {"1. open": "100"}}

        result = main("2023-10-15", "M", self.transactions)
        self.assertIn("expenses", json.loads(result))
        self.assertIn("income", json.loads(result))
        self.assertIn("currency_rates", json.loads(result))
        self.assertIn("stock_prices", json.loads(result))


if __name__ == "__main__":
    unittest.main()
