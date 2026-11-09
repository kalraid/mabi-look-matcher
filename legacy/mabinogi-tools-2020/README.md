# 마비노기 도구 (2020, 보관용)

2020-12 ~ 2021-01에 [dnd-project](https://github.com/kalraid/dnd-project)(던전앤파이터 도구 모음) 안의 `mabinogi` 패키지로 만들기 시작한 마비노기 도구입니다. 던파와 상관없는 기능이라 2026-11-10에 마비노기 관련 코드를 모으는 이 저장소로 옮겼습니다.

이 저장소의 본 기능(사진으로 의상 찾기)과는 별개이고, 빌드나 테스트 대상도 아닙니다.

## 구상했던 기능

| 패키지 | 내용 |
|---|---|
| `stuff/character` | 캐릭터(`MbCharacterVo`), 모험단(`MbAdvVo`) |
| `stuff/packging` | 인벤토리: 가방(`MbBagpackVo`), 은행 아이템(`MbBankitemVo`), 아이템(`MbItemVo`) |
| `stuff/bankslot` | 은행 슬롯 관리 |
| `stuff/training` | 직업·스킬 수련(`MbCharacterJobVo`, `MbCharaterJobSkillVo`, `MbTrainingVo`) |

## 상태

JPA 엔티티(VO)만 정의했고 controller·service는 빈 클래스입니다. 설계 단계에서 멈췄습니다.

- 스택: Spring Boot 2.3, Java 11, JPA
- 패키지 이름(`com.dnd.project.mabinogi`)은 원래 프로젝트의 것을 그대로 두었습니다.
- VO가 원래 프로젝트의 회원 엔티티(`CmUserVo`)를 참조하므로 이 폴더만으로는 컴파일되지 않습니다.
