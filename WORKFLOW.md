# 내 개발 워크플로

원칙: 내가 코드를 직접 보면서 주도한다. 테스트 먼저(TDD). 리팩터링은 green일 때 수시로. 에이전트에게 여러 단계를 통째로 맡기지 않는다.

## 한눈에 보기

| 상황 | 부를 것 |
|---|---|
| 새 프로젝트 첫 설정 | `/setup-matt-pocock-skills` → `/setup-pre-commit` → `/git-guardrails-claude-code` |
| 기능 설계 다듬기 | `/grill-with-docs` (작은 일이면 `/grill-me`, 그보다 작으면 생략) |
| 설계가 맞는지 손으로 확인 | `/prototype` |
| 구현 | `/tdd` |
| 큰 리팩터링 직전 | `/pstack:blast-radius` |
| 커밋 직전 | `/ponytail-review` |
| PR | `/pr` |
| 버그 | `/diagnosing-bugs` → `/tdd` |
| 세션 하나로 안 끝나는 작업 | `/to-spec` → `/to-tickets` |
| 여러 주짜리 큰 작업 | `/wayfinder` |
| 구조 점검 (몇 주에 한 번) | `/improve-codebase-architecture`, `/ponytail-audit` |
| 코드가 이해 안 될 때 | `/pstack:how`, `/pstack:why`, `/pstack:teach` |
| 컨텍스트가 길어졌을 때 | `/handoff` |
| 세션 끝 | `/retro` |
| 어떤 스킬을 쓸지 모를 때 | `/ask-matt` |

## 0. 프로젝트 설정 (한 번)

1. `/setup-matt-pocock-skills`: 이슈 트래커(로컬 파일도 됨), 라벨, 도메인 문서 위치를 정한다. `to-spec`과 `to-tickets`가 이 설정을 쓴다.
2. `/setup-pre-commit`: 커밋할 때 포맷, 타입체크, 테스트가 자동으로 돈다. TS 프로젝트라면 `/setup-ts-deep-modules`도 고려한다.
3. `/git-guardrails-claude-code`: 에이전트가 push, reset --hard 같은 명령을 못 쓰게 막는다. 주도권을 지키는 장치다.
4. 첫 설계 세션은 `/grill-with-docs`로 한다. `GLOSSARY.md`와 ADR이 생기고, 이후 `tdd`와 `code-review`가 이 용어를 따른다.

Ponytail 모드는 세션 시작 훅으로 항상 켜져 있다. 필요한 최소한만 바꾸게 한다. 강도는 `/ponytail lite|full|ultra`로 조절한다.

## 1. 기능 하나 만들기 (기본 루프)

```
/grill-with-docs ─▶ /tdd ─┬─ seam 합의 (내가 확인)
                          ├─ red → green  (한 slice씩)
                          └─ 리팩터링     (green일 때, 내가 요청할 때)
                     ─▶ /ponytail-review ─▶ 커밋 ─▶ /pr
```

1. 설계 다듬기. `/grill-with-docs`가 질문을 퍼붓는다. 답하는 동안 용어와 결정이 문서에 남는다. 설계가 맞는지 확신이 없으면 `/prototype`으로 버릴 시제품을 만들어 확인한다.
2. seam 합의. `/tdd`는 테스트를 쓰기 전에 어느 공개 인터페이스에 테스트를 걸지 묻는다. 여기서 승인하거나 고친다. 인터페이스 모양 자체가 고민이면 `codebase-design`의 용어(deep module, seam, adapter)로 이야기한다.
3. red → green. 테스트 하나, 통과시킬 최소 구현 하나. 한 번에 한 slice만 한다. 매 사이클 diff를 직접 본다.
4. 리팩터링. green 상태에서 "리팩터링하자"라고 말한다. 테스트는 계속 통과해야 하고 assertion은 바꾸지 않는다. 리팩터링 중 테스트가 깨지면 테스트가 구현에 묶여 있었다는 신호다. 범위가 diff를 넘어가면 먼저 `/pstack:blast-radius`로 영향 범위를 확인한다.
5. 3~4를 반복한다.
6. 커밋 전 `/ponytail-review`. 로직, 안전성, 테스트 공백, 불필요한 줄을 본다. 스펙 대비 구현까지 확인하려면 `/code-review`를 쓴다.
7. `/pr`로 PR 본문을 쓴다.

