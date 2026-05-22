# Depth Preview beta — Sigkill iframe

**Labels:** `ready-for-agent`  
**Type:** HITL  
**Blocked by:** #007

## What to build

**Depth Preview** 탭/모달에 Sigkill iframe을 띄운다. **Look Preset**과 동기화는 베타; 실패 시 “수동 확인” 안내. `depth_preview.beta=true` 설정 반영.

## Acceptance criteria

- [x] iframe URL from config
- [x] 베타 배지·동기화 미지원 문구
- [ ] (선택) save-link 연동 스파이크 결과 ADR 초안

## Blocked by

- #007 Next.js Custom Shell

## HITL note

Sigkill URL/저장 포맷 조사 결과에 따라 동기화 범위 결정 필요.
