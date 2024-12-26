import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, mock_open
from src.reports import expenses_by_category

# Подготовка тестовых данных
data = {
    "date": [
        datetime(2023, 1, 10),
        datetime(2023, 2, 15),
        datetime(2023, 3, 20),
        datetime(2023, 4, 25),
        datetime(2023, 5, 30),
        datetime(2023, 6, 15),
        datetime(2023, 8, 25),
    ],
    "amount": [100, 200, 150, 300, 250, 200, 300],
    "category": ["Еда", "Еда", "Транспорт", "Еда", "Транспорт", "Еда", "Еда"],
}
transactions_df = pd.DataFrame(data)


@pytest.mark.parametrize("category, expected_total", [("Еда", 300), ("Транспорт", 0), ("Развлечения", 0)])
@patch("builtins.open", new_callable=mock_open)
def test_expenses_by_category(mock_file, category, expected_total):
    """Тест для проверки функции expenses_by_category."""

    fixed_date = datetime(2023, 9, 30)
    result = expenses_by_category(transactions_df, category, fixed_date)

    mock_file.assert_called_once()

    assert f"Total expenses for category '{category}'" in result
    assert str(expected_total) in result


# Запуск тестов
if __name__ == "__main__":
    pytest.main()
