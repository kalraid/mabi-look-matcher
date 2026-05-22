"""FlatPreviewComposer — layer order and placeholders."""

from look_matcher.catalog_store import CatalogStore
from look_matcher.flat_preview import FlatPreviewComposer
from look_matcher.loadout import CatalogItemRef, LoadoutState
from look_matcher.look_preset import BaseCharacter, ServerSelection


def test_compose_respects_slot_order_and_placeholders(repo_root) -> None:
    catalog = CatalogStore.from_snapshot_file(
        repo_root / "tests/fixtures/catalog/minimal.json"
    )
    loadout = LoadoutState(
        server=ServerSelection(server_id="mabikr1", region="kr"),
        base=BaseCharacter(race="human", gender="female", age=20),
    )
    loadout.click_equip("body", CatalogItemRef("item-001", dyeable=False))
    loadout.click_equip(
        "wings",
        CatalogItemRef("item-002", dyeable=True),
        dye_hint_rgb=(4, 5, 6),
    )

    composer = FlatPreviewComposer(
        catalog=catalog,
        slot_order=["body", "wings", "shoes"],
    )
    layers = composer.compose(loadout)

    assert [layer.slot_id for layer in layers] == ["body", "wings"]
    assert all(layer.placeholder for layer in layers)
    assert layers[1].color_rgb == (4, 5, 6)
