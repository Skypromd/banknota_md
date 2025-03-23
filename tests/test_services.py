from typing import Dict, List

import pytest

from src.services import get_beneficial_cashback_categories


@pytest.fixture
def sample_transactions() -> List[Dict[str, float | str]]:
    """
    Фикстура для тестовых транзакций.

    Returns:
        List[Dict[str, float | str]]: Список тестовых транзакций.
    """
    return [
        {"Дата операции": "01.12.2021 10:00:00", "Сумма операции": -100.0, "Категория": "Еда"},
        {"Дата операции": "02.12.2021 12:00:00", "Сумма операции": -200.0, "Категория": "Транспорт"},
    ]


def test_get_beneficial_cashback_categories(sample_transactions: List[Dict[str, float | str]]) -> None:
    """
    Тестирует функцию get_beneficial_cashback_categories.

    Args:
        sample_transactions (List[Dict[str, float | str]]): Тестовые данные транзакций из фикстуры.
    """
    result = get_beneficial_cashback_categories(sample_transactions, 2021, 12)
    assert isinstance(result, dict)
    assert result["Еда"] == 1.0
    assert result["Транспорт"] == 2.0
