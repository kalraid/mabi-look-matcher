# Simulator는 2D 합성을 기본으로 하고 3D는 별도 미리보기로 제공한다

**Custom Shell** 기본 뷰는 Catalog 썸네일 기반 **Flat Preview**(2D 합성)로 **Equip Action**을 즉시 반영한다. **Depth Preview**(Sigkill iframe 3D)는 사용자가 요청할 때 탭·모달로 연다. 3D와 착용 상태 동기화가 준비되기 전에는 Depth Preview를 베타로 표시할 수 있다.

**Status:** accepted

**Considered Options:** (A) iframe만, (B) 2D만, (D) 2D만 1차·3D 2단계

**Consequences:** Flat Preview용 레이어·슬롯 z-order 규칙이 필요하고, Depth Preview는 Sigkill 연동 조사·베타 품질을 사용자 기대치에서 분리해야 한다.
