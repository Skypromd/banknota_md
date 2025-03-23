import json
import logging
import os
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_excel_data(file_path: str) -> pd.DataFrame:
    """
    Читает данные из Excel файла и возвращает их в виде DataFrame.

    Args:
        file_path (str): Путь к Excel файлу с транзакциями.

    Returns:
        pd.DataFrame: DataFrame с данными из Excel файла.

    Raises:
        Exception: Если файл не удалось прочитать или он поврежден.
    """
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        logger.info(f"Успешно прочитан файл {file_path}")
        return df
    except Exception as e:
        logger.error(f"Ошибка при чтении файла: {e}")
        raise


def load_user_settings(settings_path: str) -> Dict[str, List[str]]:
    """
    Загружает пользовательские настройки из JSON файла.

    Args:
        settings_path (str): Путь к файлу настроек.

    Returns:
        Dict[str, List[str]]: Словарь с валютами и акциями.
    """
    with open(settings_path, "r", encoding="utf-8") as f:
        data: Dict[str, List[str]] = json.load(f)  # Явно аннотируем тип
        return data


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv("API_KEY_CURRENCY")
    url = f"https://api.exchangerate-api.com/v4/latest/RUB?access_key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rates = [{"currency": curr, "rate": data["rates"].get(curr, 0)} for curr in currencies]
        logger.info("Успешно получены курсы валют")
        return rates
    except requests.RequestException as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return [{"currency": curr, "rate": 0} for curr in currencies]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv("API_KEY_STOCKS")
    prices = []
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            last_date = list(data["Time Series (Daily)"].keys())[0]
            price = float(data["Time Series (Daily)"][last_date]["4. close"])
            prices.append({"stock": stock, "price": price})
            logger.info(f"Успешно получена цена акции {stock}")
        except (requests.RequestException, KeyError) as e:
            logger.error(f"Ошибка получения цены акции {stock}: {e}")
            prices.append({"stock": stock, "price": 0})
    return prices
