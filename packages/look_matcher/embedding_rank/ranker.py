from __future__ import annotations

from typing import Protocol

from look_matcher.candidate_builder.builder import CandidateListResult
from look_matcher.catalog_store.store import CatalogEntry


class EmbeddingRanker(Protocol):
    def rerank(
        self, reference_image: bytes, candidates: CandidateListResult
    ) -> CandidateListResult: ...


class PassthroughRanker:
    """MVP default — no reorder."""

    def rerank(
        self, reference_image: bytes, candidates: CandidateListResult
    ) -> CandidateListResult:
        return candidates


class ReverseOrderRanker:
    """Test double: reverses each slot list to prove ranker runs without Gemini."""

    def rerank(
        self, reference_image: bytes, candidates: CandidateListResult
    ) -> CandidateListResult:
        by_slot = {
            slot: list(reversed(entries))
            for slot, entries in candidates.by_slot.items()
        }
        return CandidateListResult(
            by_slot=by_slot,
            unrecognized_slots=candidates.unrecognized_slots,
        )
