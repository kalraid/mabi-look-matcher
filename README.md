# Mabi Look Matcher

레퍼런스 사진을 업로드하면 슬롯별로 비슷한 마비노기 장비 후보를 보여 주고, 클릭·드래그로 착용해 2D/3D 미리보기를 확인하는 웹 앱입니다.

- 도메인 용어·결정: [`CONTEXT.md`](CONTEXT.md), [`docs/adr/`](docs/adr/)
- PRD: [`docs/PRD-look-matcher.md`](docs/PRD-look-matcher.md)
- 이슈 백로그: [`docs/issues/`](docs/issues/)

## 요구 사항

- Python 3.11+
- Node.js 18+ (웹 UI)

## 빠른 시작 (mock 모드, 기본)

```bash
# 루트에서 Python 패키지 + API
pip install -e ".[api,dev]"
copy .env.example .env   # Windows: LOOK_MATCHER_PROVIDERS__MODE=mock 유지

# 카탈로그 스냅샷 (이미 data/catalog.snapshot.json 있으면 생략 가능)
look-matcher-catalog-merge --out data/catalog.snapshot.json

# API (포트 8000)
uvicorn apps.api.main:app --reload --port 8000
```

다른 터미널에서 웹:

```bash
cd apps/web
copy .env.example .env.local
npm install
npm run dev
```

브라우저: http://localhost:3000 — `NEXT_PUBLIC_API_BASE_URL`은 기본 `http://127.0.0.1:8000` 입니다.

## 테스트

```bash
pytest tests/ -q
```

## 구현 상태 (MVP)

| 영역 | 경로 |
|------|------|
| Analysis API | `packages/look_matcher/api/`, `apps/api/main.py` |
| Mock Vision / Orchestrator | `packages/look_matcher/analysis/`, `vision/` |
| Catalog 검색·후보 | `catalog_store/`, `candidate_builder/` |
| Flat Preview | `packages/look_matcher/flat_preview/` |
| Embedding Rank (stub) | `packages/look_matcher/embedding_rank/` |
| Custom Shell UI | `apps/web/` |

`LOOK_MATCHER_PROVIDERS__MODE=mock` 일 때 Gemini·CLIP·Redis 없이 동작합니다. Embedding Rank는 `config/default.yaml`의 `embedding_rank.enabled`로 켭니다.

## 라이선스

프로젝트 정책에 따릅니다.
