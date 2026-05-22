"""Provider registry — maps config to mock/live adapter ids (implementations TDD later)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from look_matcher.config.settings import AppSettings, ProviderMode, StorageBackend, VisionProviderKind


class AdapterId(str, Enum):
    VISION_MOCK = "vision.mock"
    VISION_GEMINI = "vision.gemini"
    CATALOG_MOCK = "catalog.mock"
    CATALOG_SQLITE = "catalog.sqlite"
    EPHEMERAL_MEMORY = "ephemeral.memory"
    EPHEMERAL_FILESYSTEM = "ephemeral.filesystem"
    REDIS_MOCK = "redis.mock"
    REDIS_TCP = "redis.tcp"
    QUEUE_INLINE_MOCK = "queue.inline_mock"
    QUEUE_REDIS = "queue.redis"
    EMBEDDING_PASSTHROUGH = "embedding.passthrough"
    EMBEDDING_LOCAL_CLIP = "embedding.local_clip"
    SOURCE_LABANYU_MOCK = "source.labanyu.mock"
    SOURCE_SIGKILL_MOCK = "source.sigkill.mock"
    SOURCE_DUMP_MOCK = "source.community_dump.mock"


@dataclass(frozen=True)
class ResolvedProviders:
    """Active adapter ids for dependency injection (factory stubs in TDD cycles)."""

    vision: AdapterId
    catalog_store: AdapterId
    ephemeral: AdapterId
    redis: AdapterId
    analysis_queue: AdapterId
    embedding_rank: AdapterId | None
    catalog_sources: tuple[AdapterId, ...]


def resolve_providers(settings: AppSettings) -> ResolvedProviders:
    mock = settings.is_mock_mode

    vision = (
        AdapterId.VISION_MOCK
        if settings.vision_provider.provider == VisionProviderKind.MOCK or mock
        else AdapterId.VISION_GEMINI
    )

    catalog = (
        AdapterId.CATALOG_MOCK
        if settings.catalog.provider == "mock" or mock
        else AdapterId.CATALOG_SQLITE
    )

    ephemeral = (
        AdapterId.EPHEMERAL_MEMORY
        if settings.ephemeral_upload.storage_backend == StorageBackend.MEMORY or mock
        else AdapterId.EPHEMERAL_FILESYSTEM
    )

    redis = (
        AdapterId.REDIS_MOCK
        if settings.redis.provider == "mock" or mock
        else AdapterId.REDIS_TCP
    )

    queue = AdapterId.QUEUE_INLINE_MOCK if mock else AdapterId.QUEUE_REDIS

    embedding: AdapterId | None = None
    if settings.embedding_rank.enabled:
        embedding = (
            AdapterId.EMBEDDING_PASSTHROUGH
            if settings.embedding_rank.provider == "mock"
            else AdapterId.EMBEDDING_LOCAL_CLIP
        )

    sources: list[AdapterId] = []
    if mock:
        sources = [
            AdapterId.SOURCE_LABANYU_MOCK,
            AdapterId.SOURCE_SIGKILL_MOCK,
            AdapterId.SOURCE_DUMP_MOCK,
        ]

    return ResolvedProviders(
        vision=vision,
        catalog_store=catalog,
        ephemeral=ephemeral,
        redis=redis,
        analysis_queue=queue,
        embedding_rank=embedding,
        catalog_sources=tuple(sources),
    )


def assert_mock_only_for_tests(settings: AppSettings) -> None:
    """Guard: integration tests must opt in to live providers."""
    if settings.providers.mode != ProviderMode.MOCK:
        raise RuntimeError(
            "Tests require LOOK_MATCHER_PROVIDERS__MODE=mock unless @pytest.mark.integration"
        )
