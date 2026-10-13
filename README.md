# Factory Management Analytics

A portfolio project for a small manufacturing company, built around six Excel sheets, a pandas ETL pipeline, MySQL relational tables, SQL analysis, and a Power BI data model.

## Stack

- Excel and pandas for source data and transformations
- MySQL for relational storage and analytical SQL
- Power BI for the semantic model, DAX measures, and report pages
- pytest for basic transformation checks

## Project structure

```text
factory_management_project/
├── data/raw/factory_data.xlsx
├── data/processed/
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
├── sql/
│   ├── schema.sql
│   ├── views.sql
│   └── analytics.sql
├── powerbi/
│   ├── DAX_Measures.dax
│   ├── Calendar_Table.dax
│   └── model_relationships.md
├── tests/
├── .env.example
└── requirements.txt
```

## Setup on Windows

1. Install MySQL Server and make sure the service is running.
2. Open this folder in VS Code.
3. Create a virtual environment in the terminal:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and enter your own MySQL password in `DB_PASSWORD`. Do not upload `.env` to GitHub.
5. Create the database and six relational tables by running `sql/schema.sql` in MySQL Workbench before running the ETL script.
6. Run the pipeline from the project root:

```powershell
python -m src.main
```

The pipeline reads all six sheets, trims text, removes duplicate rows, checks required values and relationships, writes cleaned CSV files under `data/processed/`, and upserts records into MySQL by primary key. It does not drop or rebuild tables. Matching IDs are updated from the workbook, new IDs are inserted, and rows that were removed from Excel are not automatically deleted from MySQL. Back up important data before testing ETL changes.

## SQL analysis

Run `sql/views.sql` to create reporting views and `sql/analytics.sql` to execute example analyses. The views use delivered orders for sales reporting. Update the status filter if your business rules differ.

## Power BI

1. In Power BI Desktop, choose Get Data → MySQL database.
2. Server: the value of `DB_HOST`; database: `factory_management`.
3. Import `departments`, `employees`, `products`, `customers`, `orders`, and `order_items`.
4. Create relationships described in `powerbi/model_relationships.md`.
5. Create the `Calendar` table using Modeling → New table and the expression in `powerbi/Calendar_Table.dax`. Add measures from `powerbi/DAX_Measures.dax` one by one through Modeling → New measure. Mark Calendar as the date table.
6. Build the report pages described in the model guide. Save the Power BI file as `reports/factory_management_dashboard.pbix`.

The `.pbix` file is not pre-generated because it must be created and saved from Power BI Desktop connected to your local MySQL instance. The DAX and model guide provide the reusable setup.

## Validation

```powershell
python -m pytest
```

## Data notes

The workbook currently contains 8 departments, 15 employees, 20 products, 15 customers, 20 orders, and 40 order-item rows. This is a compact demo dataset, suitable for demonstrating the workflow but small for drawing strong business conclusions. For a stronger portfolio case study, expand the data across several months and more orders before presenting performance trends.
