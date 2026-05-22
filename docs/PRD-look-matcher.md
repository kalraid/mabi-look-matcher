# PRD: Mabi Look Matcher

**Status:** ready-for-agent  
**Labels:** `ready-for-agent`  
**Domain glossary:** `CONTEXT.md`  
**ADRs:** `docs/adr/0001`–`0013`

---

## Problem Statement

마비노기 유저는 참고 사진(일러스트, 타 게임/캐릭터 스샷, 코스프레 레퍼런스 등)에 맞는 인게임 코디를 맞추고 싶지만, 수천 개의 의상·액세서리·날개·가발을 일일이 검색하고 시뮬레이터에서 입혀 보는 과정이 오래 걸린다. 기존 Sigkill 캐릭터 시뮬레이터는 착용·염색에는 강하지만, **레퍼런스 이미지에서 슬롯별로 비슷한 아이템 후보를 자동으로 제안**하는 흐름은 없다. 경매장 시세까지는 필요 없고, **사진 → 후보 목록 → 골라 입혀 보기**가 핵심이다.

---

## Solution

**Look Matcher** 웹 앱: 사용자가 **Reference Image**를 올리고 **Server Selection**·**Base Character**(종족·성별·나이)를 고른 뒤 **Analysis Run**을 시작하면, Sigkill **Slot Coverage** 전체에 대해 슬롯당 약 10개의 **Candidate List**가 우측에 채워진다. **Click Equip**으로 **Flat Preview**에 반영하고, **Dye Hint** 자동 RGB는 **Dye Override**로 수정한다. **Look Preset**은 localStorage와 **Share Link**로 저장한다. 3D는 **Depth Preview**(Sigkill iframe, 베타)로 선택 확인한다.

---

## User Stories

