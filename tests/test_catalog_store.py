"""CatalogStore — server/slot text search (public interface)."""

from pathlib import Path

import pytest

from look_matcher.catalog_store import CatalogStore


@pytest.fixture
def store(repo_root: Path) -> CatalogStore:
    return CatalogStore.from_snapshot_file(
        repo_root / "tests/fixtures/catalog/minimal.json"
    )


def test_search_filters_by_slot_and_server(store: CatalogStore) -> None:
    results = store.search(slot_id="body", server_id="mabikr1", query="", limit=10)

    assert len(results) == 1
    assert results[0].display_name_ko == "서큐버스의 옷"
    assert results[0].dyeable is False


def test_search_matches_korean_query(store: CatalogStore) -> None:
    results = store.search(slot_id="wings", server_id="mabikr1", query="데빌", limit=10)

    assert len(results) == 1
    assert "데빌" in results[0].display_name_ko


def test_search_respects_limit(store: CatalogStore) -> None:
    results = store.search(slot_id="body", server_id="mabikr1", query="", limit=1)

    assert len(results) <= 1


def test_search_unknown_server_returns_empty(store: CatalogStore) -> None:
    results = store.search(slot_id="body", server_id="mabijp1", query="", limit=10)

    assert results == []


def test_sqlite_provider_is_stub_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="sqlite"):
        CatalogStore.from_sqlite(Path("data/catalog.sqlite"))


def test_get_catalog_store_uses_mock_fixture(settings) -> None:
    from look_matcher.catalog_store import get_catalog_store

    store = get_catalog_store()
    results = store.search(slot_id="wings", server_id="mabikr1", query="데빌", limit=5)

    assert len(results) >= 1
