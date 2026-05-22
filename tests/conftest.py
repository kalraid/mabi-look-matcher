"""Pytest — force mock providers; no live Gemini/Redis/Sigkill."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from look_matcher.config.providers_registry import AdapterId, resolve_providers
from look_matcher.config.settings import get_settings, reset_settings


@pytest.fixture(autouse=True)
def _mock_mode_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOOK_MATCHER_PROVIDERS__MODE", "mock")
    reset_settings()


@pytest.fixture
def settings():
    return get_settings()


@pytest.fixture
def resolved(settings):
    return resolve_providers(settings)


@pytest.fixture
def repo_root(settings):
    return settings.repo_root


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(
                pytest.mark.skipif(
                    os.getenv("LOOK_MATCHER_RUN_INTEGRATION") != "1",
                    reason="Set LOOK_MATCHER_RUN_INTEGRATION=1 for live external calls",
                )
            )


@pytest.fixture
def adapter_ids(resolved) -> set[AdapterId]:
    ids = {
        resolved.vision,
        resolved.catalog_store,
        resolved.ephemeral,
        resolved.redis,
        resolved.analysis_queue,
    }
    ids.update(resolved.catalog_sources)
    if resolved.embedding_rank:
        ids.add(resolved.embedding_rank)
    return ids
