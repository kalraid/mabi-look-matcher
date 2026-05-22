from __future__ import annotations

import json
from pathlib import Path

from look_matcher.candidate_builder.builder import MatchHintsBySlot, SlotMatchHint


class MockVisionProvider:
    """Vision Provider: loads Match Hint JSON fixture (no API call)."""

    def __init__(self, fixture_path: Path) -> None:
        self._path = fixture_path

    def generate_hints(self, image_bytes: bytes, *, base_meta: dict) -> MatchHintsBySlot:
        with self._path.open(encoding="utf-8") as f:
            data = json.load(f)
        slots = []
        for row in data.get("slots", []):
            slots.append(
                SlotMatchHint(
                    slot_id=str(row.get("slotId", row.get("slot_id", ""))),
                    confidence=str(row.get("confidence", "none")),
                    search_queries=list(row.get("searchQueries", row.get("search_queries", []))),
                )
            )
        return MatchHintsBySlot(slots=slots)
