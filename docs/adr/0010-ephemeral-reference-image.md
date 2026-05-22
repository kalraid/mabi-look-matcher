# Reference Image는 브라우저 보관, 서버는 분석 작업 중만 임시 보관한다

**Reference Image** 원본은 브라우저(File API·메모리)에 두고 **Share Link**·**Look Preset**에 넣지 않는다. **Analysis Queue** 처리를 위해 백엔드가 바이트를 잠시 받을 수 있으나, **Analysis Run** 단위 작업이 끝나면(성공·실패 포함) 즉시 삭제한다. 장기·세션·N일 보관은 1차 범위 밖.

**Status:** accepted
