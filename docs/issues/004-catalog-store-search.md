# Catalog Store — server/slot text search

**Labels:** `ready-for-agent`  
**Type:** AFK  
**Blocked by:** #003

## What to build

**CatalogStore**가 snapshot을 읽어 **Server Selection**·**Equipment Slot**·검색어로 아이템을 반환한다. `providers.mode=mock`일 때 fixture JSON을 사용한다.

## Acceptance criteria

- [x] `search(slot, server_id, query, limit)` 동작
- [x] mock fixture로 테스트, live는 sqlite 경로 스텁
- [x] 결과에 display_name, dyeable, thumbnail_url(optional)

## Blocked by

- #003 Catalog Merge CLI
