import pandas as pd
from .extract import EXPECTED_SHEETS

KEYS = {
    "departments": "department_id",
    "employees": "employee_id",
    "products": "product_id",
    "customers": "customer_id",
    "orders": "order_id",
    "order_items": "order_item_id"
}

def transform_tables(tables):
    cleaned = {}
    for name, expected in EXPECTED_SHEETS.items():
        frame = tables[name].copy()
        frame = frame[expected]
        for column in frame.select_dtypes(include="object").columns:
            frame[column] = frame[column].map(lambda value: value.strip() if isinstance(value, str) else value)
        frame = frame.drop_duplicates()
        frame = frame.dropna(subset=[KEYS[name]])
        if name in {"departments", "employees", "products", "customers", "orders", "order_items"}:
            frame = frame.dropna()
        if name in {"orders"}:
            frame["order_date"] = pd.to_datetime(frame["order_date"], errors="coerce")
            frame = frame.dropna(subset=["order_date"])
        for column in frame.columns:
            if column.endswith("_id") or column in {"salary", "unit_price", "stock_quantity", "quantity"}:
                frame[column] = pd.to_numeric(frame[column], errors="coerce")
        frame = frame.dropna()
        if name in KEYS:
            frame = frame.drop_duplicates(subset=[KEYS[name]], keep="last")
        cleaned[name] = frame.reset_index(drop=True)
    _validate_relationships(cleaned)
    cleaned["order_items"]["line_total"] = cleaned["order_items"]["quantity"] * cleaned["order_items"]["unit_price"]
    return cleaned

def _validate_relationships(tables):
    checks = [
        ("employees", "department_id", "departments", "department_id"),
        ("orders", "customer_id", "customers", "customer_id"),
        ("order_items", "order_id", "orders", "order_id"),
        ("order_items", "product_id", "products", "product_id")
    ]
    for child, child_key, parent, parent_key in checks:
        missing = set(tables[child][child_key]) - set(tables[parent][parent_key])
        if missing:
            raise ValueError(f"Invalid relationship: {child}.{child_key} has keys not found in {parent}.{parent_key}: {sorted(missing)}")
    numeric_nonnegative = {
        "employees": ["salary"],
        "products": ["unit_price", "stock_quantity"],
        "order_items": ["quantity", "unit_price"]
    }
    for table, columns in numeric_nonnegative.items():
        for column in columns:
            if (tables[table][column] < 0).any():
                raise ValueError(f"Negative values found in {table}.{column}")
