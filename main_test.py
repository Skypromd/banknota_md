import json
import os
import sys
from typing import Any, Dict, List

from src.reports import spending_by_category
from src.services import get_beneficial_cashback_categories
from src.utils import read_excel_data
from src.views import home_page


sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def main() -> None:
    """
    Основная точка входа в приложение, демонстрирует работу всех функций.
    """
    df = read_excel_data("data/operations.xlsx")
    transactions: List[Dict[str, Any]] = [{str(k): v for k, v in record.items()} for record in df.to_dict("records")]

    home_result = home_page("2021-12-31 16:44:00")
    print("Home Page:")
    print(json.dumps(home_result, ensure_ascii=False, indent=2))

    cashback_result = get_beneficial_cashback_categories(transactions, 2021, 12)
    print("\nBeneficial Cashback Categories:")
    print(json.dumps(cashback_result, ensure_ascii=False, indent=2))

    spending_result = spending_by_category(df, "Супермаркеты", "2022-01-01")
    print("\nSpending by Category:")
    print(json.dumps(spending_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()