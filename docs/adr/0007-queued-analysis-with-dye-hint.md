# 코디 분석은 게이트 후 큐 처리하고, 염색은 추천 RGB + 수동 덮어쓰기다

**Reference Image** 업로드 후 사용자가 **Analysis Run**을 시작하면, 슬롯 전체 **Match Hint**를 한 번(또는 소수)의 LLM 호출로 받고 **Analysis Queue**에서 슬롯별 Catalog 검색·**Embedding Rank**를 순차·병렬 처리한다. 슬롯별 **Candidate List**는 준비되는 대로 UI에 채운다.

**Dye Hint**는 Match Hint·이미지에서 추출한 슬롯·아이템별 추천 RGB다. **Equip Action** 시 기본 적용하며, 사용자는 **Dye Override**로 수동 변경할 수 있다. Sigkill·게임 팔레트와 다른 값은 가장 가까운 팔레트로 스냅하거나 raw RGB를 유지한다(구현 시 결정).

**Status:** accepted
