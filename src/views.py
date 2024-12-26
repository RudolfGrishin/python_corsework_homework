import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Tuple
from calendar import monthrange

# Загрузка ключа API из файла .env
load_dotenv()
API_KEY = os.getenv("API_KEY")


def calculate_date_range(date_str: str, range_type: str = "M") -> Tuple[datetime, datetime]:
    """Определяет начальную и конечную даты на основе заданного диапазона."""
    date = datetime.strptime(date_str, "%Y-%m-%d")

    if range_type == "W":
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=6)
    elif range_type == "M":
        start_date = date.replace(day=1)
        end_date = date.replace(day=monthrange(date.year, date.month)[1])
    elif range_type == "Y":
        start_date = date.replace(month=1, day=1)
        end_date = date.replace(month=12, day=31)
    elif range_type == "ALL":
        start_date = datetime.min
        end_date = date
    else:
        raise ValueError("Неверный тип диапазона. Используйте W, M, Y или ALL.")

    # Отладочные сообщения
    print(f"Start date: {start_date}, End date: {end_date}")

    return start_date, end_date


def calculate_expenses(transactions: List[Dict[str, Any]], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Рассчитывает общую сумму расходов и классифицирует их по категориям."""
    expenses = defaultdict(float)
    total_expenses = 0

    for transaction in transactions:
        if transaction["amount"] < 0:
            date = datetime.strptime(transaction["date"], "%Y-%m-%d")
            if start_date <= date <= end_date:
                expenses[transaction["category"]] += abs(transaction["amount"])
                total_expenses += abs(transaction["amount"])

    sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    main_expenses = sorted_expenses[:7]
    other_expenses = sum(amount for _, amount in sorted_expenses[7:])

    return {
        "total": round(total_expenses),
        "main": {category: round(amount) for category, amount in main_expenses},
        "other": round(other_expenses),
    }


def calculate_income(transactions: List[Dict[str, Any]], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Рассчитывает общую сумму поступлений и классифицирует их по категориям."""
    income = defaultdict(float)
    total_income = 0

    for transaction in transactions:
        if transaction["amount"] > 0:
            date = datetime.strptime(transaction["date"], "%Y-%m-%d")
            if start_date <= date <= end_date:
                income[transaction["category"]] += transaction["amount"]
                total_income += transaction["amount"]

    sorted_income = sorted(income.items(), key=lambda x: x[1], reverse=True)

    return {"total": round(total_income), "main": {category: round(amount) for category, amount in sorted_income}}


def get_currency_rate(base_currency: str = "USD") -> Dict[str, float]:
    """Получает курсы валют по отношению к заданной базовой валюте."""
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    return data.get("rates", {})


def get_stock_prices(symbol: str = "IBM") -> Dict[str, Any]:
    """Получает цены акций из Alpha Vantage по заданному символу."""
    url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
           f"{symbol}&interval=5min&apikey={API_KEY}")
    response = requests.get(url)
    data = response.json()

    return data.get("Time Series (5min)", {})


def main(date_str: str, range_type: str = "M", transactions: List[Dict[str, Any]] = []) -> str:
    """Главная функция для обработки данных о транзакциях и получения результатов."""
    start_date, end_date = calculate_date_range(date_str, range_type)

    expenses = calculate_expenses(transactions, start_date, end_date)
    income = calculate_income(transactions, start_date, end_date)
    currency_rates = get_currency_rate()
    stock_prices = get_stock_prices()

    response = {"expenses": expenses, "income": income, "currency_rates": currency_rates, "stock_prices": stock_prices}

    return json.dumps(response, ensure_ascii=False, indent=4)


# Пример использования
if __name__ == "__main__":
    transactions = [
        {"date": "2023-10-01", "amount": -200, "category": "Еда"},
        {"date": "2023-10-05", "amount": -150, "category": "Транспорт"},
        {"date": "2023-10-10", "amount": 300, "category": "Зарплата"},
        {"date": "2023-10-15", "amount": -50, "category": "Развлечения"},
        {"date": "2023-10-20", "amount": -100, "category": "Еда"},
        {"date": "2023-10-25", "amount": 200, "category": "Бонус"},
        {"date": "2023-10-30", "amount": -75, "category": "Наличные"},
    ]

    date_input = "2023-10-15"
    result = main(date_input, "M", transactions)
    print(result)
