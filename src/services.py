import json
import logging
from datetime import datetime
from typing import List, Dict, Any

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def analyze_cashback(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """Анализирует кешбэк по категориям за указанный месяц и год."""

    cashback_analysis: Dict[str, int] = {}

    for transaction in data:
        try:
            transaction_date = datetime.strptime(transaction["date"], "%Y-%m-%d")
        except ValueError as e:
            logging.error(f"Ошибка парсинга даты: {transaction['date']} - {e}")
            continue

        if transaction_date.year == year and transaction_date.month == month:
            category = transaction["category"]
            amount = transaction["amount"]

            if category in cashback_analysis:
                cashback_analysis[category] += amount
            else:
                cashback_analysis[category] = amount

    logging.info(f"Кешбэк анализ завершен для {year}-{month}: {cashback_analysis}")
    return json.dumps(cashback_analysis, ensure_ascii=False)


# Пример использования функции
data = [
    {"date": "2023-10-01", "amount": 1000, "category": "Еда"},
    {"date": "2023-10-05", "amount": 2000, "category": "Транспорт"},
    {"date": "2023-10-10", "amount": 1500, "category": "Еда"},
    {"date": "2023-09-15", "amount": 500, "category": "Развлечения"},
    {"date": "2023-10-20", "amount": 500, "category": "Еда"},
]

result = analyze_cashback(data, 2023, 10)
print(result)
