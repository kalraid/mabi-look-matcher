from __future__ import annotations

import json
from functools import lru_cache

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from look_matcher.analysis import AnalysisOrchestrator, EphemeralBlobStore
from look_matcher.catalog_store import get_catalog_store
from look_matcher.config import get_settings
from look_matcher.embedding_rank import PassthroughRanker, ReverseOrderRanker
from look_matcher.vision import MockVisionProvider

app = FastAPI(title="Look Matcher API", version="0.1.0")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.get("allowed_origins", ["http://localhost:3000"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def _orchestrator() -> AnalysisOrchestrator:
    s = get_settings()
    vision_path = s.vision_fixture_path() or s.resolve_path(
        "tests/fixtures/match_hints/default.json"
    )
    ranker = None
    if s.embedding_rank.enabled:
        ranker = (
            ReverseOrderRanker()
            if s.embedding_rank.provider == "mock"
            and not s.embedding_rank.mock.get("passthrough", True)
            else PassthroughRanker()
        )
    return AnalysisOrchestrator(
        ephemeral=EphemeralBlobStore(ttl_seconds=s.ephemeral_upload.ttl_seconds),
        vision=MockVisionProvider(vision_path),
        catalog=get_catalog_store(),
        slot_ids=s.slot_coverage.priority_slot_ids
        or ["body", "wings", "head", "gloves", "shoes"],
        limit_per_slot=s.analysis.candidate_limit_per_slot,
        embedding_ranker=ranker,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analysis/run")
async def start_analysis(
    image: UploadFile = File(...),
    server_id: str = Form(default="mabikr1"),
    base_meta: str = Form(default="{}"),
) -> dict[str, str]:
    s = get_settings()
    data = await image.read()
    if len(data) > s.ephemeral_upload.max_bytes:
        raise HTTPException(status_code=413, detail="image too large")

    try:
        meta = json.loads(base_meta)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="invalid base_meta json") from exc

    run_id = _orchestrator().start_run(
        image_bytes=data,
        content_type=image.content_type or "image/jpeg",
        server_id=server_id,
        base_meta=meta,
    )
    return {"run_id": run_id}


@app.get("/api/analysis/run/{run_id}")
def get_analysis(run_id: str) -> dict:
    state = _orchestrator().get_run(run_id)
    if state is None:
        raise HTTPException(status_code=404, detail="run not found")

    return {
        "run_id": state.run_id,
        "status": state.status,
        "server_id": state.server_id,
        "unrecognized_slots": state.unrecognized_slots,
        "slots": [
            {
                "slot_id": s.slot_id,
                "status": s.status,
                "candidates": s.candidates,
                "message": s.message,
            }
            for s in state.slots
            if s.status != "pending" or s.candidates
        ],
    }
