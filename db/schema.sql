CREATE TABLE IF NOT EXISTS source_uploads (
    id BIGSERIAL PRIMARY KEY,
    source_type TEXT NOT NULL,
    file_name TEXT NOT NULL,
    row_count INTEGER NOT NULL DEFAULT 0,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS account_mapping (
    id BIGSERIAL PRIMARY KEY,
    ledger_name TEXT NOT NULL UNIQUE,
    primary_group TEXT NOT NULL,
    report_section TEXT NOT NULL,
    report_line TEXT NOT NULL,
    cash_flow_type TEXT,
    normal_sign TEXT NOT NULL CHECK (normal_sign IN ('debit', 'credit'))
);

CREATE TABLE IF NOT EXISTS fact_sales (
    id BIGSERIAL PRIMARY KEY,
    invoice_date DATE NOT NULL,
    invoice_number TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    item_name TEXT NOT NULL,
    quantity NUMERIC(18, 4) NOT NULL DEFAULT 0,
    taxable_value NUMERIC(18, 2) NOT NULL DEFAULT 0,
    upload_id BIGINT REFERENCES source_uploads(id)
);

CREATE TABLE IF NOT EXISTS fact_production (
    id BIGSERIAL PRIMARY KEY,
    production_date DATE NOT NULL,
    customer_name TEXT NOT NULL,
    product_name TEXT NOT NULL,
    batch_number TEXT NOT NULL,
    quantity NUMERIC(18, 4) NOT NULL DEFAULT 0,
    upload_id BIGINT REFERENCES source_uploads(id)
);

CREATE TABLE IF NOT EXISTS fact_trial_balance (
    id BIGSERIAL PRIMARY KEY,
    period DATE NOT NULL,
    ledger_name TEXT NOT NULL,
    debit NUMERIC(18, 2) NOT NULL DEFAULT 0,
    credit NUMERIC(18, 2) NOT NULL DEFAULT 0,
    upload_id BIGINT REFERENCES source_uploads(id)
);
