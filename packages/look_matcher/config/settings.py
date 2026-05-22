"""Configuration loader — YAML + env. No external API calls."""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).resolve().parents[3]
_CONFIG_DIR = _REPO_ROOT / "config"


class ProviderMode(str, Enum):
    MOCK = "mock"
    LIVE = "live"


class VisionProviderKind(str, Enum):
    MOCK = "mock"
    GEMINI = "gemini"


class StorageBackend(str, Enum):
    MEMORY = "memory"
    FILESYSTEM = "filesystem"


class MockVisionConfig(BaseModel):
    fixture_path: str = "tests/fixtures/match_hints/default.json"
    latency_ms: int = 0
    fail_rate: float = 0.0


class GeminiVisionConfig(BaseModel):
    api_key_env: str = "GEMINI_API_KEY"
    base_url: str = "https://generativelanguage.googleapis.com"
    model: str = "gemini-2.0-flash"
    timeout_seconds: int = 60
    max_output_tokens: int = 8192


class VisionProviderConfig(BaseModel):
    provider: VisionProviderKind = VisionProviderKind.MOCK
    mock: MockVisionConfig = Field(default_factory=MockVisionConfig)
    gemini: GeminiVisionConfig = Field(default_factory=GeminiVisionConfig)


class MockCatalogStoreConfig(BaseModel):
    fixture_path: str = "tests/fixtures/catalog/minimal.json"
    latency_ms: int = 0


class CatalogConfig(BaseModel):
    snapshot_path: str = "data/catalog.snapshot.json"
    sqlite_path: str = "data/catalog.sqlite"
    search_max_results: int = 15
    provider: Literal["mock", "sqlite"] = "mock"
    mock: MockCatalogStoreConfig = Field(default_factory=MockCatalogStoreConfig)


class CatalogMergeConfig(BaseModel):
    config_path: str = "config/catalog.merge.yaml"
    review_queue_path: str = "data/merge_review.jsonl"


class EphemeralUploadConfig(BaseModel):
    max_bytes: int = 10_485_760
    allowed_content_types: list[str] = Field(
        default_factory=lambda: ["image/jpeg", "image/png", "image/webp"]
    )
    ttl_seconds: int = 3600
    storage_backend: StorageBackend = StorageBackend.MEMORY
    filesystem_path: str = "data/ephemeral"


class RedisConfig(BaseModel):
    url_env: str = "REDIS_URL"
    url_default: str = "redis://127.0.0.1:6379/0"
    analysis_queue_key_prefix: str = "lm:analysis:"
    provider: Literal["mock", "redis"] = "mock"
    mock: dict[str, Any] = Field(default_factory=dict)


class AnalysisConfig(BaseModel):
    candidate_limit_per_slot: int = 10
    match_hint_model: str = "gemini-2.0-flash"
    queue_poll_interval_ms: int = 800
    slot_job_timeout_seconds: int = 120
    run_timeout_seconds: int = 600


class ServerSelectionConfig(BaseModel):
    default_server_id: str = "mabikr1"
    default_server_label: str = "류트"
    default_region: str = "kr"
    supported_regions: list[str] = Field(default_factory=lambda: ["kr"])


class SlotCoverageConfig(BaseModel):
    source: str = "sigkill"
    priority_slot_ids: list[str] = Field(default_factory=list)


class EmbeddingRankConfig(BaseModel):
    enabled: bool = False
    provider: Literal["mock", "local_clip"] = "mock"
    mock: dict[str, Any] = Field(default_factory=lambda: {"passthrough": True})


class ProvidersConfig(BaseModel):
    mode: ProviderMode = ProviderMode.MOCK


