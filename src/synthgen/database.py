"""Stockage des datasets générés dans DuckDB"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import duckdb

from .columns.base import ColumnGenerator
from .logger import get_logger

logger = get_logger(__name__)


@contextmanager
def duckdb_connection(
    db_path: str | Path = "synthgen.duckdb",
) -> Iterator[duckdb.DuckDBPyConnection]:
    """Ouvre une connexion DuckDB et garantit sa fermeture (try/finally)."""
    conn = duckdb.connect(str(db_path))
    logger.info("Connexion DuckDB ouverte (%s)", db_path)
    try:
        yield conn
    finally:
        conn.close()
        logger.info("Connexion DuckDB fermée (%s)", db_path)


class DuckDBStorage:
    """Encapsule la création de table et l'insertion d'un dataset dans DuckDB."""

    def __init__(self, db_path: str | Path = "synthgen.duckdb") -> None:
        self.db_path = db_path

    def store(
        self,
        table_name: str,
        rows: list[dict[str, object]],
        columns: list[ColumnGenerator],
        *,
        replace: bool = True,
    ) -> None:
        """Crée (ou recrée) une table et y insère les lignes générées.

        Args:
            table_name: nom de la table cible.
            rows: lignes générées (une ligne = un dict colonne -> valeur).
            columns: colonnes du dataset, utilisées pour déduire le type SQL.
            replace: si True, supprime la table existante avant de la recréer.
        """
        if not rows:
            logger.warning("Aucune ligne à stocker pour la table '%s'", table_name)
            return

        columns_sql = ", ".join(f'"{col.name}" {col.duckdb_type}' for col in columns)
        column_names = [col.name for col in columns]

        with duckdb_connection(self.db_path) as conn:
            if replace:
                conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
            conn.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_sql})')

            placeholders = ", ".join("?" for _ in column_names)
            columns_list_sql = ", ".join(f'"{name}"' for name in column_names)
            insert_sql = (
                f'INSERT INTO "{table_name}" ({columns_list_sql}) VALUES ({placeholders})'
            )
            values = [tuple(row[name] for name in column_names) for row in rows]
            conn.executemany(insert_sql, values)

            logger.info("%d lignes insérées dans la table '%s'", len(rows), table_name)