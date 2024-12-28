import json
import os
import pandas as pd
from dotenv import load_dotenv
from .utils import calculate_date_range, calculate_expenses, calculate_income, get_currency_rate, get_stock_prices

# Загрузка ключа API из файла .env
load_dotenv()
API_KEY = os.getenv("API_KEY")


def main(transactions_list: list, date_str: str, range_type: str = "M") -> str:
    """Главная функция для обработки данных о транзакциях и получения результатов."""
    transactions = pd.DataFrame(transactions_list)
    start_date, end_date = calculate_date_range(date_str, range_type)

    expenses = calculate_expenses(transactions, start_date, end_date)
    income = calculate_income(transactions, start_date, end_date)
    currency_rates = get_currency_rate()
    stock_prices = get_stock_prices(symbol="IBM", api_key=API_KEY)

    response = {"expenses": expenses, "income": income, "currency_rates": currency_rates, "stock_prices": stock_prices}

    return json.dumps(response, ensure_ascii=False, indent=4)


# Пример использования
if __name__ == "__main__":
    transactions_list = [
        {"date": "2023-10-01", "amount": -200, "category": "Еда"},
        {"date": "2023-10-05", "amount": -150, "category": "Транспорт"},
        {"date": "2023-10-10", "amount": 300, "category": "Зарплата"},
        {"date": "2023-10-15", "amount": -50, "category": "Развлечения"},
        {"date": "2023-10-20", "amount": -100, "category": "Еда"},
        {"date": "2023-10-25", "amount": 200, "category": "Бонус"},
        {"date": "2023-10-30", "amount": -75, "category": "Наличные"},
    ]

    date_input = "2023-10-15"
    result = main(transactions_list, date_input, "M")
    print(result)
