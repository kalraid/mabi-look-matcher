from __future__ import annotations

from dataclasses import dataclass

from look_matcher.catalog_store.store import CatalogStore
from look_matcher.loadout.state import LoadoutState


@dataclass(frozen=True)
class PreviewLayer:
    slot_id: str
    item_id: str
    label: str
    color_rgb: tuple[int, int, int] | None
    placeholder: bool


class FlatPreviewComposer:
    """Build ordered 2D preview layers from LoadoutState + Catalog."""

    def __init__(self, *, catalog: CatalogStore, slot_order: list[str]) -> None:
        self._catalog = catalog
        self._slot_order = slot_order

    def compose(self, loadout: LoadoutState) -> list[PreviewLayer]:
        layers: list[PreviewLayer] = []
        equipped = loadout.equipped

        for slot_id in self._slot_order:
            item = equipped.get(slot_id)
            if item is None:
                continue

            entries = self._catalog.search(
                slot_id=slot_id,
                server_id=loadout.snapshot().server.server_id,
                query="",
                limit=50,
            )
            meta = next((e for e in entries if e.id == item.item_id), None)
            label = meta.display_name_ko if meta else item.item_id
            has_thumb = meta is not None and meta.thumbnail_url is not None

            layers.append(
                PreviewLayer(
                    slot_id=slot_id,
                    item_id=item.item_id,
                    label=label,
                    color_rgb=loadout.effective_rgb(slot_id),
                    placeholder=not has_thumb,
                )
            )

        return layers
