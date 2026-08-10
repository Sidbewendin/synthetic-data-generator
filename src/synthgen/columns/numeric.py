"""Colonnes numériques : entiers et flottants, bornés par min/max."""

from __future__ import annotations

import random
from dataclasses import dataclass

from faker import Faker

from .base import ColumnGenerator


@dataclass
class IntColumn(ColumnGenerator):
    """Colonne d'entiers aléatoires compris entre min_value et max_value."""

    min_value: int = 0
    max_value: int = 100

    def __post_init__(self) -> None:
        if self.min_value > self.max_value:
            raise ValueError(
                f"min_value ({self.min_value}) doit être <= max_value ({self.max_value})"
            )

    def generate(self, faker: Faker) -> int:
        return random.randint(self.min_value, self.max_value)

    @property
    def duckdb_type(self) -> str:
        return "BIGINT"


@dataclass
class FloatColumn(ColumnGenerator):
    """Colonne de flottants aléatoires compris entre min_value et max_value."""

    min_value: float = 0.0
    max_value: float = 1.0
    round_digits: int = 2

    def __post_init__(self) -> None:
        if self.min_value > self.max_value:
            raise ValueError(
                f"min_value ({self.min_value}) doit être <= max_value ({self.max_value})"
            )

    def generate(self, faker: Faker) -> float:
        return round(random.uniform(self.min_value, self.max_value), self.round_digits)

    @property
    def duckdb_type(self) -> str:
        return "DOUBLE"