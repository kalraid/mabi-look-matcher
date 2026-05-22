from __future__ import annotations

import base64
import json
import zlib
from typing import Any

from look_matcher.config import get_settings
from look_matcher.look_preset.models import (
    BaseCharacter,
    DyeOverride,
    EquippedItem,
    LookPreset,
    ServerSelection,
)

SUPPORTED_SCHEMA_VERSIONS = {1}


class PresetDecodeError(ValueError):
    """Share Link or stored preset could not be restored."""


class LookPresetCodec:
    """Encode/decode Look Preset for Share Link and localStorage."""

    def __init__(self, *, max_encoded_length: int | None = None) -> None:
        settings = get_settings()
        self._max_len = max_encoded_length or int(
            settings.look_preset.get("max_encoded_length", 8000)
        )

    def encode(self, preset: LookPreset) -> str:
        if preset.schema_version not in SUPPORTED_SCHEMA_VERSIONS:
            raise ValueError(f"unsupported schema_version: {preset.schema_version}")

        payload = _preset_to_dict(preset)
        raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
        token = base64.urlsafe_b64encode(zlib.compress(raw, level=9)).decode("ascii")
        if len(token) > self._max_len:
            raise ValueError("encoded preset exceeds max_encoded_length")
        return token

    def decode(self, token: str) -> LookPreset:
        try:
            compressed = base64.urlsafe_b64decode(token.encode("ascii"))
            raw = zlib.decompress(compressed)
            data = json.loads(raw.decode("utf-8"))
        except (ValueError, json.JSONDecodeError, zlib.error, OSError) as exc:
            raise PresetDecodeError("invalid preset token") from exc

        if not isinstance(data, dict):
            raise PresetDecodeError("invalid preset payload")

        version = data.get("v")
        if version not in SUPPORTED_SCHEMA_VERSIONS:
            raise PresetDecodeError(f"unsupported schema version: {version}")

        return _dict_to_preset(data)


def _rgb_list(rgb: tuple[int, int, int] | None) -> list[int] | None:
    if rgb is None:
        return None
    return [rgb[0], rgb[1], rgb[2]]


def _rgb_tuple(values: list[int] | None) -> tuple[int, int, int] | None:
    if values is None:
        return None
    if len(values) != 3:
        raise PresetDecodeError("invalid rgb")
    return (int(values[0]), int(values[1]), int(values[2]))


def _preset_to_dict(preset: LookPreset) -> dict[str, Any]:
    equipped: dict[str, Any] = {}
    for slot_id, item in preset.equipped.items():
        entry: dict[str, Any] = {"id": item.item_id}
        hint = _rgb_list(item.dye_hint_rgb)
        if hint is not None:
            entry["hint"] = hint
        if item.dye_override is not None:
            entry["over"] = list(item.dye_override.rgb)
        equipped[slot_id] = entry

    return {
        "v": preset.schema_version,
        "server": {
            "server_id": preset.server.server_id,
            "region": preset.server.region,
        },
        "base": {
            "race": preset.base.race,
            "gender": preset.base.gender,
            "age": preset.base.age,
        },
        "equipped": equipped,
    }


def _dict_to_preset(data: dict[str, Any]) -> LookPreset:
    server_raw = data.get("server") or {}
    base_raw = data.get("base") or {}
    equipped_raw = data.get("equipped") or {}

    if not isinstance(server_raw, dict) or not isinstance(base_raw, dict):
        raise PresetDecodeError("invalid preset sections")

    equipped: dict[str, EquippedItem] = {}
    if isinstance(equipped_raw, dict):
        for slot_id, entry in equipped_raw.items():
            if not isinstance(entry, dict):
                continue
            item_id = entry.get("id")
            if not item_id:
                continue
            override = None
            if "over" in entry:
                override = DyeOverride(rgb=_rgb_tuple(entry["over"]))  # type: ignore[arg-type]
            equipped[str(slot_id)] = EquippedItem(
                item_id=str(item_id),
                dye_hint_rgb=_rgb_tuple(entry.get("hint")),
                dye_override=override,
            )

    return LookPreset(
        schema_version=int(data["v"]),
        server=ServerSelection(
            server_id=str(server_raw.get("server_id", "mabikr1")),
            region=str(server_raw.get("region", "kr")),
        ),
        base=BaseCharacter(
            race=str(base_raw.get("race", "human")),
            gender=str(base_raw.get("gender", "female")),
            age=int(base_raw.get("age", 20)),
        ),
        equipped=equipped,
    )