## 2. 세션 하나로 안 끝나는 작업

```
/grill-with-docs ─▶ /to-spec ─▶ /to-tickets ─▶ 티켓마다 1번 루프
```

- `/to-spec`: 지금까지 나눈 대화를 스펙으로 정리한다. 인터뷰는 하지 않는다.
- `/to-tickets`: 수직 슬라이스 티켓으로 쪼갠다. 티켓마다 막는 관계가 붙는다. 티켓 하나가 컨텍스트 하나에 들어가는 크기다.
- 티켓 하나를 고르고 새 세션에서 1번 루프를 돈다. `/implement`는 쓰지 않는다. tdd부터 커밋까지 에이전트가 혼자 진행하기 때문이다.
- 여러 주짜리 작업이면 `/wayfinder`가 결정 티켓 지도를 만든다. 결정을 하나씩 풀어 간다.

## 3. 버그

1. `/diagnosing-bugs`: 재현 → 가설 → 원인 확인 루프. 성능 회귀도 이걸로 본다.
2. 원인을 찾으면 `/tdd`로 실패하는 회귀 테스트를 먼저 쓰고 고친다.
3. 1번 루프의 6~7단계로 마무리한다.

## 4. 리팩터링 크기별

| 크기 | 언제 | 방법 |
|---|---|---|
| 작음 (이름, 추출, 정리) | tdd 루프 안, green일 때 | 그냥 요청한다 |
| 중간 (diff 밖으로 번짐) | 루프 안 | `/pstack:blast-radius` 다음에 진행 |
| 큼 (모듈 경계, 구조) | 몇 주에 한 번 | `/improve-codebase-architecture`: 자주 바뀌는 곳에서 deepening 후보를 찾고 하나 골라 설계를 다듬는다 |
| 지우기 | 몇 주에 한 번 | `/ponytail-audit`: 지울 것, 합칠 것, 위험한 곳 보고 |
| 넓은 기계적 변경 (rename 등) | 필요할 때 | `/to-tickets`가 expand → migrate → contract 순서로 쪼갠다 |

`/ponytail-debt`는 미뤄 둔 `shortcut:` 주석 목록을 보여 준다. 큰 리팩터링 때 같이 본다.

## 5. 세션 관리

- 에이전트 말이 이해가 안 되면 `/wait-what`. 다시 설명하게 한다.
- 코드의 동작 방식이 궁금하면 `/pstack:how`, 이유가 궁금하면 `/pstack:why`, 배우고 싶으면 `/pstack:teach`.
- 컨텍스트가 길어지면 `/handoff`로 인계 문서를 만들고 새 세션에서 이어 간다.
- 세션이 끝나면 `/retro`. 반복되는 교훈이 있으면 스킬이나 CLAUDE.md에 반영한다(`writing-for-agents` 참고).

## 아직 쓰지 않는 것

`/implement`, `/implement-spec`, `/chief-of-staff`, `/claude-handoff`, `software-factory`, `/pstack:poteto-mode`, `/pstack:arena`, `/pstack:swarm`. 모두 여러 단계를 에이전트에게 통째로 맡기는 도구다. 반복되고 지루한 작업이 생기면 `/implement`부터 시험해 본다.

## 로컬 수정 사항

- `.claude/skills/tdd/SKILL.md`: 원본은 리팩터링을 리뷰 단계로 미룬다. green일 때 내가 요청하면 리팩터링하도록 바꿨다. 원본 스킬을 업데이트하면 이 수정이 덮어써질 수 있다.
