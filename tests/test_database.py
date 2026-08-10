from __future__ import annotations

import pytest

from synthgen.columns import IntColumn, NameColumn
from synthgen.database import DuckDBStorage, duckdb_connection


def test_duckdb_connection_closes_after_context(tmp_path):
    db_path = tmp_path / "test.duckdb"
    with duckdb_connection(db_path) as conn:
        conn.execute("SELECT 1")

    with pytest.raises(Exception):
        conn.execute("SELECT 1")


def test_store_creates_table_and_inserts_rows(tmp_path):
    db_path = tmp_path / "test.duckdb"
    storage = DuckDBStorage(db_path)
    columns = [IntColumn(name="id", min_value=0, max_value=10), NameColumn(name="name")]
    rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    storage.store("people", rows, columns)

    with duckdb_connection(db_path) as conn:
        assert conn.execute("SELECT COUNT(*) FROM people").fetchone()[0] == 2


def test_store_replace_true_recreates_table(tmp_path):
    db_path = tmp_path / "test.duckdb"
    storage = DuckDBStorage(db_path)
    columns = [IntColumn(name="id", min_value=0, max_value=10)]

    storage.store("t", [{"id": 1}, {"id": 2}], columns, replace=True)
    storage.store("t", [{"id": 3}], columns, replace=True)

    with duckdb_connection(db_path) as conn:
        assert conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 1


def test_store_with_no_rows_does_not_raise(tmp_path):
    db_path = tmp_path / "test.duckdb"
    storage = DuckDBStorage(db_path)
    storage.store("empty", [], [IntColumn(name="id")])