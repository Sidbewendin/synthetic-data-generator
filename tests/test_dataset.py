from __future__ import annotations

import pytest

from synthgen.columns import IntColumn, NameColumn
from synthgen.dataset import Dataset, DatasetConfig


def _make_config(**overrides: object) -> DatasetConfig:
    defaults: dict[str, object] = dict(
        name="test_ds",
        table_name="test_table",
        n_rows=10,
        output_format="csv",
        columns=[
            IntColumn(name="id", min_value=0, max_value=100),
            NameColumn(name="name"),
        ],
    )
    defaults.update(overrides)
    return DatasetConfig(**defaults)  # type: ignore[arg-type]


def test_dataset_config_rejects_empty_columns():
    with pytest.raises(ValueError):
        _make_config(columns=[])


def test_dataset_config_rejects_duplicate_column_names():
    with pytest.raises(ValueError):
        _make_config(columns=[IntColumn(name="id"), NameColumn(name="id")])


def test_dataset_config_rejects_non_positive_n_rows():
    with pytest.raises(ValueError):
        _make_config(n_rows=0)


def test_dataset_config_rejects_bad_output_format():
    with pytest.raises(ValueError):
        _make_config(output_format="xml")


def test_generate_rows_count_and_keys():
    config = _make_config(n_rows=15)
    rows = Dataset(config).generate_rows()
    assert len(rows) == 15
    assert set(rows[0].keys()) == {"id", "name"}


def test_generate_rows_is_reproducible_with_seed():
    config = _make_config(seed=123, n_rows=5)
    rows_a = Dataset(config).generate_rows()
    rows_b = Dataset(config).generate_rows()
    assert rows_a == rows_b