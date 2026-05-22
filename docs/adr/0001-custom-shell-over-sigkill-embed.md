# 자체 레이아웃(Custom Shell)으로 시뮬 UI를 구성한다

Look Matcher는 Sigkill 페이지 전체를 iframe으로 넣지 않고, **Custom Shell**(업로드·베이스 캐릭터·슬롯별 Candidate List)을 직접 만들고 3D 뷰는 Sigkill iframe 또는 정적 프리뷰로 붙인다. 아이템 메타·검색·유사도 순위는 labanyu/Sigkill에서 추출·정규화한 로컬 데이터셋을 사용한다.

**Status:** accepted

**Considered Options:** (A) Sigkill 전체 임베드 + 수동 착용, (B) 저장 URL로 iframe 동기화, (D) Sigkill 운영자 API 협의

**Consequences:** 초기에 아이템 카탈로그·썸네일·슬롯 매핑 파이프라인이 필요하고, Equip Action은 우리 UI에서 구현해야 한다. 대신 “사진 업로드 + 우측 Top 10 + 클릭/드래그 착용” UX를 Sigkill 기본 UI와 분리해 설계할 수 있다.