1. As a 코디를 맞추는 유저, I want a **Reference Image**를 업로드할 수 있게, so that 레퍼런스 외형을 기준으로 삼을 수 있다.
2. As a 유저, I want 업로드한 사진이 서버에 영구 저장되지 않게, so that 개인 사진이 유출·보관되지 않는다.
3. As a 유저, I want **Server Selection**(기본 한국/류트)을 고를 수 있게, so that 내 서버에 있는 아이템만 후보에 나온다.
4. As a 유저, I want **Base Character**의 종족·성별·나이를 설정할 수 있게, so that 착용 불가 아이템을 줄일 수 있다.
5. As a 유저, I want 베이스 설정 후 기본 외형이 **Flat Preview**에 보이게, so that 코디 맥락을 바로 볼 수 있다.
6. As a 유저, I want **Analysis Run** 버튼으로 분석을 시작할 수 있게, so that 업로드만으로 API가 자동 소모되지 않는다.
7. As a 유저, I want 분석 중 슬롯별 진행 상태(대기·처리 중·완료)를 보게, so that **Analysis Queue** 진행을 알 수 있다.
8. As a 유저, I want 분석이 끝나면 슬롯마다 **Candidate List**(~10개)가 우측에 나타나게, so that 일일이 검색하지 않아도 된다.
9. As a 유저, I want 사진에 잘 안 보이는 슬롯(무기 등)에 “식별 안 됨” 또는 낮은 신뢰도 표시를 보게, so that 빈 목록이 오류가 아님을 알 수 있다.
10. As a 유저, I want **Candidate List** 항목을 클릭해 **Click Equip**할 수 있게, so that 해당 **Equipment Slot**에 바로 반영된다.
11. As a 유저, I want 착용 시 **Dye Hint** 색이 기본 적용되게, so that 레퍼런스 색에 가깝게 볼 수 있다.
12. As a 유저, I want **Dye Override**로 RGB/팔레트를 수동 수정할 수 있게, so that 자동 색이 틀릴 때 고칠 수 있다.
13. As a 유저, I want **Flat Preview**가 착용·염색 변경에 즉시 반응하게, so that 조합 결과를 빠르게 비교할 수 있다.
14. As a 유저, I want Sigkill과 동일한 **Slot Coverage** 전 슬롯 탭/섹션을 보게, so that 무기·펫 장비까지 한 화면에서 맞출 수 있다.
15. As a 유저, I want 후보 목록에 아이템명·썸네일(있을 때)·염색 가능 여부를 보게, so that 고르기 쉽다.
16. As a 유저, I want 현재 착용 중인 아이템이 슬롯 UI에서 강조되게, so that 상태를 헷갈리지 않는다.
17. As a 유저, I want **Look Preset**이 브라우저에 자동 저장되게, so that 새로고침 후에도 코디가 남는다.
18. As a 유저, I want **Share Link**를 복사해 친구에게 보낼 수 있게, so that 코디 설정만 공유할 수 있다(사진 제외).
19. As a 유저, I want **Share Link**로 열면 동일 **Look Preset**이 복원되게, so that 링크만으로 코디를 재현할 수 있다.
20. As a 유저, I want **Depth Preview**로 3D 확인(베타)을 열 수 있게, so that 게임에 가까운 착용감을 볼 수 있다.
21. As a 유저, I want Gemini 무료 한도 초과 시 안내 메시지를 보게, so that 분석 실패 이유를 알 수 있다.
22. As a 유저, I want 분석을 다시 실행할 수 있게, so that 다른 사진·설정으로 후보를 갱신할 수 있다.
23. As a 유저, I want 후보가 내 **Server Selection**에 없는 아이템이면 목록에 안 나오거나 비활성 표시되게, so that 살 수 없는/못 입는 추천을 받지 않는다.
24. As a 유저, I want 의상·날개·가발 등 코디 핵심 슬롯 후보가 먼저 준비되는 느낌을 받게, so that Queue가 길어도 기다릴 가치가 있다(슬롯 우선순위 정렬).
25. As a 개발자, I want **Item Catalog**가 오프라인 **Catalog Merge**로 갱신되게, so that 런타임 크롤 의존을 줄인다.
26. As a 개발자, I want **Vision Provider** 키가 서버에만 있게, so that API 키가 노출되지 않는다.
27. As a 유저(2단계), I want **Drag Equip**으로 후보를 끌어 **Flat Preview**에 놓을 수 있게, so that 더 빠르게 교체할 수 있다.
28. As a 유저(2단계), I want **Embedding Rank**로 썸네일 유사도 재정렬된 후보를 보게, so that 텍스트 검색보다 사진에 가까운 순서를 받는다.
29. As a 유저(2단계), I want JP/NA **Server Selection** 데이터가 지원되게, so that 다른 서버 유저도 쓸 수 있다.
30. As a 유저, I want **Depth Preview**가 **Look Preset** 착용 상태와 맞게(가능 시) 열리게, so that 3D가 2D와 일치한다.

---

## Implementation Decisions

### Architecture (ADR 요약)

- **Custom Shell** (Next.js): UI, **Share Link**, localStorage, 분석 폴링/SSE.
- **Analysis API** (FastAPI): **Ephemeral Upload**, **Analysis Run**, **Vision Provider**, Catalog 검색, 큐 워커.
- **Queue:** Redis(또는 동급) + worker 프로세스; 슬롯별 job.
- **Catalog:** 오프라인 Python **Catalog Merge** → SQLite/JSON; web은 읽기 전용 API.
- **Vision Provider:** Google AI Studio Gemini API 무료 티어; 구독(Claude/Cursor/Gemini Advanced)은 런타임 미사용.
- **Embedding Rank:** MVP 생략; Phase 2 로컬 CLIP.
- **경매장·넥슨 오픈 API:** 범위 밖.

### Deep modules (테스트·교체 용이 인터페이스)

