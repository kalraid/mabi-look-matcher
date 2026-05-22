# Catalog·Simulator는 UI에서 선택한 서버(지역)로 필터한다

사용자는 **Server Selection**으로 지역·서버(기본: 한국/류트)을 고른다. **Item Catalog**·**Candidate List**·**Equip Action**·**Simulator**는 선택된 서버에 존재·착용 가능한 아이템만 노출한다. 1차 구현은 한국 서버 데이터를 채우고, 스키마에 `server_id`를 두어 JP/NA 확장을 막지 않는다.

**Status:** accepted

**Considered Options:** (A) 한국만, (B) KR+JP/NA 토글, (C) 지역 무관 마스터

**Consequences:** **Catalog Merge** 시 소스별 서버 태그·미출시 아이템 처리가 필요하다. 서버 변경 시 착용 상태·Candidate List를 재계산하거나 경고해야 한다.
