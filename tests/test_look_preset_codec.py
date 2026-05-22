"""LookPresetCodec — Share Link round-trip (public interface)."""

import pytest

from look_matcher.look_preset import (
    BaseCharacter,
    DyeOverride,
    EquippedItem,
    LookPreset,
    LookPresetCodec,
    PresetDecodeError,
    ServerSelection,
)


def test_encode_decode_round_trip_preserves_loadout() -> None:
    preset = LookPreset(
        schema_version=1,
        server=ServerSelection(server_id="mabikr1", region="kr"),
        base=BaseCharacter(race="human", gender="female", age=20),
        equipped={
            "body": EquippedItem(item_id="item-001", dye_hint_rgb=(120, 40, 180)),
            "wings": EquippedItem(
                item_id="item-002",
                dye_hint_rgb=(80, 20, 120),
                dye_override=DyeOverride(rgb=(90, 30, 130)),
            ),
        },
    )

    codec = LookPresetCodec()
    token = codec.encode(preset)
    restored = codec.decode(token)

    assert restored.schema_version == 1
    assert restored.server.server_id == "mabikr1"
    assert restored.base.age == 20
    assert restored.equipped["body"].item_id == "item-001"
    assert restored.equipped["wings"].dye_override is not None
    assert restored.equipped["wings"].dye_override.rgb == (90, 30, 130)


def test_decode_unknown_schema_version_fails_clearly() -> None:
    codec = LookPresetCodec()
    import base64
    import json
    import zlib

    payload = {
        "v": 99,
        "server": {"server_id": "mabikr1", "region": "kr"},
        "base": {"race": "human", "gender": "female", "age": 20},
        "equipped": {},
    }
    raw = base64.urlsafe_b64encode(
        zlib.compress(json.dumps(payload).encode("utf-8"), level=9)
    ).decode("ascii")

    with pytest.raises(PresetDecodeError, match="unsupported schema"):
        codec.decode(raw)


def test_decode_invalid_token_raises() -> None:
    codec = LookPresetCodec()
    with pytest.raises(PresetDecodeError):
        codec.decode("not-valid-preset!!!")
