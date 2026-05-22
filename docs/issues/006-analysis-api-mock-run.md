# Analysis API — mock Analysis Run end-to-end

**Labels:** `ready-for-agent`  
**Type:** AFK  
**Blocked by:** #005

## What to build

FastAPI가 **Analysis Run**을 받아 **Ephemeral Upload** 저장 → **Vision Provider** mock **Match Hint** → **Analysis Queue** inline mock으로 슬롯별 후보를 채운다. 완료 후 ephemeral 삭제. 클라이언트는 run id로 poll/SSE.

## Acceptance criteria

- [ ] POST analysis/run → run_id
- [ ] GET analysis/run/{id} → 슬롯별 status + candidates
- [ ] `LOOK_MATCHER_PROVIDERS__MODE=mock`만 기본
- [ ] run 종료 후 ephemeral 제거 검증 테스트

## Blocked by

- #005 Candidate Builder
