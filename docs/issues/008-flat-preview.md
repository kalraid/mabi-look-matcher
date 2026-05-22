# Flat Preview — 2D layer compose

**Labels:** `ready-for-agent`  
**Type:** AFK  
**Blocked by:** #002, #004

## What to build

**FlatPreviewComposer**가 **LoadoutState**와 catalog 썸네일(없으면 플레이스홀더)로 2D 합성 뷰를 갱신한다. **Slot Coverage** 순서로 레이어한다.

## Acceptance criteria

- [x] equip/dye 변경 시 preview 갱신
- [x] 슬롯 z-order가 config 우선순위와 일치
- [x] 썸네일 없을 때 깨지지 않음

## Blocked by

- #002 Loadout state
- #004 Catalog Store
