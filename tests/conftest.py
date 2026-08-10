from __future__ import annotations

import pytest
from faker import Faker


@pytest.fixture
def faker_instance() -> Faker:
    """Instance Faker partagée par les tests qui génèrent des valeurs."""
    return Faker()