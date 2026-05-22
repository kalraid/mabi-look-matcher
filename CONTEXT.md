# Mabi Look Matcher

레퍼런스 사진을 업로드하면, 기존 마비노기 캐릭터 시뮬레이터 위에 슬롯별로 비슷한 의상 후보를 보여 주고 골라 입혀 보는 웹 서비스.

## Language

**Look Matcher**:
사용자가 올린 참고 사진과, 선택한 종족·성별·나이 등의 베이스 캐릭터에 맞춰 의상 조합을 맞춰 보는 웹 앱 전체.
_Avoid_: 코스프레 도우미, 코디 추천기 (너무 일회성·캐주얼한 뉘앙스)

**Reference Image**:
사용자가 업로드한 “이렇게 맞추고 싶다”는 기준 사진. 원본은 브라우저에 두고, 서버는 **Analysis Run** 처리 중에만 임시 보관 후 삭제한다(ADR-0010).
_Avoid_: 레퍼런스, 원본, 소스 이미지

**Ephemeral Upload**:
**Analysis Queue**가 돌아가는 동안만 서버에 존재하는 **Reference Image** 바이트. 작업 종료 시 삭제된다.
_Avoid_: 임시 파일, 업로드 캐시

**Base Character**:
**Server Selection**·종족·성별·나이(및 시뮬이 지원하는 체형·얼굴 파라미터)로 만든 기본 외형.
_Avoid_: 베이스 모델, 아바타

**Server Selection**:
사용자가 고른 지역·서버(예: 한국/류트). **Item Catalog** 필터·**Simulator**·착용 가능 여부의 기준. 기본값은 한국 서버.
_Avoid_: 리전, 월드

**Equipment Slot**:
한 번에 하나(또는 시뮬이 허용하는 개수)만 착용하는 장비 부위. **Simulator**(Sigkill)가 노출하는 슬롯 ID·이름·순서를 1:1로 따른다. 1차 릴리스부터 전 슬롯을 지원한다.
_Avoid_: 파트, 부위 (슬롯과 혼동될 때)

**Slot Coverage**:
1차에 기능·UI 모두 열어두는 **Equipment Slot** 집합. Sigkill 전 슬롯과 동일(ADR-0003).
_Avoid_: MVP 슬롯, 코디 슬롯만

**Candidate List**:
레퍼런스 이미지와의 유사도 순으로 정렬된, 슬롯당 약 10개 내외의 아이템 목록. 화면 우측 패널에 표시된다.
_Avoid_: 추천 목록, Top N

**Simulator**:
착용 결과를 보여 주는 렌더링. **Flat Preview**(2D 썸네일 합성)가 기본이고, **Depth Preview**(Sigkill iframe 3D)는 선택적(ADR-0006).
_Avoid_: 드레스룸, 코디 시뮬

**Flat Preview**:
**Item Catalog** 썸네일을 슬롯 순서로 겹쳐 보여 주는 2D 뷰. **Equip Action**과 실시간 동기화한다.
_Avoid_: 2D 모드, 썸네일 뷰

**Depth Preview**:
Sigkill 등 WebGL 시뮬을 iframe으로 띄운 3D 뷰. 동기화 전까지 베타로 둘 수 있다.
_Avoid_: 3D 탭, iframe 시뮬

**Custom Shell**:
업로드·베이스 캐릭터 설정·슬롯별 Candidate List·Equip Action을 담는 자체 웹 레이아웃. 좌(또는 중앙)에 Simulator 뷰, 우측에 후보 패널을 둔다.
_Avoid_: 래퍼, 포털

**Item Catalog**:
labanyu·Sigkill·커뮤니티 덤프를 **Catalog Merge**한 뒤 서비스가 쓰는 정규 아이템 레코드 집합.
_Avoid_: DB, 아이템 DB

**Catalog Source**:
**Item Catalog**를 채우는 외부 출처 하나. Sigkill(슬롯·착용), labanyu(카테고리·설명), **Community Dump**(클래스 ID·내부명·xml 파생 필드)가 있다.
_Avoid_: 크롤러, API

**Community Dump**:
게임 클라이언트·모드 커뮤니티에서 유통하는 itemdb.xml 등 오프라인 아이템 덤프 및 위키 파생 데이터.
_Avoid_: xml, itemdb

**Catalog Merge**:
여러 **Catalog Source** 레코드를 정규화된 아이템명·ID로 합치고, 필드별 우선순위(Sigkill→슬롯, labanyu→설명, 덤프→class id 등)로 충돌을 해소하는 과정.
_Avoid_: ETL, sync

**Match Hint**:
**Vision Provider**가 **Reference Image**에서 뽑은 슬롯별 설명(실루엣, 색, 소재, 분위기 키워드). **Item Catalog** 텍스트·카테고리 검색의 입력이다.
_Avoid_: 프롬프트 결과, AI 분석

**Vision Provider**:
**Analysis Run** 시 이미지→JSON **Match Hint**를 만드는 외부 비전 API. 1차는 Google AI Studio **Gemini API** 무료 티어(ADR-0011).
_Avoid_: LLM, GPT

**Embedding Rank**:
**Match Hint**로 좁혀진 후보군을 착용 썸네일 벡터 유사도(CLIP 등)로 재정렬하는 단계. Catalog 썸네일이 없으면 생략한다.
_Avoid_: 이미지 검색, 벡터 검색

