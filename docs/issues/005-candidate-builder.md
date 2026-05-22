# Candidate Builder — Match Hint to Candidate List

**Labels:** `ready-for-agent`  
**Type:** AFK  
**Blocked by:** #004

## What to build

**Match Hint** 슬롯별 `searchQueries`·`confidence`를 받아 **Candidate List**(~10)를 만든다. `confidence: none`이면 빈 목록. **Slot Coverage** 우선순위로 정렬 메타를 붙인다.

## Acceptance criteria

- [ ] fixture hint + catalog → 슬롯당 후보 수 ≤ `candidate_limit_per_slot`
- [ ] `none` confidence → 빈 리스트, UI 메시지용 플래그
- [ ] **Embedding Rank** 미사용(MVP)

## Blocked by

- #004 Catalog Store
