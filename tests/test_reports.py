import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    """Фикстура для тестовых транзакций."""
    data = {
        "Дата операции": ["01.10.2021 10:00:00", "01.11.2021 12:00:00", "01.12.2021 14:00:00"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Транспорт"],
        "Сумма платежа": [-100.0, -150.0, -200.0],
        "Сумма операции": [-100.0, -150.0, -200.0],
    }
    return pd.DataFrame(data)


@pytest.mark.parametrize(
    "category, expected_spent",
    [("Супермаркеты", 250.0), ("Транспорт", 200.0)],
)
def test_spending_by_category(
    sample_transactions: pd.DataFrame, category: str, expected_spent: float
) -> None:
    """Тестирует функцию spending_by_category с параметрами."""
    result = spending_by_category(sample_transactions, category, "2022-01-01")
    assert isinstance(result, dict)
    assert result["category"] == category
    assert result["total_spent"] == expected_spent
    assert "period" in result
