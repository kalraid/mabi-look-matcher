# UI는 Next.js, 분석·큐는 FastAPI 워커로 분리한다

**Custom Shell**·**Flat Preview**·**Share Link**는 Next.js. **Analysis Run**, **Ephemeral Upload**, **Vision Provider**, **Analysis Queue**, Catalog 검색 API는 FastAPI. 큐는 Redis 등으로 web↔worker 연결. Catalog **Catalog Merge** 오프라인 배치는 Python CLI.

**Status:** accepted
