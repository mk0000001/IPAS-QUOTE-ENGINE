# 출력·준비 시간 분리 / Print and preparation duration separation

## 한국어

파일 시간의 제조사 구현 근거와 상세 계약: [공식 시간 의미](energy-duration-semantics.md).

견적 엔진 v0.13.0은 전체 작업시간과 파일에 명시된 모델 출력시간을 구분한다. 호스트는 해당 파일의 시간 출처를 검증한 경우에만 `duration_scope`, `model_print_seconds`와 `energy_condition_sources.model_print_seconds=GCODE_MODEL_TIME_HEADER`를 전달한다. 수정된 수동 시간이나 모호한 시간 표기를 확정된 모델 시간으로 취급하지 않는다.

- `TOTAL_WITH_PREPARATION`에서 유효한 명시 모델 시간(0 이상, 전체시간 이하)이 있으면 출력 평균 W는 그 시간에만 곱한다. `pricing_print_seconds_basis=SLICER_EXPLICIT_MODEL_TIME`로 기록한다.
- 명시 모델 시간이 없거나 유효하지 않으면 조건이 맞는 역사적 준비 단계의 평균 시간을 전체시간에서 빼는 기존 방식으로 돌아간다. 근거는 `HISTORICAL_PREPARATION_DURATION_DIFFERENCE`이며 잘못된 명시 입력은 별도 가정 사유로 남는다.
- `PRINT_ONLY`는 입력 전체가 출력시간이다. `UNKNOWN`은 시간 범위를 임의로 확정하지 않으며, 전체시간용 모델 필드를 사용하지 않는다.
- 예열·준비 에너지는 조건이 맞는 과거 계측량을 별도로 사용하고, 없으면 기존 이론 예열 가정을 유지한다. 둘을 더하지 않는다. 출력 평균에 이미 포함된 AMS 건조·부속 장치 전력도 다시 더하지 않는다.
- 출력 종료 정화 단계가 별도 계측됐더라도 작업시간과 중복 여부가 확인되지 않으면 임의의 추가 요금으로 넣지 않는다.

예시 회귀는 전체 4,200초, 명시 모델 3,600초, 과거 준비 시간 500초, 출력 평균 200 W, 준비 에너지 30 Wh를 사용한다. 명시 모델 시간을 사용하는 결과는 `200×3600/3600000 + 30/1000 = 0.23 kWh`다. 과거 준비 시간 차감만 사용하면 3,700초를 출력으로 취급해 0.235556 kWh가 된다. 이는 계산 계약 검증을 위한 합성 사례이며 실제 장비 측정 기록이 아니다.

유효하지 않은 숫자·비정수·bool·비유한 값·전체시간 초과, 시간 근거 누락, 모델 시간 누락, 서로 다른 시간 범위, 계측 준비 자료가 없는 경우를 검증했다. 새 회귀 6개와 전체 견적 엔진 45개가 통과했다. 과거 준비량을 새 작업의 실제 소비량이라고 주장하지 않는다. 전력 프로파일·예열 조건·건조기 가동 상태와 데이터 공백은 호스트가 관리한다.

## English

Manufacturer timing implementation and detailed contract: [official duration semantics](energy-duration-semantics.md).

Quote engine v0.13.0 separates total job duration from explicit slicer model-print time. The host supplies `duration_scope`, `model_print_seconds`, and `energy_condition_sources.model_print_seconds=GCODE_MODEL_TIME_HEADER` only after verifying the selected file's timing semantics. Edited manual durations and ambiguous time labels do not establish model-print time.

- For `TOTAL_WITH_PREPARATION`, a corroborated integer model time between zero and total duration controls the print-average power term. The result records `SLICER_EXPLICIT_MODEL_TIME`.
- Missing or invalid model time retains the historical preparation-duration subtraction fallback, recorded as `HISTORICAL_PREPARATION_DURATION_DIFFERENCE`. Invalid explicit input retains a separate assumption flag.
- `PRINT_ONLY` uses the input duration; `UNKNOWN` does not adopt a total-scope model override.
- Preparation uses matched historical energy or the existing theoretical allowance, never both. Accessory/AMS-drying power included in the reference meter total is not added again.
- Independently observed end-purification energy is not arbitrarily surcharged while its overlap with job duration remains unresolved.

The synthetic regression uses total 4,200 s, explicit model 3,600 s, historical preparation 500 s, print average 200 W, and preparation 30 Wh. Explicit model time yields 0.23 kWh; historical-duration subtraction alone would yield 0.235556 kWh. This validates arithmetic semantics, not a real machine's consumption.

Six added regressions and all 45 quote-engine tests passed, covering invalid/partial/uncorroborated inputs and missing preparation observations. Historical preparation is not the proposed job's measured consumption. The host owns telemetry conditions, accessory operating state and coverage gaps.
