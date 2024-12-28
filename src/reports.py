import pandas as pd
import json
from datetime import datetime, timedelta


def report_decorator(default_filename=None):
    def decorator(func):
        def wrapper(transactions_df, category, date=None, filename=None):

            if date is None:
                date = datetime.now()

            if filename is None:
                filename = default_filename or f"report_{category}_{date.strftime('%Y%m%d')}.json"

            report_data = func(transactions_df, category, date)

            report_data["total_expenses"] = int(report_data["total_expenses"])

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(report_data, f, ensure_ascii=False, indent=4)

            return report_data

        return wrapper

    return decorator


@report_decorator()
def expenses_by_category(transactions_df, category, date=None):

    if date is None:
        date = datetime.now()

    three_months_ago = date - timedelta(days=90)

    filtered_df = transactions_df[
        (transactions_df["category"] == category)
        & (transactions_df["date"] >= three_months_ago)
        & (transactions_df["date"] <= date)
    ]

    total_expenses = filtered_df["amount"].sum()

    result = {"category": category, "total_expenses": total_expenses, "date": date.strftime("%Y-%m-%d")}

    return result


# Пример использования
if __name__ == "__main__":

    data = {
        "date": pd.date_range(start="2023-01-01", periods=100, freq="D"),
        "amount": [100, 200, 150, 300, 250] * 20,
        "category": ["food", "transport", "entertainment", "food", "transport"] * 20,
    }
    transactions_df = pd.DataFrame(data)

    report = expenses_by_category(transactions_df, "food")
    print(report)
