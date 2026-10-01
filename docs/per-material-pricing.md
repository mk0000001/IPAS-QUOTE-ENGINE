# 필라멘트별 견적과 베드 옵션 / Per-filament quotes and bed options

## 한국어

하나의 출력에 여러 필라멘트가 사용되면 각 실제 제품과 원가 입력을 `material_selections` 배열로 전달한다. 호스트는 배열의 `usage_index`를 해당 플레이트 G-code 분석의 원본 `material_usage`와 연결하고 중량을 원본으로 대체해야 한다. 누락·중복·잘못된 인덱스와 전체 중량 불일치를 거부한다. 단일 제품을 전체 중량에 적용하는 방식으로 복수 소재를 바꾸지 않는다.

엔진은 각각의 `grams`와 `material_price`로 기존 Decimal 소재 원가 공식을 적용하고 합계 하나를 `MATERIAL`에 기록한다. `material_breakdown`은 제품·소재·중량·세전 금액·원 감지값을 보존한다. 기계 시간과 전력은 한 번 계산한다. 금액 표시 반올림은 합계와 맞춰야 하며 소재별 내역과 합계를 이중 합산하면 안 된다.

대표 장비 요율 소재는 명시적인 서포트 전용 항목을 제외한 모델 항목 중 최대 중량 항목이다. 여러 모델 소재의 조합 요율은 실증된 혼합 요율이 아니므로 검토 표시를 남긴다. 서로 다른 제품을 단일 제품으로 합치거나 소재 참고 강도에 혼합 평균을 사용하지 않는다. 별도 중량을 확인할 수 없을 때는 추정 배분 없이 검토를 요구한다.

`extras.bed_mode`는 `NONE`, `UNIFY`, `UNIFY_SPECIFIED`, `PURCHASE_SPECIFIED` 중 하나다. 정책의 `bed_fee_policy.mode_fees_krw`와 `purchase_landed_cost_share_ratio`가 금액을 정한다. 구매 옵션의 `bed_landed_cost`는 배송비·관세·세금을 이미 포함한 총 비용이다. 추가 비용을 다시 합치지 않고 정책 비율을 곱한 금액에 지정 서비스비를 더한다. 공급가 서비스 요금으로 기록한 뒤 기존 출력 부가세 규칙을 적용한다. 명시적인 옵션은 오래된 `plate_setup`/`plate_purchase`와 중복되지 않으며, 과거 정책 스냅샷의 원래 계산은 유지한다.

이 계산은 원가와 설정에 근거한 견적이며 실측 파단하중 검증이 아니다. G-code만으로 사용 제품·건조 상태·층간 접합 품질을 확정할 수 없다. 실제 제품 선택과 원본 감지값을 보고서에 함께 보존한다.

검증: `python -m pytest --noconftest tests -q` — 39개 테스트와 36개 하위 검사가 통과했다. 별도 제품별 Decimal 원가, 원본 중량, 베드 옵션 및 과거 정책 스냅샷 호환성을 포함한다. 호스트의 UI·DB·PDF·배포 검증은 별도로 수행하며 이 단위 테스트 결과를 전체 시스템 정확도나 실측 강도 검증으로 해석하지 않는다.

## English

Pass each actual filament and its price inputs in `material_selections`. The host must bind `usage_index` to the original selected-plate `material_usage`, replace submitted grams with authoritative source weights, and reject missing/duplicate/invalid indices and unreconciled total mass. A single product must not silently replace an entire mixed-material job.

The engine applies its existing Decimal material-cost formula independently to every row. It emits one summed `MATERIAL` component plus `material_breakdown` containing actual product/material/grams/net cost and original detections. Machine time and energy are charged once. Reports must reconcile displayed rounding to the saved total and avoid adding the material total twice.

The representative machine-rate material is the heaviest model row after excluding explicitly support-only rows. Mixed model-material machine rates require review; this heuristic is not an empirically calibrated blended rate. Distinct actual grades remain distinct for strength-reference selection. Unknown weights require review instead of invented allocation.

`extras.bed_mode` is one of `NONE`, `UNIFY`, `UNIFY_SPECIFIED`, `PURCHASE_SPECIFIED`. Host policy supplies `bed_fee_policy.mode_fees_krw` and `purchase_landed_cost_share_ratio`. Purchase mode multiplies fully landed `bed_landed_cost` (already including shipping, customs and taxes) by that share and adds the selected service fee. It does not add acquisition charges again. The resulting net service component follows the existing output-VAT policy. Explicit modes suppress legacy plate flags; frozen old-policy snapshots preserve their original behavior.

Pricing and geometry screening do not validate breaking loads. Actual product selection and original source detections must both be retained in customer reports.

Tests: `python -m pytest --noconftest tests -q` — 39 tests and 36 subtests passed, including per-product Decimal costs, authoritative weights, bed options and frozen-policy compatibility. Host UI, DB, PDF and deployment verification is separate; these unit checks do not establish whole-system accuracy or empirical strength calibration.
