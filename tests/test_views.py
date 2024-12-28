import json
import pytest
from unittest.mock import patch
from src.views import main


@pytest.fixture
def transactions_list():
    return [
        {"date": "2023-10-01", "amount": -200, "category": "Еда"},
        {"date": "2023-10-05", "amount": -150, "category": "Транспорт"},
        {"date": "2023-10-10", "amount": 300, "category": "Зарплата"},
        {"date": "2023-10-15", "amount": -50, "category": "Развлечения"},
        {"date": "2023-10-20", "amount": -100, "category": "Еда"},
        {"date": "2023-10-25", "amount": 200, "category": "Бонус"},
        {"date": "2023-10-30", "amount": -75, "category": "Наличные"},
    ]


@pytest.mark.parametrize(
    "date_input, expected_expenses",
    [
        ("2023-10-15", {"total": 325, "main": {"Еда": 200, "Транспорт": 150}, "other": 75}),
        ("2023-10-20", {"total": 325, "main": {"Еда": 200, "Транспорт": 150}, "other": 75}),
        ("2023-10-01", {"total": 200, "main": {"Еда": 200}, "other": 0}),
    ],
)
@patch("src.views.calculate_expenses")
@patch("src.views.calculate_income")
@patch("src.views.get_currency_rate")
@patch("src.views.get_stock_prices")
def test_main(
    mock_get_stock_prices,
    mock_get_currency_rate,
    mock_calculate_income,
    mock_calculate_expenses,
    transactions_list,
    date_input,
    expected_expenses,
):

    mock_calculate_expenses.return_value = expected_expenses
    mock_calculate_income.return_value = {"total": 300}
    mock_get_currency_rate.return_value = {"USD": 1.0}
    mock_get_stock_prices.return_value = {"IBM": 150}

    result = main(transactions_list, date_input, "M")

    response = json.loads(result)

    assert response["expenses"] == expected_expenses
    assert response["income"]["total"] == 300
    assert response["currency_rates"]["USD"] == 1.0
    assert response["stock_prices"]["IBM"] == 150