| Module | Responsibility | Stable interface (conceptual) |
|--------|----------------|------------------------------|
| **CatalogMerge** | labanyu + Sigkill + Community Dump → 정규 레코드 | `merge(sources) → CatalogSnapshot` |
| **CatalogStore** | server·slot·텍스트 검색 | `search(slot, server, query, limit) → Item[]` |
| **MatchHintGenerator** | 이미지+베이스 메타 → JSON | `generate(imageBytes, baseMeta) → MatchHintsBySlot` |
| **CandidateBuilder** | Hint → 후보 목록 | `build(hints, server) → CandidatesBySlot` |
| **AnalysisOrchestrator** | Run 생명주기·슬롯 job·상태 | `start(runId)`, `poll(runId) → SlotStatus[]` |
| **EphemeralBlobStore** | 분석 중만 바이트 보관 | `put(runId, bytes)`, `delete(runId)` |
| **LookPresetCodec** | 프리셋 직렬화 | `encode(preset) → string`, `decode(string) → preset` |
| **LoadoutState** | 착용·Dye 상태 | `equip(slot, item)`, `setDye(slot, rgb)`, `snapshot() → LookPreset` |
| **FlatPreviewComposer** | 레이어 합성 | `render(loadout, catalog) → layer stack / image` |
| **RateLimitGuard** | Gemini 무료 한도 | `acquire() → ok \| retryAfter` |

**Shallow / thin:** Next.js 페이지·레이아웃, iframe **Depth Preview** 래퍼, 폼 컴포넌트.

### Match Hint contract (Vision Provider 출력)

슬롯 키는 Sigkill **Equipment Slot** ID와 동일. 슬롯당 필드 예:

```json
{
  "slotId": "robe",
  "confidence": "high | low | none",
  "silhouetteKeywords": ["미니드레스", "코르셋"],
  "colorRgb": [120, 40, 180],
  "dyeablePreferred": true,
  "searchQueries": ["보라 미니드레스", "서큐버스 의상"]
}
```

한 번의 `generateContent` 호출로 전 슬롯 배열을 받는다(MVP). 실패 시 슬롯별 `confidence: none`.

### Candidate List pipeline (MVP)

1. **Match Hint** 전 슬롯 생성  
2. 슬롯별 `searchQueries` + `colorRgb` → **CatalogStore.search** (텍스트·카테고리, limit ~15 → 상위 ~10)  
3. `confidence: none` → 빈 목록 + UI 메시지  
4. (Phase 2) **EmbeddingRanker.rank** with local CLIP on thumbnail embeddings  

### Catalog Merge field precedence

| Field | Priority |
|-------|----------|
| slotIds, equipId, race/gender gates | Sigkill |
| displayName, category, description | labanyu |
| classId, internalName | Community Dump |
| thumbnailUrl | Sigkill → labanyu → dump |
| dyeable | Sigkill → labanyu |

불일치 레코드는 `mergeReview` 큐(수동 매핑 테이블)에 적재.

### Analysis Run flow

1. Client: Reference Image 로컬 미리보기 + Base Character + Server Selection  
2. User: **Analysis Run**  
3. Client → API: multipart **Ephemeral Upload** + metadata  
4. Orchestrator: Vision job → Match Hints → enqueue per-slot search jobs  
5. Client: poll/SSE `slotId → { status, candidates[] }`  
6. On complete/fail: **Ephemeral Upload** 삭제  

### Equip & Dye

- **Click Equip:** candidate → **LoadoutState**; apply **Dye Hint** if item dyeable  
- **Dye Override:** per-slot or per-item RGB; overrides hint until cleared  
- **Flat Preview** subscribes to loadout changes  

### Share Link & localStorage

- **Look Preset** schema version `v1` in URL (compressed JSON or base64)  
- Excludes Reference Image bytes  
- Invalid version → graceful error + empty loadout  

### Depth Preview (beta)

- iframe `mabi.sigkill.kr/charsimulator`  
- MVP: manual open; no guaranteed sync with **LoadoutState**  
- Phase 2: investigate save-link or URL param bridge  

### Tech stack

- Next.js (App Router), FastAPI, Redis queue, optional k8s: web / api / worker  

