# Match Hint 비전 호출은 Google AI Studio(Gemini API) 무료 티어를 쓴다

**Match Hint** 생성은 FastAPI 워커에서 **Vision Provider**로 Gemini API(`generateContent` + 이미지)를 호출한다. **Google AI Studio** 무료 티어·`gemini-2.0-flash`(또는 동급 Flash)를 1차로 쓰고, 쿼터 초과 시 분석 큐 지연·사용자 안내 또는 유료 결제 연동을 2단계로 둔다. Claude Pro·Gemini Advanced·Cursor 구독은 런타임 크레딧으로 쓰지 않는다.

**Status:** accepted

**Considered Options:** Claude API(유료 크레딧), Cursor Cloud Agents, 수동 채팅 붙여넣기

**Consequences:** API 키는 `GEMINI_API_KEY`로 서버에만 둔다. 무료 한도는 Google 정책에 따라 변하므로 **Analysis Queue**에 rate limit·재시도가 필요하다.
