from __future__ import annotations

import pytest

from synthgen.columns import (
    AddressColumn,
    FloatColumn,
    IntColumn,
    IPColumn,
    NameColumn,
    RandomStringColumn,
)


@pytest.mark.parametrize("min_value, max_value", [(0, 10), (-5, 5), (100, 100)])
def test_int_column_within_bounds(faker_instance, min_value, max_value):
    column = IntColumn(name="n", min_value=min_value, max_value=max_value)
    for _ in range(50):
        value = column.generate(faker_instance)
        assert min_value <= value <= max_value


def test_int_column_invalid_bounds_raises():
    with pytest.raises(ValueError):
        IntColumn(name="n", min_value=10, max_value=0)


@pytest.mark.parametrize("min_value, max_value", [(0.0, 1.0), (-2.5, 2.5)])
def test_float_column_within_bounds(faker_instance, min_value, max_value):
    column = FloatColumn(name="f", min_value=min_value, max_value=max_value)
    for _ in range(50):
        value = column.generate(faker_instance)
        assert min_value <= value <= max_value


def test_float_column_invalid_bounds_raises():
    with pytest.raises(ValueError):
        FloatColumn(name="f", min_value=5.0, max_value=1.0)


def test_name_column_returns_str(faker_instance):
    assert isinstance(NameColumn(name="n").generate(faker_instance), str)


def test_address_column_has_no_newline(faker_instance):
    value = AddressColumn(name="a").generate(faker_instance)
    assert "\n" not in value


@pytest.mark.parametrize("version", [4, 6])
def test_ip_column_versions(faker_instance, version):
    value = IPColumn(name="ip", version=version).generate(faker_instance)
    assert isinstance(value, str)
    assert ("." in value) if version == 4 else (":" in value)


def test_ip_column_invalid_version_raises():
    with pytest.raises(ValueError):
        IPColumn(name="ip", version=5)


@pytest.mark.parametrize("length", [1, 8, 32])
def test_random_string_column_length(faker_instance, length):
    value = RandomStringColumn(name="s", length=length).generate(faker_instance)
    assert len(value) == length


def test_duckdb_types():
    assert IntColumn(name="n").duckdb_type == "BIGINT"
    assert FloatColumn(name="f").duckdb_type == "DOUBLE"
    assert NameColumn(name="s").duckdb_type == "VARCHAR"