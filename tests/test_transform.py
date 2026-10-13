import pandas as pd
from src.transform import transform_tables

def sample_tables():
    return {
        "departments": pd.DataFrame([[1, "Production", "Tehran"]], columns=["department_id", "department_name", "city"]),
        "employees": pd.DataFrame([[1, "Sara", "Ahmadi", "Tehran", 1, 2000]], columns=["employee_id", "first_name", "last_name", "city", "department_id", "salary"]),
        "products": pd.DataFrame([[1, "Bolt", "Metal", 10, 100]], columns=["product_id", "product_name", "category", "unit_price", "stock_quantity"]),
        "customers": pd.DataFrame([[1, "Reza", "Karimi", "Tehran"]], columns=["customer_id", "first_name", "last_name", "city"]),
        "orders": pd.DataFrame([[1, 1, "2026-01-01", "Delivered"]], columns=["order_id", "customer_id", "order_date", "status"]),
        "order_items": pd.DataFrame([[1, 1, 1, 2, 10]], columns=["order_item_id", "order_id", "product_id", "quantity", "unit_price"])
    }

def test_transform_adds_line_total_and_preserves_rows():
    cleaned = transform_tables(sample_tables())
    assert len(cleaned["order_items"]) == 1
    assert cleaned["order_items"].iloc[0]["line_total"] == 20
    assert str(cleaned["orders"].iloc[0]["order_date"]).startswith("2026-01-01")

def test_duplicate_rows_are_removed():
    tables = sample_tables()
    tables["products"] = pd.concat([tables["products"], tables["products"]], ignore_index=True)
    cleaned = transform_tables(tables)
    assert len(cleaned["products"]) == 1
