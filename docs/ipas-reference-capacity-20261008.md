> **과거 부분 진행 기록:** 이 문서는 당시 상태를 보존합니다. 최종 결과는 [2026-10-09 전수 검증 완료 기록](ipas-corpus-completion-20261009.md)을 확인하세요.
> **Historical partial snapshot:** This document preserves its original state. See the [2026-10-09 corpus completion record](ipas-corpus-completion-20261009.md) for the final result.

# IPAS 예상 하중 기준 단면·전달 검증 / Reference-section load delivery

[한국어](#한국어) · [English](#english)

## 한국어

IPAS **v0.5.27-reference-capacity**, IPAS-STRENGTH ENGINE **v0.25.0**을 운영에 반영했습니다. 얇은 영역 검출 결과가 없을 때 예상 하중이 사라지던 문제, 기준 단면이 웹·보고서에서 누락되던 문제, 동일 제품을 쓰는 다색 툴이 무조건 차단되던 문제를 수정했습니다. G-code v0.28.0·quote v0.13.0과 가격 정책은 유지했습니다.

### 계산과 표시

- 얇은 영역의 계산 가능한 국부 후보를 우선합니다. 없으면 모델 경로에서 협착·대표 기준 단면을 구성합니다. 대표 단면은 실제 최약 부위나 파단 순위를 확정한 결과가 아닙니다.
- 실제 선언 폭·높이와 명령 압출 체적으로 구성한 단면을 구분하고 공극·겹침을 반영합니다. 서로 떨어진 부품의 면적을 합치지 않으며, 면적·굽힘 단면계수·표시 위치는 동일한 연결 성분을 사용합니다. 원본 끝까지 읽기와 캐시 출처를 검증합니다.
- 축방향은 `F = σ × A`, 지원되는 굽힘은 `F = σ × Z / L`로 조건부 참고 하중을 계산합니다. 굽힘 거리는 10·25·50 mm이며 25 mm는 비교 조건입니다. 실제 고정점이나 하중점으로 확인한 값은 아닙니다. N과 중량 상당량(g/kg)을 함께 표시하며, 상세 수치는 kgf로 병기합니다.
- 단면의 실제 툴마다 소재를 연결합니다. 정확한 제품 참고값이 없고 알려진 단일 소재 계열의 제조사 비교값을 쓰는 경우 제품·출처·대용값임을 표시합니다. 다른 스풀의 전역 참고값을 빌려 쓰지 않습니다.
- 다색 툴을 함께 계산하려면 각 툴의 정확한 제품·출처·원자료·방향별 하중용 값·면적기준·지원 모드가 모두 일치해야 합니다. 균질·완전 접합은 명시한 미검증 가정입니다. 색상·배치·수분·툴간 접합의 실측 동등성을 뜻하지 않습니다. 다른 제품 또는 불명확한 제품을 임의로 합치지 않습니다.
- TPU처럼 선형 굽힘 모델이 지원되지 않는 소재는 가능한 축방향 값을 유지합니다. 미지원 굽힘에 숫자를 생성하지 않습니다. 제조사 원자료 MPa는 그대로 표시하고 내부 여유계수는 하중 입력에만 한 번 적용합니다. 실측 보정계수가 아닙니다.
- 웹 요약·후보 카드·고객 및 관리자 PDF가 같은 후보와 하중을 사용합니다. 보고서는 파일명 대신 실제 파싱된 설정을 사용합니다. 온도·속도·역할별 압출량은 명령 증거이며, 검증된 물성 전이식 없이 보편적인 강도 배율로 바꾸지 않습니다.

### 실제 검증 범위

| 항목 | 결과 |
|---|---|
| 동결 이미지의 호스트 전체 시험 | 882개 + 하위 검사 199개 통과, 환경별 21개 건너뜀 |
| 동결 이미지의 강도 엔진 전체 시험 | 316개 + 하위 검사 710개 통과 |
| JavaScript 및 로컬 보충 시험 | JS 27개; 로컬 Python 43개 + 하위 검사 1개 통과 |
| 전체 캐시 corpus | 인쇄 payload 1,691개와 비인쇄 대조군 2개 검증; 수치 939개, 캐시 불완전 745개, 완전 캐시의 설명 가능한 보류 7개, 원인 없는 미산출 0개, 불변조건 위반 0개 |
| 실제 원본 fixture | 103,768,099바이트 끝까지 재분석; 기준 단면 6개 모두 숫자·웹/PDF 하중 일치 |
| PDF | 고객 9쪽·관리자 10쪽 생성, 모든 수치 라벨·산식·산출물 해시 확인; 전체 페이지 contact sheet와 선택 페이지 원해상도 검토 |
| 운영 검증 | 네 서비스의 이미지·실행 파일 확인; 실제 브라우저 표시 6/6 및 저장 견적 100개 보존 |

캐시 corpus는 동결 v4에서 산출한 기하 자료와 출처를 보존하고 v6 하중 모델만 재실행했습니다. 원본 스캐너·기하 알고리즘·자동 단면 코드가 동일한지 바이트 단위로 확인하며, 변경된 세 파일은 하중 계산·통합에 한정됩니다. **캐시 검사 1,693건을 원본 전체 재스캔 1,693건이라고 표현하지 않습니다.** 캐시가 불완전한 745개를 원본의 계산 불가 사례로 확정하지 않습니다. 추가 원본 재분석은 대상 745개 중 159개 완료로 진행 중입니다. 전체 원본 재분석 완료를 주장하지 않습니다.

알 수 없는 소재, 폭·높이·필라멘트 지름 등 필요한 원자료 누락, 비평면 경로, 불완전한 단면, 검증되지 않은 복수 제품은 해당 계산을 보류하고 이유를 남깁니다. 모든 입력에 임의 숫자를 넣는 방식은 적용하지 않았습니다. 실제 비드·용융 접합·응력 집중·충격·반복하중·고정 조건의 파단 시험이 없으므로 실측 파단하중이나 안전 허용하중의 정확도 검증을 주장하지 않습니다.

색상에 따라 물성이 달라질 수 있다는 근거는 [Gao 등, Materials 15(19), 7039](https://doi.org/10.3390/ma15197039)를 참고합니다. 이 논문은 공출력 툴 경계나 현재 제품의 보정계수를 검증한 자료가 아닙니다. 동일 제품 다색 계산은 위에 명시한 조건부 모델의 확장이며 논문의 수치를 색상 배율로 전용하지 않습니다.

### 코드와 추적성

- 실제 강도 릴리스 코드 커밋: [`03ce183`](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE/commit/03ce183d7e7f9ffa73fe8a0ba2e5bccc68cbec49) · 개정 25회 / 최초 등록 이후 업데이트 24회. 문서·시험 전용 커밋은 집계에서 제외합니다.
- 동결 식별자: `d81f78dfffc0f3102300c98ba3e59aef546053c6b2b7e063d387e67ec1fc69bf`
- 배포 이미지: `sha256:1e038770091e53427238121ca7462d0ec0450d5d41c71bec295af236bd02df1d`
- [호스트 패치](patches/ipas-reference-capacity-20261008.patch): SHA-256 `c1d4e8b326627e66e987f5f26a0daf83e1c4cc086ea161c14cec16495cc05d8f`. 이전 v3 동결 원본에 적용한 27개 공개 파일이 새 동결 바이트와 일치합니다. 강도 패키지는 별도 저장소에서 제공합니다.
- 실행 `_version.source_commit`의 `f0656c8`는 직전 공개 기준점입니다. 이번 코드 커밋이라고 주장하지 않습니다. 실행 바이트는 동결 해시·이미지로 검증하며 실제 코드 커밋은 위에 별도로 기록합니다. 공개 전체 패키지는 줄바꿈 정규화 후 일치하고, 변경된 5개 패키지 파일은 동결 바이트와 일치합니다.
- [공개 검증 요약](verification/ipas-reference-capacity-20261008.json). 공개 저장소: [IPAS-QUOTE-ENGINE](https://github.com/mk0000001/IPAS-QUOTE-ENGINE), [IPAS-STRENGTH-ENGINE](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE). 비공개 정책·고객 원본·서버 설정·인증정보는 공개하지 않습니다.

## English

IPAS **v0.5.27-reference-capacity** and IPAS-STRENGTH ENGINE **v0.25.0** are deployed. The update fixes missing estimates when thin-region detection yields no candidate, missing reference sections in the web/report delivery, and unconditional rejection of multiple color tools using the same exact product. G-code v0.28.0, quote v0.13.0 and pricing policy remain unchanged.

### Calculation and delivery

Numeric local candidates take precedence; otherwise model roads supply constricted or representative reference sections. These do not establish the weakest location or a failure order. Declared dimensions and commanded-volume-equivalent sections retain separate assumptions, voids and non-duplicated overlaps. Area, bending modulus and displayed position refer to the same connected component. Source EOF and cache provenance are checked.

Supported conditional loads use `F = σA` for axial loading and `F = σZ/L` for bending, with explicit 10/25/50 mm moment arms. Cards pair N with equivalent Earth-gravity mass in g/kg; detailed values also use kgf. The default 25 mm is a comparison scenario, not an observed fixture. Each actual section tool resolves its material comparator. Known-family substitutions are explicitly named and never borrowed from another unresolved spool.

Multicolor estimates require individually resolved exact product/source/raw and directional references/area basis/load modes to match. Perfect bonding and homogeneous properties remain unverified assumptions, not measurements of color, batch, moisture or tool-boundary equivalence. Different or unresolved products remain separate. Unsupported TPU bending stays withheld while supported axial estimates remain available. Raw manufacturer MPa is unchanged; the unvalidated internal margin applies once to load inputs.

Web summaries, cards and both PDF audiences use the same candidates and loads. Actual parsed settings take precedence over filename text. Temperature, speed and role-wise extrusion are command evidence; they are not converted into universal strength multipliers without validated transfer laws.

### Verified scope

The exact image passed 882 host tests plus 199 subtests (21 environment-specific skips), 316 strength tests plus 710 subtests, and 27 separate JavaScript checks. A local supplement passed 43 Python tests plus one subtest; it is not image execution. Cache replay covers 1,691 printing payloads and two nonprinting controls: 939 numeric, 745 incomplete cached inputs and 7 explained withheld complete-cache inputs, zero unexplained nulls and zero invariant violations.

The original 103,768,099-byte fixture was read to EOF and all six reference candidates matched across web data and real customer/admin PDFs. PDFs have nine/ten pages; labels, arithmetic and artifact hashes were verified, with all pages reviewed as contact sheets and selected pages at full resolution. Four deployed services and the real browser display were verified; 100 saved estimates were preserved.

Cache replay preserves source-linked frozen v4 geometry and reruns only the v6 load model. Scanner, geometry and automatic-section sources are byte-identical; the three changed sources are restricted to load calculation/integration. **This is not a claim of 1,693 fresh original-source rescans.** The 745 incomplete cached inputs are not classified as intrinsically uncomputable originals. Additional complete-source rescans: 159/745 completed. Still running; full original-source rescan coverage is not claimed.

Unknown materials, missing dimensions/filament diameter, nonplanar paths, incomplete sections and unsupported multiple products retain explicit reasons rather than fabricated loads. This does not validate measured failure or safe working loads without part-level tests of actual beads, welds, notches, impact/fatigue and restraints. [Gao et al., Materials 15(19), 7039](https://doi.org/10.3390/ma15197039) supports color-dependent variability, not validation of current products or co-printed interfaces; no empirical color multiplier is imported.

### Traceability

Actual strength code commit: [`03ce183`](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE/commit/03ce183d7e7f9ffa73fe8a0ba2e5bccc68cbec49), revision 25 / 24 updates after initial import. Documentation/test-only commits are excluded. Source-freeze identity: `d81f78dfffc0f3102300c98ba3e59aef546053c6b2b7e063d387e67ec1fc69bf`. Image digest: `sha256:1e038770091e53427238121ca7462d0ec0450d5d41c71bec295af236bd02df1d`. The [host patch](patches/ipas-reference-capacity-20261008.patch), SHA-256 `c1d4e8b326627e66e987f5f26a0daf83e1c4cc086ea161c14cec16495cc05d8f`, reconstructs 27 public host files byte-for-byte against the previous v3 source freeze.

Runtime `_version.source_commit=f0656c8` is the previous published baseline anchor, not this release code commit. Executed bytes are identified by the freeze and image; the actual code commit is recorded separately. The whole public package matches after line-ending normalization; its five changed package files match frozen bytes exactly. See the [public evidence summary](verification/ipas-reference-capacity-20261008.json). Private policy, customer sources, server settings and credentials are excluded.
