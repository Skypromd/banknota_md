from typing import Any
from unittest.mock import patch

import pandas as pd  # Подозреваемый импорт
import pytest

from src.views import home_page


@pytest.fixture
def mock_data() -> dict[str, list[Any]]:
    """
    Фикстура для тестовых данных.

    Returns:
        dict[str, list[Any]]: Словарь с тестовыми данными для DataFrame.
    """
    return {
        "Дата операции": ["31.12.2021 16:44:00"],
        "Номер карты": ["1234"],
        "Сумма платежа": [-100.50],
        "Сумма операции": [-100.50],
        "Категория": ["Супермаркеты"],
        "Описание": ["Покупка"],
    }


@patch("src.views.read_excel_data")
@patch("src.views.load_user_settings")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_home_page(
    mock_stocks: Any, mock_rates: Any, mock_settings: Any, mock_read: Any, mock_data: dict[str, list[Any]]
) -> None:
    """
    Тестирует функцию home_page.

    Args:
        mock_stocks: Мок для get_stock_prices.
        mock_rates: Мок для get_currency_rates.
        mock_settings: Мок для load_user_settings.
        mock_read: Мок для read_excel_data.
        mock_data: Тестовые данные из фикстуры.
    """
    mock_read.return_value = pd.DataFrame(mock_data)
    mock_settings.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mock_rates.return_value = [{"currency": "USD", "rate": 75.0}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}]

    result = home_page("2021-12-31 16:44:00")
    assert isinstance(result, dict)
    assert result["greeting"] == "Добрый вечер"
    assert len(result["cards"]) == 1
    assert result["cards"][0]["total_spent"] == 100.50
    assert result["cards"][0]["cashback"] == 1.01
    assert len(result["top_transactions"]) == 1
