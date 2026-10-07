# IPAS 프로필 자동 선택·가격 근거 보존 / Profile auto-selection and price provenance

## 한국어

**IPAS v0.5.26-profile-autoselect**의 호스트 앱 변경이다. G-code에서 식별한 필라멘트마다 확인된 가격 기준을 자동 적용하고, 가격 기준 상품과 실제 출력 소재의 식별을 분리한다. 최종 v3의 전체 시험·배포·운영 검증을 2026-10-08에 완료했다.

| 구성 | 공개 저장소 | 수치 엔진 버전 |
|---|---|---|
| IPAS-GCODE ENGINE | [IPAS-GCODE-ENGINE](https://github.com/mk0000001/IPAS-GCODE-ENGINE) | 0.28.0 |
| IPAS-STRENGTH ENGINE | [IPAS-STRENGTH-ENGINE](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE) | 0.24.0 |
| IPAS-QUOTE ENGINE | [IPAS-QUOTE-ENGINE](https://github.com/mk0000001/IPAS-QUOTE-ENGINE) | 0.13.0 |

수치 엔진 패키지와 버전은 바뀌지 않는다. 이번 변경은 호스트의 프로필 식별·가격 카탈로그 연결·보고서 설명·가격 설정 검증이다. 기존 견적의 저장 결과와 정책 스냅샷은 새 가격으로 다시 쓰지 않는다.

### 바뀐 동작

- 확인 가능한 각 필라멘트는 첫 번째 항목을 수동으로 다시 선택하지 않아도 견적 준비 상태가 된다. 두 번째 이후 항목의 가격 변경·직접 선택·선택 해제와 프로젝트 복원도 준비 상태에 반영한다.
- 브랜드가 없는 Generic 소재는 국내에서 확인한 eSUN 가격 기준을 우선한다. 확인된 eSUN 기준이 없으면 가격을 임의로 채우지 않는다. `QIDI Generic`처럼 브랜드가 명시된 프로필은 브랜드 없는 Generic으로 바꾸지 않는다. Bambu·FusRock 등 명시된 브랜드와 제품은 정확한 프로필 규칙으로 연결한다.
- 자동 가격 적용은 원본 G-code의 소재·프로필·강도 참고 식별을 보존한다. Generic PETG에 eSUN PETG 가격을 적용해도 출력 소재를 eSUN 제품으로 확인한 것이 아니다. 직접 선택한 항목만 해당 선택 제품의 소재 참고로 전환한다. 자동/직접 선택이 섞인 경우 보고서에도 항목별 근거를 남긴다.
- 희소 툴 번호, 직접 툴 배열, 서로 충돌하는 프로필, 모델/서포트 구분을 검증한다. 서포트 제품의 직접 선택이 자동 식별된 모델 소재의 강도 근거를 바꾸지 않는다. 지연된 견적 응답은 자동/직접 선택의 근거가 달라지면 현재 화면에 적용하지 않는다.
- 가격 설정은 저장 전에 전체 요청을 검사한다. 잘못된 수수료 구조, 알 수 없는 항목, NaN/Infinity, 음수·과도한 값, 0 이하의 반올림 단위를 거부한다. 잘못된 요청은 쓰기 트랜잭션을 열지 않는다.

최종 v3에서는 고객 발송 배송비가 별도 선택 입력이라는 카탈로그 설명까지 바로잡았다. 직전 후보 대비 가격 숫자·계산 규칙·UI/PDF/강도 표시 코드는 바뀌지 않았다.

### 가격·배송·조달 가산액의 출처

카탈로그 확인일은 **2026-10-08**이다. 상품명·포장 중량·VAT·옵션을 구분하며, 리필/묶음 최저가를 스풀 포함 단품 가격 대신 넣지 않는다. 색상별 재고와 판매가는 바뀔 수 있다.

| 가격 기준 | 포장 | VAT 포함 표시가 | 출처 |
|---|---:|---:|---|
| eSUN 일반 PLA | 1kg | 19,800원 | [PLABS 상품](https://www.plabs.co.kr/product/detail.html?product_no=285&item_code=P00000KZ000A) |
| eSUN PETG | 1kg | 18,700원 | [PLABS 상품](https://www.plabs.co.kr/product/detail.html?product_no=161&item_code=P00000GF000S) |
| eSUN 일반 ABS 옵션 | 1kg | 18,700원 | [PLABS 상품](https://www.plabs.co.kr/product/detail.html?product_no=171&item_code=P00000GP00CB) |
| eSUN ASA+ 가격 참고 | 1kg | 24,200원 | [PLABS 상품](https://www.plabs.co.kr/product/detail.html?product_no=327&item_code=P00000MP000D) |
| eSUN PC | 500g | 23,100원 | [PLABS 상품](https://www.plabs.co.kr/product/detail.html?product_no=160&item_code=P00000GE000T) |
| eSUN TPU 95A 옵션 | 1kg | 44,000원 | [PLABS 상품](https://www.plabs.co.kr/product/detail.html?product_no=181&item_code=P00000GZ000O) |
| eSUN PETG-CF | 1kg | 24,200원 | [PLABS 상품](https://www.plabs.co.kr/product/detail.html?product_no=323&item_code=P00000ML000B) |
| Bambu PLA Basic, 스풀 포함 | 1kg | 22,000원 | [Bambu 한국 공식 스토어](https://kr.store.bambulab.com/products/pla-basic-filament?id=565422966019776519) |

PLABS의 [PETG 판매 페이지](https://plabs.co.kr/product/esun-petg-%ED%95%84%EB%9D%BC%EB%A9%98%ED%8A%B8-filament-1kg/161/)는 단품 배송비 3,000원과 10만원 이상 무료 배송을 표시한다. **필라멘트 입고 배송비 기본 하한 4,000원과 포장당 조달 가산액 2,000원은 운영자가 확인한 견적 정책**이며 판매처가 공시한 배송료나 제품 가격이 아니다. 이번 Generic 국내 가격 기준에도 입고 배송비 하한을 적용한다. 무료 배송이 명시된 기존 PPA-CF/PPS-CF 상품 예외는 기존 동작을 유지한다. 고객 발송 배송비는 별도 선택 입력이며 같은 일괄 견적에 한 번 적용한다. ASA+는 브랜드 미지정 ASA의 가격 참고로만 쓰며 소재 등급·강도를 ASA+로 바꾸지 않는다. 가격 기준 자체가 실제 장착 스풀이나 실측 강도를 인증하지 않는다.

### 검토·최적화와 검증 범위

검토 3회는 서로 다른 검토·수정·최적화 회차다. 전체 운영 서비스를 세 번 배포했다는 뜻이 아니다. 프로필 자동 선택과 복원, 가격 기준/소재 식별의 분리, 혼합 선택의 강도 설명과 오래된 응답 차단, 가격 설정의 잘못된 입력을 각각 검토했다.

| 회차 | 검토·수정 내용 |
|---|---|
| 1차 | 프로필 v2 매칭, 명시 제품/Generic 가격 자동 적용, 다중 슬롯과 수동 선택 보존. |
| 2차 | 중복 카탈로그 조회 캐시, 두 번째 이후 가격 변경 시 복원, QIDI 브랜드와 모델 주 소재 분리. |
| 3차 | 독립 감사로 희소 툴·혼합 선택의 원본 식별 보존, 같은 가격 ID의 자동/수동 변경 시 오래된 응답 차단, 가격 정책 입력 검증과 배송 설명 최종 수정. |

최종 JS의 **5슬롯 준비 상태 확인 마이크로벤치마크**는 5,000회 반복·7회 측정에서 캐시 우회 **168.792ms**, 캐시 사용 **79.1708ms**, **53.10% 감소**였다. 전체 앱·분석·뷰어·PDF 처리의 성능 개선율로 해석할 수 없다.

| 증거 | 최종 결과 |
|---|---|
| 로컬 실제 JavaScript 회귀 | 14개 suite PASS; 최종 JS SHA-256 `d7802cf3df5883ee1ff1a4f3c18d340851d5846b286259b5d2a46e070e1aa526` |
| 최종 v3 동결 이미지의 전체 프로젝트 pytest + UI 계약 | 792 passed, 21 skipped, 168 subtests passed; 44.45s; 의존성 경고 2건 |
| Node 없는 이미지의 skip 및 별도 보완 | Node 관련 5개 skip은 로컬 14개 standalone JS suite와 5개 inline pytest로 보완. 나머지 16개는 별도 운영 스캔 도구 13개·Windows HA 도우미 3개로 이번 범위 밖. |
| 단일/통합 PDF·고객/관리자 구분 | v2 이미지의 합성 5슬롯으로 기본·상세·통합 PDF 3개 생성, 4페이지 시각 검토. 자동 가격 근거·제품 표·조건/한계·IPAS 표시 확인. 최종 v3 전체 시험에서 PDF 회귀 3개 통과. |
| 실제 브라우저·API 프로필/가격 표시 | v2 배포 화면에서 Bambu PLA 4개와 Generic PETG 1개를 5/5 자동 선택하고 주 소재 PLA 유지. 서포트 수동 변경·이력 새로고침 후 선택과 주 소재 유지, 자동 선택 5/5 복원, 콘솔 오류 0건 확인. v3 제공 HTML/JS도 동결 해시와 일치. |
| 저장 견적 보존 비교 | v3 배포 전후 기존 저장 견적 100건의 전체 행 비교; 바이트 변경 0건. |
| API·analysis·viewer·worker의 이미지·소스 해시·버전·네이티브 모듈 | 네 서비스 모두 최종 v3 빌드 이미지·v0.5.26·동결 소스 해시·3개 수치 엔진 버전/네이티브 모듈 일치. 모두 실행 중, 재시작 0회·OOM 없음. |
| 배포 직전 유휴 작업·롤백 보존 | 활성 analysis/viewer 작업 각각 0건 확인 후 v3 배포. 직전 운영 v2 이미지의 롤백 태그 보존. |

전체 pytest는 v2 동결 이미지에서 한 번, 배송 설명을 수정한 최종 v3 동결 이미지에서 한 번 실행했다. 두 실행 모두 읽기 전용 소스 스냅샷과 독립 합성 PostgreSQL을 사용했고 합성 DB는 제거했다. v3 내부 집계 960은 792개 테스트와 168개 하위 검사의 합이며 별도 테스트 960개를 뜻하지 않는다. v2 브라우저/PDF 시각 검증은 UI·보고서·강도 코드의 해시가 v3와 같음을 확인해 보존한다. v3의 전체 시험과 실제 서비스 검증은 별도로 기록한다. 테스트 범위는 프로필·카탈로그·소재별 원가·원본 중량·보고서 근거·API·저장·업로드/재시도·뷰어·강도 연동·가격 설정 입력 검증을 포함한다. 이번 수정에서 대량 원본 corpus나 물리 출력·파괴시험을 다시 수행했다는 주장은 하지 않는다. 공개 패치는 런타임 10개 파일만 포함한다. 비공개 통합 테스트의 소스와 영수증 해시는 릴리스 검증에 사용하지만 공개 배포하지 않으므로, 공개 패치만으로 전체 호스트 DB/PDF/운영 검증을 재현할 수는 없다.

최종 v3 소스 동결: `c7838d475b211cfec579f9eb11b0f74db9dde1c9edd901ad041753ad41f4420e`. 빌드 이미지: `sha256:ee78add9a993d83709772d57fc55347d62c8c5b73aa381e26a84e84116237eea`. 최종 판정: **PASS — 동결 소스·전체 시험·배포·운영 검증 완료.** 물리 출력·실측 강도 검증 범위는 확대되지 않았다.

[호스트 런타임 패치](patches/ipas-profile-autoselect-20261008-v3.patch)는 직전 IPAS 레이아웃 릴리스 소스에 적용한다. 패치 SHA-256은 `61f5865c3e877e9387847ab2099de77b8dbc15309a267dc88460455332659647`이다. 원본 줄바꿈 보존을 위해 `git -c core.autocrlf=false apply --check` 후 동일 설정으로 임시 원본에 실제 적용하여 10개 파일의 바이트가 최종 동결 소스와 같음을 확인했다. `.gitattributes`로 Git 등록 시 패치 줄바꿈 변환도 방지한다. 고객 파일·DB 덤프·내부 요율표·비밀 정책 문서·서버 접속 설정은 포함하지 않는다.

## English

**IPAS v0.5.26-profile-autoselect** updates the host application's per-filament price selection and provenance. It applies a verified price reference to each identifiable G-code profile while preserving the distinction between a costing reference and the identity of the printed material. Final v3 full-suite, deployment and production checks completed on 2026-10-08.

Numerical packages remain unchanged: [IPAS-GCODE ENGINE](https://github.com/mk0000001/IPAS-GCODE-ENGINE) **0.28.0**, [IPAS-STRENGTH ENGINE](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE) **0.24.0**, and [IPAS-QUOTE ENGINE](https://github.com/mk0000001/IPAS-QUOTE-ENGINE) **0.13.0**. The changes affect host profile identification, catalog selection, report explanations and policy-input validation. Saved estimates and their policy snapshots are not rewritten using new prices.

### Resulting behavior

- Each verified filament can become quote-ready without manually reselecting the first row. Secondary price changes, explicit choices, cleared choices and project restoration update readiness.
- Unbranded Generic materials prefer verified domestic eSUN price references. Missing references require review instead of invented prices. A branded profile such as `QIDI Generic` retains its brand. Explicit Bambu, FusRock and other products require an exact profile rule.
- Automatic pricing preserves the original G-code material/profile and strength-reference identity. Applying an eSUN PETG price to Generic PETG does not identify the printed spool as eSUN. Only an explicitly selected row adopts the selected product's material-reference identity. Reports disclose automatic and manual provenance separately when mixed.
- Sparse tool IDs, direct tool arrays, conflicting profiles and model/support roles are checked. A manual support choice does not relabel an automatically identified model's strength reference. Delayed estimates cannot replace the current selection when automatic/manual provenance changes.
- The complete settings request is validated before opening a write transaction. Malformed fee maps, unknown keys, NaN/Infinity, negative or excessive values, and nonpositive rounding units are rejected.

Final v3 also corrects the catalog explanation that customer outbound delivery is a separate optional input. Prices, calculation rules and UI/PDF/strength display code are unchanged from the preceding candidate.

### Price and delivery sources

Catalog check date: **2026-10-08**. References distinguish product grade, package weight, VAT and options. Refill or bulk discounts do not silently replace single-package spool prices. Prices and color availability can change.

| Price reference | Package | VAT-inclusive reference | Source |
|---|---:|---:|---|
| eSUN standard PLA | 1kg | KRW 19,800 | [PLABS](https://www.plabs.co.kr/product/detail.html?product_no=285&item_code=P00000KZ000A) |
| eSUN PETG | 1kg | KRW 18,700 | [PLABS](https://www.plabs.co.kr/product/detail.html?product_no=161&item_code=P00000GF000S) |
| eSUN standard ABS option | 1kg | KRW 18,700 | [PLABS](https://www.plabs.co.kr/product/detail.html?product_no=171&item_code=P00000GP00CB) |
| eSUN ASA+ costing reference | 1kg | KRW 24,200 | [PLABS](https://www.plabs.co.kr/product/detail.html?product_no=327&item_code=P00000MP000D) |
| eSUN PC | 500g | KRW 23,100 | [PLABS](https://www.plabs.co.kr/product/detail.html?product_no=160&item_code=P00000GE000T) |
| eSUN TPU 95A option | 1kg | KRW 44,000 | [PLABS](https://www.plabs.co.kr/product/detail.html?product_no=181&item_code=P00000GZ000O) |
| eSUN PETG-CF | 1kg | KRW 24,200 | [PLABS](https://www.plabs.co.kr/product/detail.html?product_no=323&item_code=P00000ML000B) |
| Bambu PLA Basic with spool | 1kg | KRW 22,000 | [Bambu Korea official store](https://kr.store.bambulab.com/products/pla-basic-filament?id=565422966019776519) |

The [PLABS PETG listing](https://plabs.co.kr/product/esun-petg-%ED%95%84%EB%9D%BC%EB%A9%98%ED%8A%B8-filament-1kg/161/) publishes KRW 3,000 single-order delivery and free delivery above KRW 100,000. **The KRW 4,000 default filament inbound-delivery floor and KRW 2,000 procurement add-on per retail package are operator-confirmed quote policy**, rather than seller-published product prices or delivery charges. The inbound floor also applies to this release's domestic Generic references. Existing explicitly free-delivery PPA-CF/PPS-CF exceptions retain their prior behavior. Customer outbound delivery is a separate optional input applied once per quote batch. ASA+ is a costing reference for unbranded ASA; it does not change that material's grade or strength identity. A price reference does not authenticate the installed spool or validate printed strength.

### Review, optimization and evidence

Three cycles mean three distinct review/fix/optimization passes, not three deployments of the complete production system. They covered profile readiness and restoration, separation of costing from material identity, mixed-selection strength disclosures and stale-response guards, and invalid policy inputs.

| Pass | Review and changes |
|---|---|
| 1 | Profile v2 matching, automatic exact-product/Generic prices, multiple slots and manual-choice preservation. |
| 2 | Cache repeated catalog lookups, restore after secondary-price changes, separate the QIDI brand and primary model material. |
| 3 | Independent audit of sparse tools and original identities under mixed choices, stale-response guards for automatic/manual changes sharing a price ID, policy-input validation and final delivery-description correction. |

The final-JS **five-slot readiness microbenchmark**, 5,000 loops over seven passes, measured **168.792ms with cache bypass versus 79.1708ms with caching: 53.10% lower elapsed time**. This is not a whole-application, analysis, viewer or PDF speedup measurement.

| Evidence | Final result |
|---|---|
| Actual local JavaScript regressions | 14 suites PASS; final JS SHA-256 `d7802cf3df5883ee1ff1a4f3c18d340851d5846b286259b5d2a46e070e1aa526` |
| Final v3 frozen-image full project pytest plus UI contract | 792 passed, 21 skipped, 168 subtests passed; 44.45s; 2 dependency warnings |
| Node-free image skips and separate coverage | Five Node skips covered by 14 local standalone JS suites and five inline pytest checks. Remaining 16: 13 operational scan-tool checks and three Windows HA-helper checks, outside this release scope. |
| Single/combined PDF and customer/admin separation | Three basic/detailed/combined PDFs from a synthetic five-slot input on the v2 image; four rendered pages visually checked for automatic-price provenance, product tables, conditions/limitations and IPAS branding. All three PDF regressions passed in the final v3 full suite. |
| Live browser/API profile and price displays | On the v2 deployment, four Bambu PLA rows and one Generic PETG row automatically selected 5/5; primary material remains PLA. Manual support changes and history refresh retain the choice and primary material; automatic 5/5 restored with zero console errors. Served v3 HTML/JS also match the frozen hashes. |
| Preservation of saved estimates | All fields of 100 existing saved rows compared before/after v3 deployment; zero byte changes. |
| API/analysis/viewer/worker image, source, versions and native modules | All four services match the final v3 image, v0.5.26, frozen source hashes and all three engine versions/native modules. All running, zero restarts and no OOM kills. |
| Idle jobs before promotion and retained rollback | Zero active analysis jobs and zero active viewer jobs before v3 deployment; preceding production v2 image retained under its rollback tag. |

The full suite ran once on the frozen v2 image and once on final v3 after correcting the delivery description. Both runs used read-only source snapshots and isolated synthetic PostgreSQL; their synthetic DBs were removed. The v3 internal count of 960 is 792 tests plus 168 subtests, not 960 separate tests. The v2 browser/PDF visual evidence is retained after checking that the UI/report/strength code hashes match v3. The v3 full suite and live-service verification are recorded separately. Coverage includes profiles/catalogs, per-filament cost and authoritative weights, report provenance, API/storage/upload/retry behavior, viewer/strength integration and policy validation. This release does not claim a repeated full-source corpus scan or physical print/failure testing. The public patch contains only ten runtime files. Private integration-test sources and receipt hashes contribute to release verification but are not distributed, so the public patch alone cannot reproduce the complete host DB/PDF/production checks.

Final v3 source identity: `c7838d475b211cfec579f9eb11b0f74db9dde1c9edd901ad041753ad41f4420e`. Built image: `sha256:ee78add9a993d83709772d57fc55347d62c8c5b73aa381e26a84e84116237eea`. Final verdict: **PASS — frozen source, full tests, deployment and production checks completed.** Physical-print and measured-strength validation scope is unchanged.

Apply the [host runtime patch](patches/ipas-profile-autoselect-20261008-v3.patch) to the preceding IPAS layout release. Its SHA-256 is `61f5865c3e877e9387847ab2099de77b8dbc15309a267dc88460455332659647`. With source line endings preserved through `git -c core.autocrlf=false apply --check` and actual temporary-baseline application under the same setting, all ten reconstructed files matched the frozen source byte-for-byte. `.gitattributes` also prevents Git from converting the patch's line endings on staging. Customer files, database dumps, internal rate tables, private policy documents and server connection settings are excluded.
