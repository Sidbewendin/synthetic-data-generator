"""Point d'entrée haut niveau : relie génération, stockage et export."""

from __future__ import annotations

from pathlib import Path

from .database import DuckDBStorage
from .dataset import Dataset, DatasetConfig
from .exporters import get_exporter
from .logger import get_logger

logger = get_logger(__name__)


class SyntheticDataGenerator:
    """Orchestre la génération complète d'un ou plusieurs datasets :
    génération des lignes -> stockage DuckDB -> export CSV/JSON.
    """

    def __init__(
        self,
        db_path: str | Path = "synthgen.duckdb",
        output_dir: str | Path = "output",
    ) -> None:
        self.storage = DuckDBStorage(db_path)
        self.output_dir = Path(output_dir)

    def run(self, config: DatasetConfig) -> Path:
        """Génère un dataset, le stocke dans DuckDB, l'exporte, puis retourne
        le chemin du fichier exporté.
        """
        dataset = Dataset(config)
        rows = dataset.generate_rows()

        self.storage.store(config.table_name, rows, config.columns)

        exporter = get_exporter(config.output_format)
        output_path = self.output_dir / f"{config.name}.{exporter.extension}"
        exporter.export(rows, output_path)

        return output_path

    def run_many(self, configs: list[DatasetConfig]) -> list[Path]:
        """Génère plusieurs datasets différents en une seule fois."""
        logger.info("Génération de %d dataset(s)", len(configs))
        return [self.run(config) for config in configs]