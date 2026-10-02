# 출력 시간 범위와 전력 계산

G-code의 명시 모델 출력 시간과 전체 작업 시간을 구분합니다. BambuStudio 공식 구현은 `model printing time`을 전체 예상 시간에서 준비 시간을 뺀 값으로 출력하고, `total estimated time`과 3MF의 `prediction`은 전체 예상 시간을 사용합니다. 제조사 코드 확인일은 2026-10-03입니다.

공식 근거: [GCodeProcessor.cpp의 시간 헤더](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/libslic3r/GCode/GCodeProcessor.cpp#L709), [PartPlate.cpp의 3MF prediction 저장](https://github.com/bambulab/BambuStudio/blob/da8b44ee34dd349f2ae0df3f1cbae366df482354/src/slic3r/GUI/PartPlate.cpp#L7336). 제조사 커밋은 `da8b44ee34dd349f2ae0df3f1cbae366df482354`(2026-09-28)이며, 고정 커밋 파일과 조사 시 내려받은 파일의 SHA-256 일치를 확인했습니다.

호스트는 분석 출처가 명확하고 현재 견적의 입력 시간이 원본 시간과 일치할 때만 `duration_scope`와 명시 모델 시간을 전달합니다. 일반적인 `estimated printing time`, 수동으로 바꾼 시간, 잘못된 숫자, 전체 시간보다 긴 모델 시간은 명시 모델 시간의 근거로 사용하지 않습니다.

| 조건 | 출력 전력에 사용할 시간 | `pricing_print_seconds_basis` |
| --- | --- | --- |
| 전체 작업 시간, 유효한 명시 모델 시간과 근거 | 파일의 모델 시간 | `SLICER_EXPLICIT_MODEL_TIME` |
| 전체 작업 시간, 모델 시간이 없거나 무효이며 조건이 맞는 예열 이력 존재 | 전체 시간 − 역사적 평균 준비 시간 | `HISTORICAL_PREPARATION_DURATION_DIFFERENCE` |
| 출력만 포함하는 명시 시간 | 입력 시간 그대로 | `INPUT_PRINT_ONLY_DURATION` |
| 전체 작업 시간이나 준비 시간 분리 불가 | 입력 시간 그대로, 예열 추정의 불확실성 표시 | `TOTAL_INPUT_DURATION_PREPARATION_UNRESOLVED` |
| 시간 범위 불명 | 기존 입력 시간과 이론 예열 유지 | `UNRESOLVED_FULL_INPUT_DURATION` |

명시 모델 시간은 `process_settings.model_print_seconds`에 넣고, `energy_condition_sources.model_print_seconds`는 `GCODE_MODEL_TIME_HEADER`여야 합니다. 유한한 0 이상의 정수이며 전체 입력 시간을 넘지 않는 값만 사용합니다. 부울, 부동소수점 객체, 잘못된 문자열, 분수 시간, 범위를 벗어난 값이나 근거 누락은 시간 단축에 사용하지 않습니다.

예를 들어 전체 4,200초, 명시 모델 3,600초, 과거 준비 평균 500초·30 Wh, 출력 평균 200 W라면 예상 전력은 **0.23 kWh**입니다. 모델 시간이 없을 때의 역사적 준비 시간 차감은 3,700초·0.23556 kWh로 별도 표시합니다. 파일의 모델 시간이 있는데도 과거 준비 시간으로 이를 다시 추정하지 않습니다.

조건이 맞는 예열 실측량은 한 번만 더합니다. 예열 이력이 없으면 예열은 이론 추정으로 남고, 명시 모델 시간은 계속 사용합니다. 같은 플러그에 프린터와 건조기가 연결됐다면 합산 전력에 이미 들어 있는 건조기 부하는 다시 더하지 않습니다. 출력 종료 후의 정화·냉각이나 완료 후 유휴 전력은 명시 시간 범위와 중복 여부가 확인되지 않으면 임의 추가하지 않습니다.

이 결과는 과거 전력량과 슬라이서의 예상 시간을 결합한 미래 작업의 예상 소비량입니다. 현재 작업의 시작부터 끝까지 직접 계측한 소비량으로 표시하지 않습니다. 기존 입력에서 명시 모델 시간이 없을 때의 비용 계산과 역사적 예열 시간 차감 방식은 유지합니다.

---

# Print duration scope and energy calculation

The integration distinguishes explicit model time from total job time. BambuStudio emits model time as estimated total time minus preparation time; its total-time header and 3MF `prediction` use estimated total time. The manufacturer implementation was checked on 2026-10-03 using the source links above.

The host supplies duration scope and explicit model seconds only when source semantics are known and the quotation duration matches the analyzed file. Ambiguous estimated-time labels, edited durations, malformed values, and model times exceeding total duration cannot shorten priced printing time.

For `TOTAL_WITH_PREPARATION`, validated `model_print_seconds` takes precedence over subtracting a different historical preparation duration. The evidence field `energy_condition_sources.model_print_seconds` must be `GCODE_MODEL_TIME_HEADER`; the value must be a nonnegative integral number of seconds no greater than input duration. Missing or unusable explicit model time retains historical preparation subtraction when that history is applicable. Print-only scope uses input duration; unknown scope retains the existing fallback.

The output field `pricing_print_seconds_basis` distinguishes these paths. With total 4,200 s, model 3,600 s, historical preparation 500 s and 30 Wh, and printing at 200 W, the explicit-model estimate is **0.23 kWh**. Without model evidence, the historical-duration fallback is **0.23556 kWh**.

Matched preparation energy is added once. When preparation observations are unavailable, warm-up remains theoretical while validated model time is retained. Aggregate printer/accessory meters already include connected drying loads, so those loads are not added again. Post-print purification, cooling, and completed idle consumption are not arbitrarily added when duration scope and overlap are unknown. The result remains an estimated future-job consumption, not a completed measurement of that job.
