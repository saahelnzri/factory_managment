import pandas as pd
from .config import EXCEL_PATH

EXPECTED_SHEETS = {
    "departments": ["department_id", "department_name", "city"],
    "employees": ["employee_id", "first_name", "last_name", "city", "department_id", "salary"],
    "products": ["product_id", "product_name", "category", "unit_price", "stock_quantity"],
    "customers": ["customer_id", "first_name", "last_name", "city"],
    "orders": ["order_id", "customer_id", "order_date", "status"],
    "order_items": ["order_item_id", "order_id", "product_id", "quantity", "unit_price"]
}

def extract_workbook(path=EXCEL_PATH):
    workbook = pd.read_excel(path, sheet_name=None)
    missing_sheets = set(EXPECTED_SHEETS) - set(workbook)
    if missing_sheets:
        raise ValueError(f"Missing sheets: {sorted(missing_sheets)}")
    result = {}
    for name, columns in EXPECTED_SHEETS.items():
        frame = workbook[name].copy()
        missing_columns = set(columns) - set(frame.columns)
        if missing_columns:
            raise ValueError(f"{name} is missing columns: {sorted(missing_columns)}")
        result[name] = frame[columns]
    return result
