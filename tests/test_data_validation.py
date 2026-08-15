import pandas as pd

from app.data_validation import normalize_columns, validate_dataframe


def test_normalize_columns_removes_spaces_and_lowercases():
    assert normalize_columns(["Invoice Date", " Customer Name "]) == ["invoice_date", "customer_name"]


def test_validate_dataframe_reports_missing_columns():
    df = pd.DataFrame({"invoice_date": ["2026-04-01"]})
    result = validate_dataframe(df, ["invoice_date", "invoice_number"])

    assert not result.is_valid
    assert "Missing required columns: invoice_number" in result.errors


def test_validate_dataframe_accepts_required_columns():
    df = pd.DataFrame({"invoice_date": ["2026-04-01"], "invoice_number": ["A1"]})
    result = validate_dataframe(df, ["invoice_date", "invoice_number"])

    assert result.is_valid
    assert result.errors == []
