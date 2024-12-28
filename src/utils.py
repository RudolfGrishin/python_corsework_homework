import logging
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from calendar import monthrange
from typing import Dict, Any, Tuple
import requests

logging.basicConfig(level=logging.INFO)


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

    logging.info(f"Start date: {start_date}, End date: {end_date}")

    return start_date, end_date


def calculate_expenses(transactions: pd.DataFrame, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Рассчитывает общую сумму расходов и классифицирует их по категориям."""
    expenses = defaultdict(float)
    total_expenses = 0

    # Фильтруем транзакции по дате и сумме
    filtered_expenses = transactions[
        (transactions["amount"] < 0)
        & (pd.to_datetime(transactions["date"]) >= start_date)
        & (pd.to_datetime(transactions["date"]) <= end_date)
    ]

    for _, transaction in filtered_expenses.iterrows():
        expenses[transaction["category"]] += abs(transaction["amount"])
        total_expenses += abs(transaction["amount"])

    # Сортируем и выбираем основные расходы
    sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    main_expenses = sorted_expenses[:2]
    other_expenses = sum(amount for _, amount in sorted_expenses[2:])

    logging.info(f"Calculated expenses: {expenses}")

    return {
        "total": round(total_expenses),
        "main": {category: round(amount) for category, amount in main_expenses},
        "other": round(other_expenses),
    }


def calculate_income(transactions: pd.DataFrame, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Рассчитывает общую сумму поступлений и классифицирует их по категориям."""
    income = defaultdict(float)
    total_income = 0

    # Фильтруем транзакции по дате и сумме
    filtered_income = transactions[
        (transactions["amount"] > 0)
        & (pd.to_datetime(transactions["date"]) >= start_date)
        & (pd.to_datetime(transactions["date"]) <= end_date)
    ]

    for _, transaction in filtered_income.iterrows():
        income[transaction["category"]] += transaction["amount"]
        total_income += transaction["amount"]

    sorted_income = sorted(income.items(), key=lambda x: x[1], reverse=True)

    logging.info(f"Calculated income: {income}")

    return {"total": round(total_income), "main": {category: round(amount) for category, amount in sorted_income}}


def get_currency_rate(base_currency: str = "USD") -> Dict[str, float]:
    """Получает курсы валют по отношению к заданной базовой валюте."""
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    logging.info(f"Currency rates fetched: {data.get('rates', {})}")

    return data.get("rates", {})


def get_stock_prices(symbol: str = "IBM", api_key: str = "") -> Dict[str, Any]:
    """Получает цены акций из Alpha Vantage по заданному символу."""
    url = (
        f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
        f"{symbol}&interval=5min&apikey={api_key}"
    )
    response = requests.get(url)
    data = response.json()

    logging.info(f"Stock prices fetched for {symbol}: {data.get('Time Series (5min)', {})}")

    return data.get("Time Series (5min)", {})
