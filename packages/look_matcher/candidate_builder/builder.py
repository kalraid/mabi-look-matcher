from __future__ import annotations

from dataclasses import dataclass, field

from look_matcher.catalog_store.store import CatalogEntry, CatalogStore


@dataclass(frozen=True)
class SlotMatchHint:
    slot_id: str
    confidence: str
    search_queries: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class MatchHintsBySlot:
    slots: list[SlotMatchHint]


@dataclass(frozen=True)
class CandidateListResult:
    by_slot: dict[str, list[CatalogEntry]]
    unrecognized_slots: list[str]


class CandidateBuilder:
    """Match Hint + CatalogStore → Candidate List per slot."""

    def __init__(self, *, catalog: CatalogStore, limit_per_slot: int = 10) -> None:
        self._catalog = catalog
        self._limit = limit_per_slot

    def build(self, hints: MatchHintsBySlot, *, server_id: str) -> CandidateListResult:
        by_slot: dict[str, list[CatalogEntry]] = {}
        unrecognized: list[str] = []

        for hint in hints.slots:
            if hint.confidence == "none" or not hint.search_queries:
                by_slot[hint.slot_id] = []
                if hint.confidence == "none":
                    unrecognized.append(hint.slot_id)
                continue

            seen: set[str] = set()
            collected: list[CatalogEntry] = []

            for query in hint.search_queries:
                for entry in self._catalog.search(
                    slot_id=hint.slot_id,
                    server_id=server_id,
                    query=query,
                    limit=self._limit,
                ):
                    if entry.id in seen:
                        continue
                    seen.add(entry.id)
                    collected.append(entry)
                    if len(collected) >= self._limit:
                        break
                if len(collected) >= self._limit:
                    break

            by_slot[hint.slot_id] = collected

        return CandidateListResult(by_slot=by_slot, unrecognized_slots=unrecognized)
