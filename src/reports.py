import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


def save_report_to_file(
    filename: str = "report.json",
) -> Callable[[Callable[..., Dict[str, Any]]], Callable[..., Dict[str, Any]]]:
    """Декоратор для сохранения результата отчета в JSON файл."""

    def decorator(func: Callable[..., Dict[str, Any]]) -> Callable[..., Dict[str, Any]]:
        def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
            result = func(*args, **kwargs)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info(f"Отчет сохранен в файл {filename}")
            return result

        return wrapper

    return decorator


@save_report_to_file(filename="report_spending_by_category.json")
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> Dict[str, Any]:
    """Формирует отчет о тратах по заданной категории за последние 3 месяца."""
    report_date = datetime.now() if not date else datetime.strptime(date, "%Y-%m-%d")
    three_months_ago = report_date - relativedelta(months=3)

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )
    filtered = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= report_date)
        & (transactions["Сумма операции"] < 0)
    ]

    total_spent = abs(filtered["Сумма платежа"].sum())
    logger.info(
        f"Рассчитаны траты по категории {category} за период {three_months_ago} - {report_date}"
    )

    return {
        "category": category,
        "total_spent": round(total_spent, 2),
        "period": f"{three_months_ago.strftime('%Y-%m-%d')} - {report_date.strftime('%Y-%m-%d')}",
    }
