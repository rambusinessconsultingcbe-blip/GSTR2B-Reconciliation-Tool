# Financial Dashboard App

Python + PostgreSQL + Streamlit dashboard for management KPIs, MIS reporting, financial statements, source-data uploads, and ledger mapping.

## Modules

1. Executive Dashboard – management KPIs, monthly performance, trends, and analytics.
2. Sales MIS – Year → Month → Customer → Invoice → Item.
3. Production MIS – Year → Month → Customer → Product → Batch.
4. P&L – month-wise columns, percentage on sales, and ledger drill-down.
5. Balance Sheet – month-wise view with explicit Net Liabilities vs Net Assets control.
6. Cash Flow – Operating, Investing, Financing, and Closing Cash.
7. Ratios & KPIs – profitability, liquidity, working capital, sales, and production ratios.
8. Customer Analysis – sales, outstanding, ageing, profitability, and drill-down.
9. Supplier Analysis – purchase/consumption, outstanding, ageing, and dependency analytics.
10. Drill-down Transactions – shared transaction-level layer for all reports.
11. Source Data – Excel upload and validation for finance and production sources.
12. Mapping & Configuration – primary group and report-line mapping.

## Source data supported

The initial upload template configuration supports:

- Sales
- Production data
- Trial Balance
- Sundry Debtors
- Sundry Creditors
- Coal consumption
- Chemical consumption

## Tech stack

- Python backend and data processing
- PostgreSQL production database
- Streamlit dashboard UI
- pandas and openpyxl for Excel ingestion
- Plotly for interactive charts
- SQLAlchemy for database access

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/dashboard.py
```

Set `DATABASE_URL` in `.env` for PostgreSQL. If it is not set, the app falls back to a local SQLite development database URL for early prototyping.

## Database setup

Create the PostgreSQL database, update `.env`, and apply `db/schema.sql` using your preferred SQL client. The schema includes upload tracking, account mapping, sales facts, production facts, and trial-balance facts.

## Testing

```bash
python -m pytest tests
```
