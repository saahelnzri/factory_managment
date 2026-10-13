from sqlalchemy import MetaData, Table, inspect
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from .config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

TABLE_ORDER = ["departments", "employees", "products", "customers", "orders", "order_items"]
PRIMARY_KEYS = {
    "departments": "department_id",
    "employees": "employee_id",
    "products": "product_id",
    "customers": "customer_id",
    "orders": "order_id",
    "order_items": "order_item_id"
}

def create_database_engine():
    url = URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        query={"charset": "utf8mb4"}
    )
    return create_engine(url, pool_pre_ping=True)

def load_tables(tables, engine, batch_size=500):
    existing_tables = set(inspect(engine).get_table_names())
    missing_tables = set(TABLE_ORDER) - existing_tables
    if missing_tables:
        raise RuntimeError(
            f"Missing MySQL tables: {sorted(missing_tables)}. Run sql/schema.sql in MySQL Workbench first."
        )

    metadata = MetaData()
    reflected = {
        name: Table(name, metadata, autoload_with=engine)
        for name in TABLE_ORDER
    }

    with engine.begin() as connection:
        for name in TABLE_ORDER:
            frame = tables[name].drop(columns=["line_total"], errors="ignore")
            if frame.empty:
                continue

            table = reflected[name]
            primary_key = PRIMARY_KEYS[name]
            valid_columns = {column.name for column in table.columns}
            frame = frame[[column for column in frame.columns if column in valid_columns]]
            records = frame.astype(object).where(frame.notna(), None).to_dict(orient="records")
            update_columns = [column for column in frame.columns if column != primary_key]

            for start in range(0, len(records), batch_size):
                batch = records[start:start + batch_size]
                statement = insert(table).values(batch)
                if update_columns:
                    statement = statement.on_duplicate_key_update(
                        **{column: statement.inserted[column] for column in update_columns}
                    )
                connection.execute(statement)
