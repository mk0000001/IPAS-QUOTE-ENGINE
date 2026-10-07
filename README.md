# IPAS-QUOTE ENGINE

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="branding/ipas/ipas-logo-light.svg">
  <img src="branding/ipas/ipas-logo.svg" alt="IPAS · Integrated Printing Analysis System">
</picture>

[한국어](#한국어) · [English](#english)

## 한국어

최신 호스트 릴리스: [IPAS v0.5.26 프로필 자동 선택·가격 근거 보존](docs/ipas-profile-autoselect-20261008.md). 수치 엔진은 G-code v0.28.0·strength v0.24.0·quote v0.13.0을 유지합니다.

**IPAS-QUOTE ENGINE**은 **IPAS / Integrated Printing Analysis System**의 견적 계산 엔진이다. 통합 시스템은 [IPAS-STRENGTH ENGINE](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE), [IPAS-GCODE ENGINE](https://github.com/mk0000001/IPAS-GCODE-ENGINE), [IPAS-QUOTE ENGINE](https://github.com/mk0000001/IPAS-QUOTE-ENGINE)을 연결한다. Python 패키지 이름 `print_quote_engine`은 기존 연동 호환성을 위해 유지한다.

릴리스 **v0.13.0** · 코드 개정 13회(최초 등록 이후 업데이트 12회). [커밋 집계](VERSION_HISTORY.json).

엔진 패키지를 변경한 도달 가능한 비병합 커밋 기준이다. 병합된 개발 이력은 포함하고 문서 전용·시험 전용·호스트 앱 변경과 자동 생성 `_version.py`는 제외한다. 개정 수는 기능 수나 정확도 검증 횟수가 아니다. 버전은 `0.<코드 개정 수>.<릴리스 메타데이터 수정>`이며 과거 결과에 버전이 없으면 미상으로 남긴다.

IPAS의 Decimal 기반 견적 계산기다. `calculate(input, policy)`에 호스트가 입력과 요금 정책을 전달한다. 공개 저장소에는 운영 요율·고객 데이터·서버 설정·접속정보가 없다. 정책 검증과 이식 가능한 예제 fixture는 계속 개발 중이다.

[필라멘트별 견적·베드 옵션](docs/per-material-pricing.md): 각 실제 제품의 사용량과 원가를 따로 계산하고 베드 준비 옵션의 중복 요금을 막습니다.

[출력·예열 시간 분리](docs/energy-duration-scope-20261003.md): 파일에 명시된 모델 시간은 출력 평균 전력에, 준비 단계는 조건이 맞는 실측 준비 전력에 각각 적용합니다. 같은 플러그의 건조 전력은 중복하지 않습니다.

### 전력과 할인

필라멘트 정책의 `method: DOMESTIC_LANDED_COST_PLUS_MARGIN_V1`은 호스트가 제공한 국내 구매가와 포장당 입고 배송비, 고정 조달 마진을 합쳐 사용 중량에 비례해 계산한다. 구매가와 입고 배송비의 포함 세금은 각각 제외한다. 마진은 `procurement_margin_krw`이며 `margin_tax_included`/`margin_tax_rate`로 가산액의 포함 세금을 별도로 지정한다. 필드가 없는 기존 정책은 세전 가산액을 유지한다. 입고 배송비 입력은 `material_price.inbound_shipping`과 별도 `inbound_shipping_tax_included`/`inbound_shipping_tax_rate`다. 고객 발송 배송비와 중복하지 않으며 기존 배율을 추가로 적용하지 않는다. method가 없는 과거 정책 스냅샷은 기존 `markup_multiplier` 계산을 유지한다. 운영 가격과 마진은 호스트가 제공한다.

호스트가 제공한 `energy_model`·`energy_telemetry` 스냅샷으로 전기요금을 추정한다. 조건이 맞는 과거 출력 구간의 평균전력을 우선하고 베드 크기·온도가 다르면 신뢰도가 낮은 열 모델로 환산한다. 이 패키지는 Home Assistant에 접속하거나 인증정보를 저장하지 않는다. `energy_kwh` 직접 입력이 우선하며 모델이 없는 과거 스냅샷은 이전 동작을 유지한다.

`energy`에는 추정 kWh·정상상태 W·초기 예열 Wh·기준 표본 시간·형상·온도 출처와 가정이 남는다. 새 작업을 직접 계측한 값은 아니다. 임시 모델의 전장/모터 35 W, 베드 12 W/m²/K, 가열 핫엔드당 0.12 W/K, 능동 챔버 3.5 W/m²/K와 두께 3 mm 알루미늄 상당 베드·효율 80%는 개발 가정이다. 검증된 제조사 히터 정격이 아니다. 대기 노즐 가열·누설·팬·예열 시간·MMU/건조기·단열·주변온도 영향에는 작업별 실측 보정이 필요하다.

선택 입력 `discount_percent`는 0–100의 십진 문자열이다. 양의 할인에는 최대 500자의 `discount_reason`이 필요하다. 서비스 소계와 배송비에 각각 할인을 적용해 1원 단위 half-up 반올림 후 정책대로 부가세를 다시 계산한다. 원금액·감면액·비율·사유·반올림 근거를 보존하며 새 할인율은 기존 할인에 중첩하지 않고 할인 전 입력부터 다시 계산한다.

여러 파일을 독립 견적하려면 `calculate_batch(items, policy)`를 사용한다. 입력 순서를 보존하고 항목별 성공·실패를 반환하므로 한 파일의 오류가 정상 파일 계산을 폐기하지 않는다. 한 번에 최대 50개이며 파일 분석·저장·권한·멱등성은 호스트 애플리케이션이 담당한다.

```sh
python -m unittest discover -s tests
```

관련 자료: [시스템 검증 범위](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE/blob/master/docs/system-validation.md).

---

## English

Latest host release: [IPAS v0.5.26 profile auto-selection and price provenance](docs/ipas-profile-autoselect-20261008.md). Numerical engines remain G-code v0.28.0, strength v0.24.0 and quote v0.13.0.

**IPAS-QUOTE ENGINE** is the quote calculation engine of **IPAS / Integrated Printing Analysis System**. The integrated system connects [IPAS-STRENGTH ENGINE](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE), [IPAS-GCODE ENGINE](https://github.com/mk0000001/IPAS-GCODE-ENGINE), and [IPAS-QUOTE ENGINE](https://github.com/mk0000001/IPAS-QUOTE-ENGINE). The Python package name `print_quote_engine` is retained for compatibility with existing integrations.

Release: **v0.13.0** · 13 recorded code revisions (12 updates after initial import). [Commit ledger](VERSION_HISTORY.json).

Count includes reachable non-merge commits touching the engine package, including merged development history; excludes documentation-only, tests-only, host-app changes and generated _version.py. It counts commits, not individual features or validated accuracy. Version convention: 0.<code revision count>.<release metadata fix>. Past results without a recorded version remain unknown.


[Per-filament pricing and bed options](docs/per-material-pricing.md) preserve separate product weights/costs and mutually exclusive bed service fees.

[Print/preparation duration separation](docs/energy-duration-scope-20261003.md) uses corroborated explicit model time for print-average power and matched measured preparation energy for preparation. Accessory power already included in the same meter is not added again.

Optional host-supplied `energy_model` and `energy_telemetry` snapshots enable estimated electricity costs. Matched historical print-phase average power is preferred; different bed sizes/temperatures use an explicitly low-confidence thermal scaling model. The host supplies geometry with provenance and telemetry grouped by observed heater temperatures. This package never connects to Home Assistant or stores connection credentials.

The result's `energy` field preserves estimated kWh, steady average W, assumed cold-start Wh, reference sample hours, geometry, temperature sources and assumptions. Direct `energy_kwh` input takes precedence. Old snapshots without `energy_model` retain legacy behavior. This is not metered consumption of a proposed job. The provisional model assumes a 35 W electronics/motor baseline, 12 W/m²/K effective bed heat loss, 0.12 W/K per heated hotend, and 3.5 W/m²/K active-chamber loss. A cold-start allowance uses a 3 mm aluminium-equivalent bed and 80% efficiency. These are configurable-model development assumptions, not verified manufacturer heater ratings. Unknown toolchanger standby heat, chamber leakage, fan speed, heat-up phase timing, auxiliary MMU/dryer circuits, insulation, and ambient conditions limit accuracy; real per-job calibration remains necessary.

Run portable tests with `python -m unittest discover -s tests`.

Optional quote inputs: `discount_percent` (decimal string, 0–100) and `discount_reason` (required for a positive discount, max 500 characters). Discounts apply to the final service subtotal and shipping; each is rounded to 1 KRW using half-up, and VAT is then recomputed with the supplied tax policy. The returned `discount` breakdown preserves original subtotal/VAT/shipping/total, reductions, percentage, reason, and rounding basis. Applying a new percentage recalculates from the undiscounted inputs rather than compounding the previous discount.

Standalone Decimal-based quote calculation for IPAS. Call calculate(input, policy). The host supplies its policy; this repository contains no production rates, customer data, server configuration, or credentials. Policy validation and portable example fixtures are still being developed.

The optional `DOMESTIC_LANDED_COST_PLUS_MARGIN_V1` policy removes included purchase and inbound-delivery VAT independently, normalizes the host-supplied package add-on using optional `margin_tax_included`/`margin_tax_rate` fields (missing fields preserve the prior pre-tax margin) and adds it, and allocates the sum by consumed grams/package weight. Customer delivery is separate. Missing method preserves historical markup snapshots; the new method never stacks the old multiplier. See [domestic retail references](docs/domestic-retail-references-20261001.md).

For independent per-file quotes, call `calculate_batch(items, policy)`. The result preserves input order and returns item-level success or failure, so one invalid file does not discard valid calculations. Batch size is limited to 50. Host applications remain responsible for file analysis, persistence, authorization and idempotency.
