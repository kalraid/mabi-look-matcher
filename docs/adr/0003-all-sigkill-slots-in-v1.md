# 1차 릴리스부터 Sigkill이 정의한 전 Equipment Slot을 지원한다

**Look Matcher** 1차 범위는 코디 핵심 슬롯만이 아니라, **Simulator**(Sigkill)가 노출하는 **Equipment Slot** 전부(의상·날개·가발·액세서리·신발·장갑·모자·로브·무기·방패·펫 장비 등)에 대해 **Candidate List**와 **Equip Action**을 제공한다. 슬롯별 우선순위는 UI 정렬·Match Hint 가중치로만 반영하고, 기능적으로 잠그지 않는다.

**Status:** accepted

**Considered Options:** (A) 코디 핵심 4슬롯, (B) A+4 확장, (D) 사용자 선택 슬롯

**Consequences:** **Item Catalog**에 슬롯·썸네일·종족/성별 제한 매핑이 거의 전량 필요하고, Reference Image가 무기·펫 장비를 안 보여줘도 빈 **Candidate List** 또는 낮은 신뢰도 표시가 필요하다. MVP 일정은 Catalog 파이프라인이 병목이 된다.
