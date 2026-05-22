"""LoadoutState — Click Equip and dye (public interface)."""

from look_matcher.loadout import CatalogItemRef, LoadoutState
from look_matcher.look_preset import (
    BaseCharacter,
    LookPresetCodec,
    ServerSelection,
)


def _base_loadout() -> LoadoutState:
    return LoadoutState(
        server=ServerSelection(server_id="mabikr1", region="kr"),
        base=BaseCharacter(race="human", gender="female", age=20),
    )


def test_click_equip_places_item_and_snapshot_round_trip() -> None:
    loadout = _base_loadout()
    item = CatalogItemRef(item_id="item-001", dyeable=False)

    loadout.click_equip("body", item)

    snapshot = loadout.snapshot()
    assert snapshot.equipped["body"].item_id == "item-001"

    codec = LookPresetCodec()
    restored = LoadoutState.from_preset(codec.decode(codec.encode(snapshot)))
    assert restored.equipped["body"].item_id == "item-001"


def test_click_equip_on_dyeable_item_applies_dye_hint() -> None:
    loadout = _base_loadout()
    loadout.click_equip(
        "wings",
        CatalogItemRef(item_id="item-002", dyeable=True),
        dye_hint_rgb=(80, 20, 120),
    )

    assert loadout.effective_rgb("wings") == (80, 20, 120)


def test_dye_override_takes_precedence_over_dye_hint() -> None:
    loadout = _base_loadout()
    loadout.click_equip(
        "wings",
        CatalogItemRef(item_id="item-002", dyeable=True),
        dye_hint_rgb=(80, 20, 120),
    )
    loadout.set_dye_override("wings", (90, 30, 130))

    assert loadout.effective_rgb("wings") == (90, 30, 130)
    assert loadout.snapshot().equipped["wings"].dye_override is not None


def test_re_equip_clears_override_and_applies_new_hint() -> None:
    loadout = _base_loadout()
    loadout.click_equip(
        "body",
        CatalogItemRef(item_id="item-001", dyeable=True),
        dye_hint_rgb=(10, 10, 10),
    )
    loadout.set_dye_override("body", (99, 99, 99))

    loadout.click_equip(
        "body",
        CatalogItemRef(item_id="item-003", dyeable=True),
        dye_hint_rgb=(20, 30, 40),
    )

    assert loadout.equipped["body"].item_id == "item-003"
    assert loadout.equipped["body"].dye_override is None
    assert loadout.effective_rgb("body") == (20, 30, 40)
