from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ServerSelection:
    server_id: str
    region: str


@dataclass(frozen=True)
class BaseCharacter:
    race: str
    gender: str
    age: int


@dataclass(frozen=True)
class DyeOverride:
    rgb: tuple[int, int, int]


@dataclass(frozen=True)
class EquippedItem:
    item_id: str
    dye_hint_rgb: tuple[int, int, int] | None = None
    dye_override: DyeOverride | None = None


@dataclass(frozen=True)
class LookPreset:
    schema_version: int
    server: ServerSelection
    base: BaseCharacter
    equipped: dict[str, EquippedItem] = field(default_factory=dict)
