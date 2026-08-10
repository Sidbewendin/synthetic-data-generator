# synthgen - Générateur de données synthétiques

## Contexte

En entreprise, on a régulièrement besoin de tester du code ou des analyses
(avant mise en production) sans utiliser de vraies données utilisateurs, que
ce soit pour des raisons de sécurité, de confidentialité, ou simplement parce
qu'on n'a pas encore de données réelles. synthgen génère des jeux de
données **synthétiques**, **configurables**, prêts à être utilisés dans un
environnement de développement/test.

## Fonctionnalités

- Génère **plusieurs datasets différents** en une seule exécution.
- Chaque dataset est entièrement **configurable** :
  - nom et type de chaque colonne ;
  - pour les colonnes numériques : bornes min/max;
  - pour les colonnes texte : nom, adresse, IP, ou string aléatoire;
  - format d'export : CSV ou JSON;
  - nom de la table où le dataset est stocké.
- Stockage automatique dans une base **DuckDB**.
- Export du dataset vers un fichier **CSV** ou **JSON**.

## Stack technique

| Outil       | Rôle                                                  |
|-------------|--------------------------------------------------------|
| **Faker**   | Génération de valeurs réalistes (noms, adresses, IP)  |
| **DuckDB**  | Base de données locale où sont stockés les datasets   |
| **Git**     | Versioning du code (une branche par fonctionnalité)   |
| **pytest**  | Tests unitaires + couverture de code                   |

## Installation

###bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"

## Utilisation

Un exemple complet est fourni dans main.py : il génère deux datasets
différents (users et transactions), chacun avec sa propre configuration.

###bash
python main.py


Cela va :
1. générer les lignes de chaque dataset (via Faker) ;
2. les stocker dans synthgen.duckdb, dans la table configurée pour chaque dataset ;
3. les exporter dans output/ au format demandé (CSV ou JSON).

### Définir son propre dataset

###python
from synthgen import (
    DatasetConfig,
    IntColumn,
    FloatColumn,
    NameColumn,
    AddressColumn,
    IPColumn,
    RandomStringColumn,
    SyntheticDataGenerator,
)

config = DatasetConfig(
    name="clients",
    table_name="clients",
    n_rows=1000,
    output_format="json",
    seed=42,
    columns=[
        IntColumn(name="id", min_value=1, max_value=100_000),
        NameColumn(name="nom_complet"),
        AddressColumn(name="adresse"),
        IPColumn(name="ip", version=4),
        FloatColumn(name="solde", min_value=0.0, max_value=5000.0, round_digits=2),
        RandomStringColumn(name="token", length=12),
    ],
)

generator = SyntheticDataGenerator(db_path="synthgen.duckdb", output_dir="output")
generator.run(config)


## Architecture du projet

###
src/synthgen/
├── columns/
│   ├── base.py      # ColumnGenerator (classe abstraite)
│   ├── numeric.py   # IntColumn, FloatColumn
│   └── text.py      # StringColumn (abstraite) -> NameColumn, AddressColumn, IPColumn, RandomStringColumn
├── dataset.py        # DatasetConfig (dataclass) + Dataset (génère les lignes)
├── database.py        # DuckDBStorage + context manager pour la connexion
├── exporters.py        # Exporter (abstraite) -> CSVExporter, JSONExporter
├── generator.py          # SyntheticDataGenerator : orchestre le tout
└── logger.py              # Configuration centralisée du logging
####

Chaque type de colonne hérite de ColumnGenerator (classe abstraite) et
implémente sa propre méthode generate() ainsi que son type SQL DuckDB
correspondant (duckdb_type). Ajouter un nouveau type de colonne se fait
donc sans toucher au reste du code.

La connexion DuckDB est gérée via un **context manager** (duckdb_connection),
ce qui garantit sa fermeture même en cas d'erreur pendant l'insertion.

## Tests

###bash
pytest --cov


La suite de tests utilise des **fixtures** (Faker, chemins temporaires) et
la **paramétrisation** pytest pour couvrir plusieurs bornes, versions d'IP et
longueurs de chaînes sans dupliquer le code de test.