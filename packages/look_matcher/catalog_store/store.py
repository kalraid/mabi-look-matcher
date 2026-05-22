from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from look_matcher.config import get_settings


@dataclass(frozen=True)
class CatalogEntry:
    id: str
    display_name_ko: str
    slot_ids: list[str]
    dyeable: bool
    server_ids: list[str] = field(default_factory=list)
    thumbnail_url: str | None = None
    equip_id: str | None = None
    category: str | None = None


class CatalogStore:
    """Read-only Item Catalog search."""

    def __init__(self, items: list[CatalogEntry]) -> None:
        self._items = items

    @classmethod
    def from_snapshot_file(cls, path: Path) -> CatalogStore:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        raw_items = data.get("items", data if isinstance(data, list) else [])
        entries: list[CatalogEntry] = []
        for row in raw_items:
            if not isinstance(row, dict):
                continue
            server_ids = list(row.get("server_ids", []))
            entries.append(
                CatalogEntry(
                    id=str(row.get("id", "")),
                    display_name_ko=str(row.get("display_name_ko", "")),
                    slot_ids=list(row.get("slot_ids", [])),
                    dyeable=bool(row.get("dyeable", False)),
                    server_ids=server_ids,
                    thumbnail_url=row.get("thumbnail_url"),
                    equip_id=row.get("equip_id"),
                    category=row.get("category"),
                )
            )
        return cls(entries)

    @classmethod
    def from_sqlite(cls, path: Path) -> CatalogStore:
        raise NotImplementedError(
            f"sqlite CatalogStore not implemented yet (path={path})"
        )

    def search(
        self,
        *,
        slot_id: str,
        server_id: str,
        query: str,
        limit: int = 10,
    ) -> list[CatalogEntry]:
        q = query.strip().lower()
        matches: list[CatalogEntry] = []

        for item in self._items:
            if slot_id not in item.slot_ids:
                continue
            if item.server_ids and server_id not in item.server_ids:
                continue
            if q and q not in item.display_name_ko.lower():
                if not (item.category and q in item.category.lower()):
                    continue
            matches.append(item)
            if len(matches) >= limit:
                break

        return matches


def get_catalog_store() -> CatalogStore:
    """Factory: mock fixture or catalog snapshot from settings."""
    settings = get_settings()
    if settings.catalog.provider == "mock":
        path = settings.catalog_fixture_path() or settings.resolve_path(
            settings.catalog.mock.fixture_path
        )
    else:
        path = settings.resolve_path(settings.catalog.snapshot_path)
    return CatalogStore.from_snapshot_file(path)
