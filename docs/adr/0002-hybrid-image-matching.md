# 레퍼런스 매칭은 LLM 비전 힌트 + (가능 시) 임베딩 재랭킹 하이브리드로 한다

**Reference Image** 분석은 1차에 LLM 비전으로 슬롯별 실루엣·색·키워드 **Match Hint**를 추출하고 **Item Catalog**를 텍스트·카테고리로 좁힌다. Catalog에 착용 썸네일이 있으면 CLIP 등 **Embedding Rank**로 슬롯당 Top 10을 재정렬한다. MVP는 Match Hint만으로 후보를 내며, 썸네일 파이프라인이 준비되면 Embedding Rank를 켠다.

**Status:** accepted

**Considered Options:** (A) 임베딩만, (B) 태그/키워드만, (C) LLM 비전만

**Consequences:** LLM API 비용·레이턴시가 있고, 게임 고유 아이템명은 Catalog 정규화·퍼지 매칭이 필요하다. 썸네일 수집·슬롯별 크롭 품질이 Embedding Rank 정확도를 좌우한다.
