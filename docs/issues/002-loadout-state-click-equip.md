# Loadout state — Click Equip and Dye

**Labels:** `ready-for-agent`  
**Type:** AFK  
**Blocked by:** #001

## What to build

**LoadoutState**가 슬롯별 착용·**Dye Hint**·**Dye Override**를 관리한다. **Click Equip** 시 dyeable 아이템에 **Dye Hint** RGB가 기본 적용되고, **Dye Override**가 있으면 우선한다. `snapshot()`은 **Look Preset**과 호환된다.

## Acceptance criteria

- [x] 동일 슬롯 재착용 시 이전 dye 상태 정책이 테스트로 고정됨
- [x] **Dye Override**가 **Dye Hint**보다 **effective_rgb**에 우선
- [x] `snapshot()` → **LookPresetCodec** round-trip
- [x] 단위 테스트만 공개 API 사용

## Blocked by

- #001 Look Preset codec
