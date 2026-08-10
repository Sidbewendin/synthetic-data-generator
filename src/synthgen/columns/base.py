"""Classe de base abstraite pour tous les générateurs de colonnes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from faker import Faker


@dataclass
class ColumnGenerator(ABC):
    """Contrat commun à toute colonne configurable d'un dataset.

    Attributes:
        name: nom de la colonne, utilisé comme en-tête CSV / clé JSON /
            nom de colonne dans DuckDB.
    """

    name: str

    @abstractmethod
    def generate(self, faker: Faker) -> Any:
        """Génère une valeur unique pour cette colonne."""
        raise NotImplementedError

    @property
    @abstractmethod
    def duckdb_type(self) -> str:
        """Type SQL DuckDB à utiliser pour créer la colonne en base."""
        raise NotImplementedError