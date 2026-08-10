"""Export d'un dataset généré vers un fichier CSV ou JSON."""

from __future__ import annotations

import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path

from .logger import get_logger

logger = get_logger(__name__)


class Exporter(ABC):
    """Contrat commun à tout export de dataset vers un fichier."""

    extension: str

    @abstractmethod
    def export(self, rows: list[dict[str, object]], output_path: Path) -> None:
        """Écrit `rows` dans `output_path`."""
        raise NotImplementedError


class CSVExporter(Exporter):
    extension = "csv"

    def export(self, rows: list[dict[str, object]], output_path: Path) -> None:
        if not rows:
            logger.warning("Aucune ligne à exporter vers %s", output_path)
            return
        fieldnames = list(rows[0].keys())
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.info("%d lignes exportées en CSV vers %s", len(rows), output_path)


class JSONExporter(Exporter):
    extension = "json"

    def export(self, rows: list[dict[str, object]], output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        logger.info("%d lignes exportées en JSON vers %s", len(rows), output_path)


_EXPORTERS: dict[str, type[Exporter]] = {
    "csv": CSVExporter,
    "json": JSONExporter,
}


def get_exporter(output_format: str) -> Exporter:
    """Factory : retourne l'exporter adapté au format demandé."""
    try:
        exporter_cls = _EXPORTERS[output_format]
    except KeyError as exc:
        raise ValueError(f"Format d'export inconnu: {output_format!r}") from exc
    return exporter_cls()