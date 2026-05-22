"""Analysis API — mock run end-to-end."""

from io import BytesIO

from fastapi.testclient import TestClient

from look_matcher.api.app import app
from look_matcher.analysis import EphemeralBlobStore
from look_matcher.analysis.orchestrator import AnalysisOrchestrator
from look_matcher.catalog_store import CatalogStore
from look_matcher.config import get_settings
from look_matcher.vision import MockVisionProvider


def test_ephemeral_deleted_after_run_completes(repo_root) -> None:
    settings = get_settings()
    ephemeral = EphemeralBlobStore()
    orch = AnalysisOrchestrator(
        ephemeral=ephemeral,
        vision=MockVisionProvider(
            repo_root / "tests/fixtures/match_hints/default.json"
        ),
        catalog=CatalogStore.from_snapshot_file(
            repo_root / "tests/fixtures/catalog/minimal.json"
        ),
        slot_ids=["body", "wings", "weapon1"],
        limit_per_slot=10,
    )

    run_id = orch.start_run(
        image_bytes=b"fake-image",
        content_type="image/jpeg",
        server_id="mabikr1",
        base_meta={"race": "human", "gender": "female", "age": 20},
    )

    assert orch.get_run(run_id).status == "completed"
    assert not ephemeral.has(run_id)


def test_api_post_and_get_run(repo_root) -> None:
    client = TestClient(app)
    png = BytesIO(b"\x89PNG\r\n\x1a\n")
    png.name = "ref.png"

    res = client.post(
        "/api/analysis/run",
        files={"image": ("ref.png", png, "image/png")},
        data={
            "server_id": "mabikr1",
            "base_meta": '{"race":"human","gender":"female","age":20}',
        },
    )
    assert res.status_code == 200
    run_id = res.json()["run_id"]

    poll = client.get(f"/api/analysis/run/{run_id}")
    assert poll.status_code == 200
    body = poll.json()
    assert body["status"] == "completed"
    wings = next(s for s in body["slots"] if s["slot_id"] == "wings")
    assert len(wings["candidates"]) >= 1
