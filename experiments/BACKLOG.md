# 실험 후보

순서는 `01-baseline`의 `/retro`에서 실제로 불편했던 지점을 보고 정한다. 한 줄 = 한 변수.

- TDD 가드 훅: 테스트 파일을 건드리기 전에 구현 파일 수정을 막는 `PreToolUse` 훅
- 자동 테스트 훅: 파일 수정 후 테스트를 돌려 결과를 돌려주는 `PostToolUse` 훅
- 원본 `/tdd` vs `/my-harness:tdd`
