import logging
import math
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from src.utils import get_currency_rates, get_stock_prices, load_user_settings, read_excel_data

logger = logging.getLogger(__name__)


def get_greeting(date_str: str) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 16:
        return "Добрый день"
    elif 16 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_cards_data(
    df: pd.DataFrame, start_date: datetime, end_date: datetime
) -> List[Dict[str, Any]]:
    """Возвращает данные о картах с расходами и кешбэком за указанный период."""
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    df_expenses = df[
        (df["Сумма операции"] < 0)
        & (df["Дата операции"] >= start_date)
        & (df["Дата операции"] <= end_date)
    ]
    cards_data = (
        df_expenses.groupby("Номер карты")
        .agg({"Сумма платежа": lambda x: abs(x.sum())})
        .reset_index()
        .rename(columns={"Номер карты": "last_digits", "Сумма платежа": "total_spent"})
    )
    cards_data["cashback"] = cards_data["total_spent"].apply(
        lambda x: round(math.ceil(x / 100 * 100) / 100, 2)
    )
    return cards_data.to_dict("records")


def get_top_transactions(
    df: pd.DataFrame, start_date: datetime, end_date: datetime
) -> List[Dict[str, Any]]:
    """Возвращает топ-5 транзакций за указанный период."""
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    top_transactions = filtered_df.nlargest(5, "Сумма платежа")[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ].rename(columns={"Дата операции": "date", "Сумма платежа": "amount"})
    # Преобразуем Timestamp в строку
    top_transactions["date"] = top_transactions["date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return top_transactions.to_dict("records")


def home_page(date_str: str) -> Dict[str, Any]:
    """Генерирует JSON-ответ для главной страницы."""
    logger.info(f"Processing home_page for {date_str}")
    df = read_excel_data("data/operations.xlsx")
    settings = load_user_settings("user_settings.json")

    end_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_date = end_date.replace(day=1, hour=0, minute=0, second=0)

    greeting = get_greeting(date_str)
    cards = get_cards_data(df, start_date, end_date)
    top_transactions = get_top_transactions(df, start_date, end_date)
    currencies = get_currency_rates(settings["user_currencies"])
    stocks = get_stock_prices(settings["user_stocks"])

    logger.info("Home page data processed successfully")
    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currencies,
        "stock_prices": stocks,
    }
