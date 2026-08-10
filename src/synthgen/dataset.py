"""Configuration et génération d'un dataset synthétique."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Literal

from faker import Faker

from .columns.base import ColumnGenerator
from .logger import get_logger

logger = get_logger(__name__)

OutputFormat = Literal["csv", "json"]


@dataclass
class DatasetConfig:
    """Configuration complète d'un dataset à générer.

    Attributes:
        name: nom logique du dataset (utilisé dans les logs / noms de fichier).
        columns: liste des colonnes configurables (voir `synthgen.columns`).
        table_name: nom de la table où stocker le dataset dans DuckDB.
        n_rows: nombre de lignes à générer.
        output_format: format d'export souhaité, "csv" ou "json".
        seed: graine aléatoire optionnelle, pour des résultats reproductibles.
    """

    name: str
    columns: list[ColumnGenerator]
    table_name: str
    n_rows: int = 100
    output_format: OutputFormat = "csv"
    seed: int | None = None

    def __post_init__(self) -> None:
        if not self.columns:
            raise ValueError("Un dataset doit avoir au moins une colonne")
        if self.n_rows <= 0:
            raise ValueError("n_rows doit être strictement positif")
        if self.output_format not in ("csv", "json"):
            raise ValueError("output_format doit être 'csv' ou 'json'")

        names = [c.name for c in self.columns]
        if len(names) != len(set(names)):
            raise ValueError("Les noms de colonnes doivent être uniques")


class Dataset:
    """Génère les lignes d'un dataset à partir de sa `DatasetConfig`."""

    def __init__(self, config: DatasetConfig) -> None:
        self.config = config
        self._faker = Faker()
        if config.seed is not None:
            Faker.seed(config.seed)
            random.seed(config.seed)

    @property
    def column_names(self) -> list[str]:
        return [col.name for col in self.config.columns]

    def generate_rows(self) -> list[dict[str, object]]:
        """Génère et retourne la liste des lignes (une ligne = un dict)."""
        logger.info(
            "Génération de %d lignes pour le dataset '%s' (%d colonnes)",
            self.config.n_rows,
            self.config.name,
            len(self.config.columns),
        )
        rows = [
            {col.name: col.generate(self._faker) for col in self.config.columns}
            for _ in range(self.config.n_rows)
        ]
        logger.info("Génération terminée pour '%s'", self.config.name)
        return rows