# Look Matcher — TODO

MVP 이슈 #1~#11 완료 (`64ab34d`, mock 모드). 아래는 **실서비스 품질** 및 **Phase 2** 백로그입니다.

## 현재 상태

- Python: Analysis API, Orchestrator, Catalog 검색, Flat Preview, Embedding Rank stub
- Web: Custom Shell, Depth Preview beta, Drag Equip, Share Link (웹 전용 codec)
- 테스트: `pytest` 25 passed · `npm run build` OK
- 기본 모드: `LOOK_MATCHER_PROVIDERS__MODE=mock`

---

## 1. MVP 품질 마무리 (우선)

- [ ] **Share Link 통일** — 웹 `presetCodec.ts` ↔ Python `LookPresetCodec` (zlib/base64 동일 포맷, ADR-0008)
- [ ] **Dye Override UI** — 슬롯별 RGB/팔레트 수정 (PRD #12, `LoadoutState.set_dye_override` 연동)
- [ ] **localStorage Look Preset** — 새로고침 후 착용·염색 복원 (PRD #17)
- [ ] **Analysis Queue UI** — 슬롯별 pending / running / done 표시 (PRD #7, ADR-0007)
- [ ] **Flat Preview 실제 렌더** — catalog 썸네일 + 레이어 합성 (현재 플레이스홀더)
- [ ] **E2E 스모크 1건** — 업로드 → Analysis Run(mock) → Click Equip → Share Link 복원 (Playwright)

---

## 2. Live 모드 (mock → production)

- [ ] **Gemini Vision Provider** — `vision_provider.provider=gemini`, contract test (ADR-0011)
- [ ] **Rate limit / 에러 UI** — Gemini 무료 한도 초과 안내 (PRD #21)
- [ ] **Redis + analysis worker** — 슬롯별 job, run/slot 타임아웃 (ADR-0013)
- [ ] **Catalog Merge 정기 실행** — labanyu + Sigkill + Community Dump 전량
- [ ] **mergeReview 큐** — 필드 충돌 수동 매핑 (`data/merge_review.jsonl`)
- [ ] **sqlite CatalogStore** — `CatalogStore.from_sqlite` 구현

---

## 3. Phase 2

- [ ] **로컬 CLIP Embedding Rank** — 썸네일 임베딩 + `embedding_rank.enabled` (ADR-0012)
- [ ] **Depth Preview ↔ Loadout 동기화** — Sigkill URL/save-link 조사 + ADR 초안 (#9 선택)
- [ ] **JP/NA Server Selection** — catalog `server_ids` 확장 (ADR-0005)
- [ ] **종족/성별 착용 불가 필터** — LoadoutState + Catalog 메타 검증

---

## 4. 도메인 / 카탈로그 데이터 (후야 레퍼런스)

- [ ] **B안** — 염색 가능 코르셋·미니드레스 후보 수집 → catalog·Match Hint fixture
- [ ] **A안 백업** — 블랙 서큐버스의 옷 (비교용 프리셋)
- [ ] **날개** — 찬란한 데빌 해커의 날개 RGB 검증 (Sigkill)
- [ ] **가터** — 서큐버스 바디웨어 등 액세 슬롯 후보

---

## 5. 운영·인프라

- [ ] **CI** — `pytest` + `apps/web` build on push
- [ ] **k8s** — web / api / worker 분리 배포
- [ ] **보안 점검** — API 키, ephemeral TTL, CORS, 업로드 MIME/크기

---

## 권장 순서

```
Share Link 통일 → Dye UI + localStorage → Queue UI → Gemini live → Catalog 전량 merge → CLIP → Depth sync → E2E/CI
```

---

## 추천 에이전트 스킬

| 상황 | 스킬 |
|------|------|
| ADR/CONTEXT 맞추기 | `grill-with-docs`, `plan-eng-review` |
| 이슈 쪼개기 | `to-issues` |
| 버그·회귀 | `diagnose`, `investigate`, `tdd` |
| UI 검증 | `qa`, `browse` |
| PR·배포 | `ship`, `review`, `split-to-prs`, `setup-deploy` |
| 보안 | `cso` |
| 문서 동기화 | `document-release` |

---

## 로컬 실행

```bash
pip install -e ".[api,dev]"
uvicorn apps.api.main:app --reload --port 8000

cd apps/web && npm install && npm run dev
```

- API: http://127.0.0.1:8000  
- Web: http://localhost:3000  

---

## 참고

- [CONTEXT.md](./CONTEXT.md) · [docs/PRD-look-matcher.md](./docs/PRD-look-matcher.md) · [docs/issues/](./docs/issues/) · [docs/adr/](./docs/adr/)
