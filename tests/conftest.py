from __future__ import annotations

import pytest

from api_service.data.store import InMemoryStore


@pytest.fixture
def seeded_store() -> None:
    """Fresh in-memory DB with default seed customers and accounts."""
    InMemoryStore.customers.clear()
    InMemoryStore.accounts.clear()
    InMemoryStore.seeded = False
    InMemoryStore.seed_data()
    yield
    InMemoryStore.customers.clear()
    InMemoryStore.accounts.clear()
    InMemoryStore.seeded = False


@pytest.fixture
def empty_store() -> None:
    """Empty store (no seed data)."""
    InMemoryStore.customers.clear()
    InMemoryStore.accounts.clear()
    InMemoryStore.seeded = True
    yield
    InMemoryStore.customers.clear()
    InMemoryStore.accounts.clear()
    InMemoryStore.seeded = False
