# Embedding Rank는 2단계에서 로컬 CLIP으로 도입한다

1차(MVP)는 **Match Hint** + **Item Catalog** 텍스트·카테고리 검색만으로 슬롯당 **Candidate List**를 만든다. **Embedding Rank**는 보류한다. Catalog 착용 썸네일이 충분히 쌓이면 FastAPI 워커에서 **로컬 CLIP**(오픈소스, API 과금 없음)으로 재랭킹을 켠다. Gemini multimodal 재랭킹은 무료 한도 소모를 피하기 위해 1차에서 쓰지 않는다.

**Status:** accepted
