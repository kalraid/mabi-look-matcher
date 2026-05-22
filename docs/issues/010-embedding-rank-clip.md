# Embedding Rank — local CLIP (Phase 2)

**Labels:** `ready-for-agent`  
**Type:** AFK  
**Blocked by:** #004, #006

## What to build

Catalog 썸네일·**Reference Image** crop에 **로컬 CLIP** **Embedding Rank**를 적용한다. `embedding_rank.enabled=true`일 때만 후보 재정렬.

## Acceptance criteria

- [x] mock passthrough off 시 순서 변경 테스트
- [x] Gemini 추가 호출 없음
- [x] feature flag로 MVP 경로 유지

## Blocked by

- #004 Catalog Store
- #006 Analysis API
