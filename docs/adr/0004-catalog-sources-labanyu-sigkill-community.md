# Item Catalog는 labanyu·Sigkill·커뮤니티 덤프를 병합한다

**Item Catalog**는 (1) **Sigkill**의 슬롯·착용 ID·종족 제한, (2) **labanyu**의 카테고리·설명·검색 메타, (3) **Community Dump**(itemdb.xml 파생, 위키 등)의 클래스 ID·내부명·오프라인 일괄 필드를 **Catalog Merge**로 합친다. 슬롯·착용 정합성은 Sigkill 우선, 텍스트·카테고리 보강은 labanyu·덤프 우선으로 충돌을 해소한다.

**Status:** accepted

**Considered Options:** (A) labanyu만, (B) Sigkill만, (C) labanyu+Sigkill만

**Consequences:** 소스별 스키마·갱신 주기가 달라 **Catalog Merge** 규칙과 불일치 큐(수동 매핑)가 필요하다. 덤프는 최신 캐시샵 반영이 늦을 수 있어 labanyu/Sigkill로 덮어쓰는 필드를 정의해야 한다.
