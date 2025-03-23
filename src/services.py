import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def get_beneficial_cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """
    Анализирует выгодность категорий повышенного кешбэка за указанный месяц.

    Args:
        data (List[Dict[str, Any]]): Список транзакций.
        year (int): Год для анализа.
        month (int): Месяц для анализа.

    Returns:
        Dict[str, float]: Словарь с категориями и потенциальным кешбэком (1% от суммы).
    """
    cashback_dict: Dict[str, float] = {}
    period = f"{year}-{month:02d}"

    for transaction in data:
        trans_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if trans_date.strftime("%Y-%m") == period and transaction["Сумма операции"] < 0:
            category = transaction["Категория"]
            amount = abs(transaction["Сумма операции"])
            cashback_dict[category] = cashback_dict.get(category, 0) + (amount * 0.01)

    logger.info(f"Рассчитаны выгодные категории кешбэка за {period}")
    return {k: round(v, 2) for k, v in cashback_dict.items()}
