# Look Preset codec — Share Link round-trip

**Labels:** `ready-for-agent`  
**Type:** AFK  
**Blocked by:** None

## What to build

**Look Preset**을 URL·localStorage용 토큰으로 **encode**/**decode**한다. **Reference Image**는 포함하지 않는다. 지원 **schema_version**은 1뿐이며, 미지원 버전·손상 토큰은 **PresetDecodeError**로 명확히 실패한다.

## Acceptance criteria

- [x] encode → decode가 **Server Selection**, **Base Character**, 착용·**Dye Hint**/**Dye Override**를 보존한다
- [x] 미지원 schema 버전 decode 시 `unsupported schema` 오류
- [x] 잘못된 토큰 decode 시 **PresetDecodeError**
- [ ] Next.js **Share Link** 쿼리 파라미 `preset` 연동 (후속 이슈 007)

## Blocked by

None — can start immediately
