import pytest
from unittest.mock import patch
from src.services import analyze_cashback


# Фикстуры для генерации тестовых данных
@pytest.fixture
def transaction_data():
    return [
        {"date": "2023-10-01", "amount": 1000, "category": "Еда"},
        {"date": "2023-10-05", "amount": 2000, "category": "Транспорт"},
        {"date": "2023-10-10", "amount": 1500, "category": "Еда"},
        {"date": "2023-09-15", "amount": 500, "category": "Развлечения"},
        {"date": "2023-10-20", "amount": 500, "category": "Еда"},
    ]


# Параметризованные тесты
@pytest.mark.parametrize(
    "year, month, expected",
    [
        (2023, 10, '{"Еда": 3000, "Транспорт": 2000}'),
        (2023, 9, '{"Развлечения": 500}'),
    ],
)
def test_analyze_cashback(transaction_data, year, month, expected):
    result = analyze_cashback(transaction_data, year, month)
    assert result == expected


# Тест с использованием mock и patch
@patch("src.services.json.dumps")
def test_analyze_cashback_with_mock(mock_dumps, transaction_data):
    mock_dumps.return_value = '{"Еда": 3000, "Транспорт": 2000}'

    result = analyze_cashback(transaction_data, 2023, 10)

    mock_dumps.assert_called_once()
    assert result == '{"Еда": 3000, "Транспорт": 2000}'