**Equip Action**:
후보에서 아이템을 착용 상태에 반영하는 동작. 1차는 **Click Equip**, 2단계는 **Drag Equip**(ADR-0009). **Dye Hint** 기본·**Dye Override** 가능.
_Avoid_: 착용, 입히기

**Click Equip**:
후보 항목 클릭 한 번으로 해당 **Equipment Slot**에 적용하는 **Equip Action**.
_Avoid_: 클릭 착용

**Drag Equip**:
후보를 **Flat Preview** 또는 슬롯 행으로 끌어다 놓아 적용하는 **Equip Action**. 2단계 기능.
_Avoid_: 드래그 착용, DnD

**Analysis Run**:
**Reference Image**·**Base Character**·**Server Selection**이 준비된 뒤 사용자가 시작하는 코디 분석. **Analysis Queue**를 돌린다.
_Avoid_: 분석 버튼, AI 실행

**Analysis Queue**:
**Match Hint** 추출 후 슬롯별 Catalog 검색·**Embedding Rank**를 백그라운드로 처리하는 작업 줄. 슬롯마다 준비 상태를 UI에 표시한다.
_Avoid_: job, worker

**Dye Hint**:
**Match Hint**·레퍼런스 색에서 나온 슬롯·아이템별 추천 RGB. **Equip Action** 시 기본 적용.
_Avoid_: 추천 염색, 자동 염색

**Dye Override**:
사용자가 **Dye Hint**를 덮어쓴 수동 RGB(또는 팔레트 선택). 아이템·슬롯 단위로 저장된다.
_Avoid_: 수동 염색, 커스텀 색

**Look Preset**:
현재 **Base Character**·착용·**Dye Hint**/**Dye Override**·**Server Selection** 스냅샷. localStorage에 자동 저장되고 **Share Link**로 공유할 수 있다.
_Avoid_: 코디 저장, 프리셋

**Share Link**:
**Look Preset**을 URL 파라미터(또는 짧은 ID)로 인코딩한 주소. **Reference Image**는 포함하지 않는다.
_Avoid_: 공유 URL, 딥링크

## Relationships

- 사용자는 **Reference Image** 1장·**Server Selection**·**Base Character** 설정을 제공한다
- **Item Catalog**·**Candidate List**는 **Server Selection**에 맞게 필터된다
- **Custom Shell**이 **Base Character**·착용 상태·**Candidate List** UI를 소유한다
- **Item Catalog**는 **Catalog Merge**로 **Catalog Source**들을 합쳐 생성·갱신된다
- **Analysis Run**이 **Analysis Queue**를 시작하고, 슬롯별 **Candidate List**가 준비되는 대로 표시된다
- 슬롯별 **Candidate List**는 **Match Hint** → **Item Catalog** 검색 → (선택) **Embedding Rank** 순으로 생성된다
- **Equip Action**은 **Dye Hint**를 기본 쓰고 **Dye Override**가 있으면 그 값을 쓴다
- **Look Preset**은 localStorage·**Share Link**로 유지된다(ADR-0008)
- **Equip Action**은 착용 상태를 바꾸고 **Flat Preview**를 갱신한다; **Depth Preview**는 동일 상태를 3D로 보여 준다(준비 시)
- **Base Character** 파라미터는 Sigkill이 지원하는 종족·성별·나이 등과 맞춘다

## Example dialogue

> **Dev:** "사진만 올리면 자동으로 전 슬롯이 채워지나요?"
> **Domain expert:** "아니요. 처음엔 유사도 상위 후보만 **Candidate List**에 뜨고, 사용자가 **Equip Action**으로 고릅니다. 자동 전체 착용은 1차 범위 밖입니다."

## Flagged ambiguities

- 이전 README의 **Price Check**(경매장 시세) 단계는 범위에서 제외됨 — **Look Matcher**에 경매·시세 개념 없음.
- 이전 README의 **일회성 보고서** 산출물은 **웹 앱**으로 대체됨.
- **Simulator** 통합은 **Custom Shell** 방식(ADR-0001)으로 확정 — Sigkill 전체 UI 임베드·저장 URL 동기화는 1차 범위 아님.
- 이미지 매칭은 **Match Hint** + **Embedding Rank** 하이브리드(ADR-0002) — MVP는 Match Hint만, 썸네일 준비 후 Embedding Rank 추가.
- **Slot Coverage**는 Sigkill 전 슬롯(ADR-0003) — 사진에 안 보이는 슬롯은 후보 없음·낮은 신뢰도로 처리.
- **Item Catalog** 소스는 labanyu+Sigkill+**Community Dump** 병합(ADR-0004).
- **Server Selection**으로 Catalog·Simulator를 필터(ADR-0005); 1차 데이터는 한국, 스키마는 다서버 확장.
- **Simulator**는 **Flat Preview** 기본 + **Depth Preview** 선택(ADR-0006).
- **Analysis Run**·**Analysis Queue**·**Dye Hint**/**Dye Override**(ADR-0007).
- **Look Preset** localStorage + **Share Link**(ADR-0008); Reference Image는 링크에 미포함.
- **Equip Action**: **Click Equip** 1차 → **Drag Equip** 2단계(ADR-0009).
- **Reference Image**: 브라우저 보관 + **Ephemeral Upload**(ADR-0010).
- **Vision Provider**: Gemini API 무료 티어(ADR-0011); Claude/Cursor 구독은 런타임 미사용.
- **Embedding Rank**: MVP 생략 → 2단계 로컬 CLIP(ADR-0012).
