from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: list[str]
    warnings: list[str]


def normalize_columns(columns: Iterable[str]) -> list[str]:
    return [str(column).strip().lower().replace(" ", "_") for column in columns]


def validate_dataframe(df: pd.DataFrame, required_columns: Iterable[str]) -> ValidationResult:
    normalized = normalize_columns(df.columns)
    missing = [column for column in required_columns if column not in normalized]
    errors: list[str] = []
    warnings: list[str] = []

    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
    if df.empty:
        errors.append("Uploaded file does not contain any rows.")
    duplicate_columns = sorted({column for column in normalized if normalized.count(column) > 1})
    if duplicate_columns:
        warnings.append(f"Duplicate columns detected after normalization: {', '.join(duplicate_columns)}")

    return ValidationResult(is_valid=not errors, errors=errors, warnings=warnings)
