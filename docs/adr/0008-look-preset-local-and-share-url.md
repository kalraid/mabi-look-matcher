# Look Preset은 localStorage 자동 저장과 공유 URL로 유지한다

**Look Preset**은 착용 상태·**Dye Hint**/**Dye Override**·**Base Character**·**Server Selection**을 담는다. 브라우저 **localStorage**에 자동 저장하고, **Share Link**로 URL에 인코딩해 공유한다. **Reference Image**는 공유 URL에 포함하지 않는다(용량·개인정보). 서버 업로드 프리셋은 1차 범위 밖.

**Status:** accepted

**Considered Options:** (A) 세션만, (D) 계정·서버 저장

**Consequences:** URL 스키마 버전·마이그레이션 규칙이 필요하고, Catalog 아이템 ID 변경 시 옛 링크 깨짐을 처리해야 한다.
