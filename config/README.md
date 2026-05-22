# Look Matcher 설정

## 파일

| 파일 | 역할 |
|------|------|
| `default.yaml` | 기본값·슬롯 우선순위·한도 |
| `mocks.yaml` | `providers.mode=mock` 일 때 오버레이 |
| `catalog.merge.yaml` | **Catalog Merge** 필드 우선순위 |

## Mock vs Live

```bash
# TDD / 로컬 (기본)
LOOK_MATCHER_PROVIDERS__MODE=mock

# 실제 Gemini·Redis·SQLite
LOOK_MATCHER_PROVIDERS__MODE=live
GEMINI_API_KEY=...
REDIS_URL=redis://127.0.0.1:6379/0
```

`packages/look_matcher/config/providers_registry.py`의 `ResolvedProviders`가 활성 **AdapterId**를 결정한다. 구현체(HTTP 클라이언트 등)는 TDD 사이클에서 추가한다.

## 외부 연동 매핑

| ADR 용어 | mock | live |
|----------|------|------|
| Vision Provider | `vision.mock` + fixture JSON | `vision.gemini` |
| Item Catalog | `catalog.mock` + fixture JSON | `catalog.sqlite` |
| Ephemeral Upload | `ephemeral.memory` | `ephemeral.filesystem` |
| Analysis Queue | `queue.inline_mock` | `queue.redis` |
| Catalog Source | `source.*.mock` fixtures | 크롤/수집 CLI (미구현) |
| Embedding Rank | off / passthrough | `local_clip` (phase 2) |

## Python

```python
from look_matcher.config import get_settings
from look_matcher.config.providers_registry import resolve_providers

settings = get_settings()
adapters = resolve_providers(settings)
```

## Phase 0 CLI

```bash
pip install -e .
look-matcher-catalog-merge --out data/catalog.snapshot.json
```

기본 입력은 `tests/fixtures/sources/*` (mock). live 수집 파일 경로는 `--labanyu`, `--sigkill`, `--dump`로 지정.

## 테스트

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

`tests/conftest.py`가 모든 테스트에 `LOOK_MATCHER_PROVIDERS__MODE=mock`을 강제한다.
