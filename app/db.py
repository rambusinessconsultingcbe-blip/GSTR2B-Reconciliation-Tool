from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

load_dotenv()


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///finance_dashboard_dev.db")


def get_engine() -> Engine:
    return create_engine(get_database_url(), future=True)


def initialize_database(engine: Engine) -> None:
    schema_path = Path(__file__).resolve().parents[1] / "db" / "schema.sql"
    schema = schema_path.read_text(encoding="utf-8")
    with engine.begin() as connection:
        for statement in schema.split(";"):
            if statement.strip():
                connection.execute(text(statement))
