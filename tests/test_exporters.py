from __future__ import annotations

import csv
import json

import pytest

from synthgen.exporters import CSVExporter, JSONExporter, get_exporter

SAMPLE_ROWS: list[dict[str, object]] = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]


def test_csv_exporter_writes_correct_content(tmp_path):
    output_path = tmp_path / "out.csv"
    CSVExporter().export(SAMPLE_ROWS, output_path)

    with output_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"


def test_json_exporter_writes_correct_content(tmp_path):
    output_path = tmp_path / "out.json"
    JSONExporter().export(SAMPLE_ROWS, output_path)

    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert data == SAMPLE_ROWS


@pytest.mark.parametrize(
    "fmt, expected_cls",
    [("csv", CSVExporter), ("json", JSONExporter)],
)
def test_get_exporter_factory(fmt, expected_cls):
    assert isinstance(get_exporter(fmt), expected_cls)


def test_get_exporter_unknown_format_raises():
    with pytest.raises(ValueError):
        get_exporter("xml")