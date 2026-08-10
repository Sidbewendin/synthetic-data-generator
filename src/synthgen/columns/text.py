"""Colonnes textuelles.

StringColumn est une classe abstraite intermédiaire : elle factorise le
duckdb_type commun (VARCHAR) mais laisse chaque sous-type définir sa
propre logique de génération via Faker.
"""

from __future__ import annotations

import random
import string
from abc import ABC
from dataclasses import dataclass

from faker import Faker

from .base import ColumnGenerator


@dataclass
class StringColumn(ColumnGenerator, ABC):
    """Classe abstraite intermédiaire pour toute colonne textuelle."""

    @property
    def duckdb_type(self) -> str:
        return "VARCHAR"


@dataclass
class NameColumn(StringColumn):
    """Colonne de noms de personnes (Faker)."""

    def generate(self, faker: Faker) -> str:
        return faker.name()


@dataclass
class AddressColumn(StringColumn):
    """Colonne d'adresses postales (Faker), sur une seule ligne."""

    def generate(self, faker: Faker) -> str:
        return faker.address().replace("\n", ", ")


@dataclass
class IPColumn(StringColumn):
    """Colonne d'adresses IP, en v4 ou v6."""

    version: int = 4

    def __post_init__(self) -> None:
        if self.version not in (4, 6):
            raise ValueError("version doit être 4 ou 6")

    def generate(self, faker: Faker) -> str:
        return faker.ipv4() if self.version == 4 else faker.ipv6()


@dataclass
class RandomStringColumn(StringColumn):
    """Colonne de chaînes aléatoires (lettres + chiffres) de longueur fixe."""

    length: int = 10

    def generate(self, faker: Faker) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(random.choices(alphabet, k=self.length))