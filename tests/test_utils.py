import logging
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import read_excel_data


@pytest.fixture
def mock_excel_data() -> pd.DataFrame:
    """Фикстура для создания тестового DataFrame."""
    return pd.DataFrame({"Дата операции": ["2025-03-01"], "Сумма операции": [100.0]})


@patch("pandas.read_excel")
def test_read_excel_data_success(
    mock_read: Any, mock_excel_data: pd.DataFrame, caplog: Any
) -> None:
    """Тестирует успешное чтение Excel файла."""
    mock_read.return_value = mock_excel_data
    caplog.set_level(logging.INFO)
    result = read_excel_data("fake_path.xlsx")
    assert isinstance(result, pd.DataFrame)
    assert result.equals(mock_excel_data)
    assert "Успешно прочитан файл fake_path.xlsx" in caplog.text


@patch("pandas.read_excel")
def test_read_excel_data_failure(mock_read: Any, caplog: Any) -> None:
    """Тестирует обработку ошибки при чтении Excel файла."""
    mock_read.side_effect = Exception("File error")
    caplog.set_level(logging.ERROR)
    with pytest.raises(Exception, match="File error"):
        read_excel_data("fake_path.xlsx")
    assert "Ошибка при чтении файла: File error" in caplog.text
