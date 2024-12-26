import pandas as pd
from datetime import datetime
import functools
from typing import Optional, Callable


def report_to_file(filename: Optional[str] = None) -> Callable:
    """Декоратор для записи результата функции в файл."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> str:
            nonlocal filename
            result = func(*args, **kwargs)

            if filename is None:
                filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)
            return result

        return wrapper

    return decorator


@report_to_file()
def expenses_by_category(transactions_df: pd.DataFrame, category: str, date: Optional[datetime] = None) -> str:
    """Вычисляет общие расходы по указанной категории за последние три месяца."""

    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date)

    three_months_ago = date - pd.DateOffset(months=3)

    filtered_df = transactions_df[
        (transactions_df["category"] == category)
        & (transactions_df["date"] >= three_months_ago)
        & (transactions_df["date"] <= date)
    ]

    total_expenses = filtered_df["amount"].sum()

    return (
        f"Total expenses for category '{category}' from {three_months_ago.date()} to {date.date()}: {total_expenses}"
    )


# Пример использования
if __name__ == "__main__":

    data = {
        "date": [
            datetime(2023, 1, 10),
            datetime(2023, 2, 15),
            datetime(2023, 3, 20),
            datetime(2023, 4, 25),
            datetime(2023, 5, 30),
        ],
        "amount": [100, 200, 150, 300, 250],
        "category": ["Еда", "Еда", "Транспорт", "Еда", "Транспорт"],
    }
    transactions_df = pd.DataFrame(data)

    # Вызов функции
    expenses_by_category(transactions_df, "Еда")
