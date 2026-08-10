"""synthgen : générateur de données synthétiques configurables."""

from .columns import (
    AddressColumn,
    FloatColumn,
    IntColumn,
    IPColumn,
    NameColumn,
    RandomStringColumn,
)
from .dataset import DatasetConfig
from .generator import SyntheticDataGenerator

__version__ = "0.1.0"

__all__ = [
    "SyntheticDataGenerator",
    "DatasetConfig",
    "IntColumn",
    "FloatColumn",
    "NameColumn",
    "AddressColumn",
    "IPColumn",
    "RandomStringColumn",
]