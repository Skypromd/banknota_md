import logging
import math
from datetime import datetime
from typing import Any, Dict

from src.utils import get_currency_rates, get_stock_prices, load_user_settings, read_excel_data

logger = logging.getLogger(__name__)


def home_page(date_str: str) -> Dict[str, Any]:
    """
    Генерирует JSON-ответ для главной страницы.

    Args:
        date_str (str): Дата и время в формате 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        Dict[str, Any]: JSON-ответ с данными для главной страницы.
    """
    logger.info(f"Processing home_page for {date_str}")
    df = read_excel_data("data/operations.xlsx")
    settings = load_user_settings("user_settings.json")

    hour = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").hour
    if 6 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 16:
        greeting = "Добрый день"
    elif 16 <= hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    df_expenses = df[df["Сумма операции"] < 0]
    cards_data = (
        df_expenses.groupby("Номер карты")
        .agg({"Сумма платежа": lambda x: abs(x.sum())})
        .reset_index()
        .rename(columns={"Номер карты": "last_digits", "Сумма платежа": "total_spent"})
    )
    cards_data["cashback"] = cards_data["total_spent"].apply(lambda x: round(math.ceil(x / 100 * 100) / 100, 2))
    cards_list = cards_data.to_dict("records")

    top_transactions = (
        df.nlargest(5, "Сумма платежа")[["Дата операции", "Сумма платежа", "Категория", "Описание"]]
        .rename(columns={"Дата операции": "date", "Сумма платежа": "amount"})
        .to_dict("records")
    )

    currencies = get_currency_rates(settings["user_currencies"])
    stocks = get_stock_prices(settings["user_stocks"])

    logger.info("Home page data processed successfully")
    return {
        "greeting": greeting,
        "cards": cards_list,
        "top_transactions": top_transactions,
        "currency_rates": currencies,
        "stock_prices": stocks,
    }