class AppSettings(BaseSettings):
    """Root settings — load via get_settings()."""

    model_config = SettingsConfigDict(
        env_prefix="LOOK_MATCHER_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app_name: str = "look-matcher"
    app_env: str = Field(default="development", alias="env")
    log_level: str = "INFO"

    providers: ProvidersConfig = Field(default_factory=ProvidersConfig)
    server_selection: ServerSelectionConfig = Field(default_factory=ServerSelectionConfig)
    base_character: dict[str, Any] = Field(
        default_factory=lambda: {
            "default_race": "human",
            "default_gender": "female",
            "default_age": 20,
        }
    )
    slot_coverage: SlotCoverageConfig = Field(default_factory=SlotCoverageConfig)
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    catalog: CatalogConfig = Field(default_factory=CatalogConfig)
    catalog_merge: CatalogMergeConfig = Field(default_factory=CatalogMergeConfig)
    ephemeral_upload: EphemeralUploadConfig = Field(default_factory=EphemeralUploadConfig)
    vision_provider: VisionProviderConfig = Field(default_factory=VisionProviderConfig)
    embedding_rank: EmbeddingRankConfig = Field(default_factory=EmbeddingRankConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    rate_limit: dict[str, int] = Field(
        default_factory=lambda: {
            "gemini_requests_per_minute": 15,
            "analysis_runs_per_hour_per_ip": 10,
        }
    )
    look_preset: dict[str, Any] = Field(
        default_factory=lambda: {
            "schema_version": 1,
            "share_param": "preset",
            "max_encoded_length": 8000,
        }
    )
    flat_preview: dict[str, Any] = Field(default_factory=dict)
    depth_preview: dict[str, Any] = Field(default_factory=dict)
    cors: dict[str, list[str]] = Field(
        default_factory=lambda: {"allowed_origins": ["http://localhost:3000"]}
    )
    catalog_sources: dict[str, Any] = Field(default_factory=dict)
    analysis_orchestrator: dict[str, Any] = Field(default_factory=dict)

    @property
    def repo_root(self) -> Path:
        return _REPO_ROOT

    @property
    def is_mock_mode(self) -> bool:
        return self.providers.mode == ProviderMode.MOCK

    def resolve_path(self, relative: str) -> Path:
        return (_REPO_ROOT / relative).resolve()

    def vision_fixture_path(self) -> Path | None:
        if self.vision_provider.provider != VisionProviderKind.MOCK:
            return None
        return self.resolve_path(self.vision_provider.mock.fixture_path)

    def catalog_fixture_path(self) -> Path | None:
        if self.catalog.provider != "mock":
            return None
        return self.resolve_path(self.catalog.mock.fixture_path)


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in overlay.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def load_settings_from_files(
    *,
    config_dir: Path | None = None,
    use_mocks: bool | None = None,
) -> AppSettings:
    """Load default.yaml; overlay mocks.yaml when mock mode."""
    config_dir = config_dir or _CONFIG_DIR
    raw = _load_yaml(config_dir / "default.yaml")

    mode = raw.get("providers", {}).get("mode", "mock")
    if use_mocks is True:
        mode = "mock"
    elif use_mocks is False:
        mode = "live"

    if mode == "mock":
        raw = _deep_merge(raw, _load_yaml(config_dir / "mocks.yaml"))
        raw.setdefault("providers", {})["mode"] = "mock"

    app_block = raw.pop("app", {})
    flat: dict[str, Any] = {
        "env": app_block.get("env", "development"),
        "log_level": app_block.get("log_level", "INFO"),
        **{k: v for k, v in raw.items()},
    }
    if app_block.get("name"):
        flat["app_name"] = app_block["name"]

    return AppSettings.model_validate(flat)


def _env_use_mocks() -> bool | None:
    import os

    mode = os.getenv("LOOK_MATCHER_PROVIDERS__MODE")
    if mode == "live":
        return False
    if mode == "mock":
        return True
    return None


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return load_settings_from_files(use_mocks=_env_use_mocks())


def reset_settings() -> None:
    """Clear cached settings (tests)."""
    get_settings.cache_clear()
