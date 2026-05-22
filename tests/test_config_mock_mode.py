"""Tracer: config loads in mock mode and resolves mock adapters only."""

from look_matcher.config.providers_registry import AdapterId, assert_mock_only_for_tests
from look_matcher.config.settings import ProviderMode, VisionProviderKind


def test_settings_load_in_mock_mode(settings) -> None:
    assert settings.is_mock_mode
    assert settings.providers.mode == ProviderMode.MOCK
    assert settings.vision_provider.provider == VisionProviderKind.MOCK


def test_resolved_providers_use_mocks(resolved) -> None:
    assert resolved.vision == AdapterId.VISION_MOCK
    assert resolved.catalog_store == AdapterId.CATALOG_MOCK
    assert resolved.ephemeral == AdapterId.EPHEMERAL_MEMORY
    assert resolved.redis == AdapterId.REDIS_MOCK
    assert resolved.analysis_queue == AdapterId.QUEUE_INLINE_MOCK
    assert resolved.embedding_rank is None


def test_mock_fixture_paths_exist(settings) -> None:
    assert settings.vision_fixture_path() is not None
    assert settings.vision_fixture_path().is_file()
    assert settings.catalog_fixture_path() is not None
    assert settings.catalog_fixture_path().is_file()


def test_assert_mock_guard(settings) -> None:
    assert_mock_only_for_tests(settings)
