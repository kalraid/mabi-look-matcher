from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Literal

from look_matcher.candidate_builder import CandidateBuilder
from look_matcher.catalog_store.store import CatalogEntry, CatalogStore
from look_matcher.analysis.ephemeral import EphemeralBlobStore
from look_matcher.embedding_rank import EmbeddingRanker
from look_matcher.vision.mock import MockVisionProvider

SlotStatusName = Literal["pending", "running", "done", "failed"]


@dataclass
class SlotStatus:
    slot_id: str
    status: SlotStatusName
    candidates: list[dict[str, Any]] = field(default_factory=list)
    message: str | None = None


@dataclass
class RunState:
    run_id: str
    server_id: str
    base_meta: dict[str, Any]
    status: Literal["running", "completed", "failed"]
    slots: list[SlotStatus]
    unrecognized_slots: list[str] = field(default_factory=list)


class AnalysisOrchestrator:
    def __init__(
        self,
        *,
        ephemeral: EphemeralBlobStore,
        vision: MockVisionProvider,
        catalog: CatalogStore,
        slot_ids: list[str],
        limit_per_slot: int = 10,
        embedding_ranker: EmbeddingRanker | None = None,
    ) -> None:
        self._ephemeral = ephemeral
        self._vision = vision
        self._catalog = catalog
        self._slot_ids = slot_ids
        self._limit = limit_per_slot
        self._embedding = embedding_ranker
        self._runs: dict[str, RunState] = {}

    def start_run(
        self,
        *,
        image_bytes: bytes,
        content_type: str,
        server_id: str,
        base_meta: dict[str, Any],
    ) -> str:
        run_id = str(uuid.uuid4())
        self._ephemeral.put(run_id, image_bytes, content_type=content_type)

        slots = [SlotStatus(slot_id=s, status="pending") for s in self._slot_ids]
        self._runs[run_id] = RunState(
            run_id=run_id,
            server_id=server_id,
            base_meta=base_meta,
            status="running",
            slots=slots,
        )

        self._process_run(run_id)
        return run_id

    def get_run(self, run_id: str) -> RunState | None:
        return self._runs.get(run_id)

    def _process_run(self, run_id: str) -> None:
        state = self._runs[run_id]
        image = self._ephemeral.get(run_id)
        if image is None:
            state.status = "failed"
            return

        try:
            hints = self._vision.generate_hints(image, base_meta=state.base_meta)
            builder = CandidateBuilder(catalog=self._catalog, limit_per_slot=self._limit)
            result = builder.build(hints, server_id=state.server_id)

            if self._embedding is not None:
                result = self._embedding.rerank(image, result)

            hint_slots = {h.slot_id for h in hints.slots}
            for slot in state.slots:
                if slot.slot_id not in hint_slots:
                    slot.status = "done"
                    slot.candidates = []
                    continue
                slot.status = "running"
                entries = result.by_slot.get(slot.slot_id, [])
                slot.candidates = [_entry_to_dict(e) for e in entries]
                slot.status = "done"

            state.unrecognized_slots = result.unrecognized_slots
            state.status = "completed"
        except Exception as exc:  # noqa: BLE001
            state.status = "failed"
            for slot in state.slots:
                if slot.status != "done":
                    slot.status = "failed"
                    slot.message = str(exc)
        finally:
            self._ephemeral.delete(run_id)


def _entry_to_dict(entry: CatalogEntry) -> dict[str, Any]:
    return {
        "id": entry.id,
        "display_name_ko": entry.display_name_ko,
        "dyeable": entry.dyeable,
        "thumbnail_url": entry.thumbnail_url,
        "slot_ids": entry.slot_ids,
    }
