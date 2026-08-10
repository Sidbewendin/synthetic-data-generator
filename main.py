"""Exemple d'utilisation de synthgen.

Simule un cas d'entreprise : on veut tester du code / des analyses sans
utiliser de vraies données utilisateurs. On génère ici deux datasets
différents, chacun configurable indépendamment (colonnes, types, bornes,
format d'export, table de stockage).
"""

from __future__ import annotations

from synthgen import (
    AddressColumn,
    DatasetConfig,
    FloatColumn,
    IntColumn,
    IPColumn,
    NameColumn,
    RandomStringColumn,
    SyntheticDataGenerator,
)


def build_users_dataset() -> DatasetConfig:
    """Dataset 'users' : exporté en CSV, stocké dans la table 'users'."""
    return DatasetConfig(
        name="users",
        table_name="users",
        n_rows=200,
        output_format="csv",
        seed=42,
        columns=[
            IntColumn(name="id", min_value=1, max_value=1_000_000),
            NameColumn(name="full_name"),
            AddressColumn(name="address"),
            IPColumn(name="last_login_ip", version=4),
            IntColumn(name="age", min_value=18, max_value=90),
            RandomStringColumn(name="api_token", length=16),
        ],
    )


def build_transactions_dataset() -> DatasetConfig:
    """Dataset 'transactions' : exporté en JSON, stocké dans la table 'transactions'."""
    return DatasetConfig(
        name="transactions",
        table_name="transactions",
        n_rows=500,
        output_format="json",
        seed=42,
        columns=[
            IntColumn(name="transaction_id", min_value=1, max_value=10_000_000),
            IntColumn(name="user_id", min_value=1, max_value=1_000_000),
            FloatColumn(name="amount", min_value=0.5, max_value=2500.0, round_digits=2),
            IPColumn(name="origin_ip", version=4),
        ],
    )


def main() -> None:
    generator = SyntheticDataGenerator(db_path="synthgen.duckdb", output_dir="output")
    output_paths = generator.run_many(
        [build_users_dataset(), build_transactions_dataset()]
    )
    for path in output_paths:
        print(f"Dataset généré : {path}")


if __name__ == "__main__":
    main()