### Suggested module test focus (defaults for agent)

| Module | Unit tests | Rationale |
|--------|------------|-----------|
| CatalogMerge | Yes | 순수 함수, 고정 fixture |
| LookPresetCodec | Yes | round-trip, version migration |
| CatalogStore | Yes | fixture DB |
| LoadoutState | Yes | equip/dye rules |
| CandidateBuilder | Yes | mocked hints |
| MatchHintGenerator | Contract tests with mocked HTTP | 외부 API 경계 |
| AnalysisOrchestrator | Integration with fakes | job 상태 기계 |
| FlatPreviewComposer | Snapshot/layer order | 시각 회귀는 2단계 |
| Next.js UI | E2E smoke (optional Phase 1) | critical path only |

---

## Testing Decisions

- **원칙:** 모듈 **공개 인터페이스의 입출력**만 검증; Gemini HTTP 클라이언트 내부·React hook 구현은 mock.  
- **CatalogMerge / CatalogStore:** 고정 `fixtures/catalog/` 스냅샷; merge 충돌·server 필터.regression.  
- **LookPresetCodec:** encode→decode 동등성; unknown version 에러.  
- **LoadoutState:** 동일 슬롯 재착용, Dye Override 우선순위, 종족 불가 아이템 거부(메타 있을 때).  
- **CandidateBuilder:** hint `confidence: none` → 빈 리스트; query 병합 순서.  
- **AnalysisOrchestrator:** run 완료 시 ephemeral delete 호출 여부; 슬롯 partial failure.  
- **E2E (Playwright):** 업로드 → Analysis Run(mock API) → Click Equip → Share Link 복원 (1 시나리오).  
- **Prior art:** 그린필드; ADR·CONTEXT가 기대 동작의 기준.

---

## Out of Scope

- 넥슨 마비노기 오픈 API 경매장·시세(**Price Check**)  
- Claude Pro / Cursor / Gemini Advanced **구독**을 런타임 API로 사용  
- Sigkill 전체 UI 임베드·저장 URL 양방향 동기화(MVP)  
- **Embedding Rank** / 로컬 CLIP (Phase 2)  
- **Drag Equip** (Phase 2)  
- Reference Image의 **Share Link**·서버 장기 보관  
- 계정·로그인·클라우드 프리셋 DB  
- 자동 전 슬롯 착용(사용자 **Equip Action** 없이 일괄 적용)  
- 게임 클라이언트 연동·인게임 적용  
- JP/NA Catalog 데이터 (Phase 2; 스키마만 1차)  
- Gemini 유료 티어·Claude API 폴백 (명시적 결정 전까지)  

---

## Further Notes

- 이전 `README.md`는 후야 단일 레퍼런스 Discovery 세션 로그; 본 PRD는 제품 **Look Matcher**로 대체.  
- 레퍼런스 시뮬: [Sigkill 캐릭터 시뮬](https://mabi.sigkill.kr/charsimulator/), labanyu, Community Dump(itemdb.xml 등).  
- **Issue tracker:** 로컬 저장소에 GitHub/이슈 트래커 미연결. 이슈 생성 시 본 문서 본문을 붙이고 라벨 `ready-for-agent` 적용.  
- Phase 0( Catalog Merge CLI) → Phase 1(MVP web) → Phase 2(CLIP, Drag Equip, Depth sync) 순 권장.

---

## Module check (for product owner)

에이전트 기본 구현·단위 테스트 대상 모듈:

1. CatalogMerge  
2. CatalogStore  
3. MatchHintGenerator (boundary)  
4. CandidateBuilder  
5. AnalysisOrchestrator  
6. EphemeralBlobStore  
7. LookPresetCodec  
8. LoadoutState  
9. FlatPreviewComposer  

UI(Next.js)는 통합·스모크 위주. **Drag Equip / Embedding Rank / Depth sync**는 Phase 2 이슈로 분리 권장.
