"""Embedding Rank — reorder without external API."""

from look_matcher.candidate_builder import CandidateListResult
from look_matcher.catalog_store.store import CatalogEntry
from look_matcher.embedding_rank import ReverseOrderRanker


def test_reverse_ranker_changes_order() -> None:
    a = CatalogEntry(id="a", display_name_ko="A", slot_ids=["body"], dyeable=False, server_ids=["mabikr1"])
    b = CatalogEntry(id="b", display_name_ko="B", slot_ids=["body"], dyeable=False, server_ids=["mabikr1"])
    original = CandidateListResult(by_slot={"body": [a, b]}, unrecognized_slots=[])

    ranked = ReverseOrderRanker().rerank(b"img", original)

    assert [e.id for e in ranked.by_slot["body"]] == ["b", "a"]
