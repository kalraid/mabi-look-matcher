# Catalog Merge CLI (Phase 0)

**Labels:** `ready-for-agent`  
**Type:** AFK  
**Blocked by:** None

## What to build

오프라인 **Catalog Merge** CLI가 labanyu·Sigkill·**Community Dump** fixture(이후 live export)를 합쳐 **Item Catalog** snapshot JSON을 쓴다. `config/catalog.merge.yaml` 우선순위를 따른다. Sigkill 동일 이름·다른 equip_id는 **merge review** jsonl에 기록한다.

## Acceptance criteria

- [x] fixture 3종 병합 → 2아이템 snapshot, slot·class_id·dyeable 정합
- [x] `look-matcher-catalog-merge` CLI로 `data/catalog.snapshot.json` 생성
- [x] duplicate sigkill equip → review queue
- [ ] live source 경로 문서화 (config/README)

## Blocked by

None — can start immediately
