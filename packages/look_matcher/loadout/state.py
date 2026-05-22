from __future__ import annotations

from dataclasses import dataclass

from look_matcher.look_preset.models import (
    BaseCharacter,
    DyeOverride,
    EquippedItem,
    LookPreset,
    ServerSelection,
)


@dataclass(frozen=True)
class CatalogItemRef:
    """Minimal item identity for Equip Action (catalog row subset)."""

    item_id: str
    dyeable: bool = False


class LoadoutState:
    """Mutable loadout: slot equips, Dye Hint, Dye Override."""

    def __init__(
        self,
        *,
        server: ServerSelection,
        base: BaseCharacter,
        schema_version: int = 1,
        equipped: dict[str, EquippedItem] | None = None,
    ) -> None:
        self._server = server
        self._base = base
        self._schema_version = schema_version
        self._equipped: dict[str, EquippedItem] = dict(equipped or {})

    @property
    def equipped(self) -> dict[str, EquippedItem]:
        return dict(self._equipped)

    @classmethod
    def from_preset(cls, preset: LookPreset) -> LoadoutState:
        return cls(
            server=preset.server,
            base=preset.base,
            schema_version=preset.schema_version,
            equipped=preset.equipped,
        )

    def click_equip(
        self,
        slot_id: str,
        item: CatalogItemRef,
        *,
        dye_hint_rgb: tuple[int, int, int] | None = None,
    ) -> None:
        hint = dye_hint_rgb if item.dyeable else None
        self._equipped[slot_id] = EquippedItem(
            item_id=item.item_id,
            dye_hint_rgb=hint,
            dye_override=None,
        )

    def set_dye_override(self, slot_id: str, rgb: tuple[int, int, int]) -> None:
        current = self._equipped.get(slot_id)
        if current is None:
            raise KeyError(f"slot not equipped: {slot_id}")
        self._equipped[slot_id] = EquippedItem(
            item_id=current.item_id,
            dye_hint_rgb=current.dye_hint_rgb,
            dye_override=DyeOverride(rgb=rgb),
        )

    def clear_dye_override(self, slot_id: str) -> None:
        current = self._equipped.get(slot_id)
        if current is None or current.dye_override is None:
            return
        self._equipped[slot_id] = EquippedItem(
            item_id=current.item_id,
            dye_hint_rgb=current.dye_hint_rgb,
            dye_override=None,
        )

    def effective_rgb(self, slot_id: str) -> tuple[int, int, int] | None:
        """Color for Flat Preview: Override > Hint."""
        current = self._equipped.get(slot_id)
        if current is None:
            return None
        if current.dye_override is not None:
            return current.dye_override.rgb
        return current.dye_hint_rgb

    def snapshot(self) -> LookPreset:
        return LookPreset(
            schema_version=self._schema_version,
            server=self._server,
            base=self._base,
            equipped=dict(self._equipped),
        )
