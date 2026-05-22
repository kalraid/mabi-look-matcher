"""CandidateBuilder — Match Hint to Candidate List."""

from pathlib import Path

from look_matcher.candidate_builder import CandidateBuilder, MatchHintsBySlot, SlotMatchHint
from look_matcher.catalog_store import CatalogStore


def _store(repo_root: Path) -> CatalogStore:
    return CatalogStore.from_snapshot_file(
        repo_root / "tests/fixtures/catalog/minimal.json"
    )


def test_build_returns_candidates_for_high_confidence_slot(repo_root: Path) -> None:
    hints = MatchHintsBySlot(
        slots=[
            SlotMatchHint(
                slot_id="wings",
                confidence="high",
                search_queries=["데빌", "박쥐 날개"],
            )
        ]
    )
    builder = CandidateBuilder(catalog=_store(repo_root), limit_per_slot=10)

    result = builder.build(hints, server_id="mabikr1")

    assert "wings" in result.by_slot
    assert len(result.by_slot["wings"]) >= 1
    assert result.by_slot["wings"][0].display_name_ko


def test_build_empty_list_when_confidence_none() -> None:
    hints = MatchHintsBySlot(
        slots=[
            SlotMatchHint(
                slot_id="weapon1",
                confidence="none",
                search_queries=[],
            )
        ]
    )
    builder = CandidateBuilder(catalog=CatalogStore([]), limit_per_slot=10)

    result = builder.build(hints, server_id="mabikr1")

    assert result.by_slot["weapon1"] == []
    assert result.unrecognized_slots == ["weapon1"]
