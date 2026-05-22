# Next.js Custom Shell — upload, base character, right panel

**Labels:** `ready-for-agent`  
**Type:** AFK  
**Blocked by:** #001, #006

## What to build

**Custom Shell** UI: **Reference Image** 업로드(로컬만), **Server Selection**, **Base Character**, **Analysis Run** 버튼, 우측 슬롯별 **Candidate List**, **Share Link** 복사. API는 mock **Analysis Run**에 연결.

## Acceptance criteria

- [x] 업로드 미리보기, 분석 진행 UI
- [x] 후보 클릭 → API/loadout 연동 스텁 또는 #002 연동
- [x] **Share Link**에 preset 토큰 (이미지 없음)
- [x] `apps/web/.env.example` 변수 사용

## Blocked by

- #001 Look Preset codec
- #006 Analysis API mock run
