import logging
from .extract import extract_workbook
from .transform import transform_tables
from .load import create_database_engine, load_tables
from .config import PROCESSED_PATH

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def run_pipeline():
    raw = extract_workbook()
    logging.info("Extracted tables: %s", {name: len(frame) for name, frame in raw.items()})
    cleaned = transform_tables(raw)
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
    for name, frame in cleaned.items():
        frame.to_csv(PROCESSED_PATH / f"{name}.csv", index=False, encoding="utf-8-sig")
    engine = create_database_engine()
    load_tables(cleaned, engine)
    logging.info("ETL completed successfully. Loaded rows: %s", {name: len(frame) for name, frame in cleaned.items()})
    engine.dispose()

if __name__ == "__main__":
    run_pipeline()
