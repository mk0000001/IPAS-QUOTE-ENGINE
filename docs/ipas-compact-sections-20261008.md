# IPAS 대형 단면 예상 하중 복구 / Dense-section reference-load recovery

[한국어](#한국어) · [English](#english)

## 한국어

IPAS **v0.5.30-compact-sections**, 강도 **v0.27.0**을 실제 운영에 배포하고 검증했습니다. 코드 개정 27회·최초 등록 이후 업데이트 26회입니다. G-code v0.28.0, 견적 v0.13.0과 가격 정책은 유지합니다.

완전한 원본과 소재 참고값이 있어도 대량 경로의 국부 단면이 기존 보관 한도를 넘으면 예상 하중이 사라졌습니다. 선언 폭·높이의 경로 직사각 단면을 일정량씩 합치도록 수정했습니다. 공극·분리된 성분·도구 소유 정보를 보존하도록 구성했습니다. 합집합 순서에 따른 부동소수점 차이가 가능하며 전체 위상·비트 동일성을 보장하지 않습니다. 샘플링, 격자화, 단순화, 공극 채우기 또는 100% 인필 가정으로 면적을 키우지 않습니다. 한도에 도달할 때만 새 경로를 사용하며, 한도 미도달 입력의 기존 수집 순서를 유지합니다. 정상 계산의 회귀와 선택된 단면의 수치 일치를 별도로 검증했습니다. 선언 단면과 명령 체적 비교가 같은 자원 한도를 공유합니다. 자원이 부족하거나 기하 합집합이 실패하면 해당 단면의 수치를 보류합니다.

추가 제품 검토에서 유효 단면과 자원 제한 단면이 함께 있는 기존 캐시 16건을 확인했습니다. 갱신 때문에 기존 예상 하중이 사라지지 않도록 유효한 부분 결과를 보존합니다. 유효 단면이 전혀 없는 순수 자원 제한 캐시는 개선된 계산으로 다시 처리하며, 원본·후보·정책 검증은 유지합니다. 최종 배포 검증일은 2026-10-09입니다. [전수 검증 완료 기록](ipas-corpus-completion-20261009.md).

문제가 있던 대형 원본의 기준 단면 **6개 모두** 인장·굽힘 참고 하중을 계산했습니다. 최종 이미지의 전체 분석 최대 RSS는 **926.0 MiB**, 운영 한도는 1,536 MiB입니다. 작은 양수 하중·면적·단면계수가 0으로 반올림되지 않도록 웹·PDF 표시도 수정했습니다. 실제 극소 국부 성분은 약 **0.252 mg 무게 / 2.47e-6 N**, 면적 **0.00177 mm²**, 단면계수 **1.32e-6 mm³**로 표시됩니다. 이는 선택된 국부 경로 성분에 대한 가상 보 비교이며 전체 출력물이 이 힘에 부러진다는 의미가 아닙니다. 매우 짧은 경로 조각·둥근 실제 비드 끝·층접합의 측정 불확실성을 그대로 유지합니다. 이 입력의 명령 체적 대안은 지원되지 않는 원호 배분 때문에 보류했으며 선언 단면 결과와 혼동하지 않습니다.

| 검증 항목 | 실제 결과 |
|---|---|
| 동결 이미지 전체 호스트 시험 | 일반 982개 + 하위 검사 220개 통과, 22개 건너뜀 |
| 동결 이미지 전체 강도 시험 | 일반 319개 + 하위 검사 710개 통과, 0개 건너뜀 |
| 최종 입력 범위 | 1693개: 인쇄 1691개 + 대조군 2개 |
| 인쇄 입력 결과 | 수치 1654개, 이유가 확인된 보류 37개, 설명 없는 미산출 0개, 불변조건 오류 0개 |
| 기하 증거 | 기존 검증 기하 1690개 재사용, 새 이미지 기하 1개 계산 |
| 보고서 | 고객·관리자 4개 PDF, 36페이지 및 시각 검토 36페이지 |
| 운영 보존 | 기존 여섯 후보의 수치와 견적 이력 100건 유지, 네 서비스 이미지·건강 상태 확인 |

745개 원본 스캔의 전체 SHA·선택 바이트·EOF 증거와 946개 캐시 전용 인쇄 증거를 구분합니다. 이번 최종 이미지에서 문제 원본 한 개의 전체 기하를 새로 계산했고, 혼합 모델 재검사 자체에서는 원본을 다시 읽지 않았습니다. 이전 실험의 원본·보관 경로 읽기와 최종 이미지 계산은 별도 기록입니다. 기하 알고리즘 변경이 있으므로 전부 동일 알고리즘으로 원본을 재스캔했다고 주장하지 않습니다. EOF는 존재하는 바이트를 읽었다는 증거이며 의도된 출력 파일이 완전하다는 보장은 아닙니다.

소재·폭·높이 정보가 없거나 제품 등급이 충돌하는 입력, 잘린 원본, 비평면 경로와 지원 범위 밖 단면은 근거 없이 수치를 채우지 않습니다. 실제 이유별 집계는 [검증 JSON](verification/ipas-compact-sections-20261008.json)에 있습니다. 온도·속도·벽·인필은 원본에서 확인된 명령과 단면에 반영되지만 보편적인 경험 강도 배율이나 실제 접합강도를 발명하지 않습니다. 실측 파단시험이 없으므로 실제 파단하중·파단 위치·안전 허용하중 정확도는 검증되지 않았습니다. 제조사 원자료와 예상 하중용 여유계수도 분리합니다.

- [공개 호스트 패치](patches/ipas-compact-sections-20261008.patch): `706f9d2d27b1c4eed192d91d50afd1339755f7449ca6024c88b5f5519476cbd7`
- [강도 구현 커밋](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE/commit/7806089591b09d4f8e1b954a5219a2048eb3ca24) · [호스트 패치 커밋](https://github.com/mk0000001/IPAS-QUOTE-ENGINE/commit/14592d27bf782fae172a3c038764bf8969ec68f4)
- 동결 `b38289dc4bfc91928052c899fee34439b1ed647aff80c51b0a994ce584c0fcd8` · 이미지 `sha256:a8fa50491814f6ca5b6f4413aa9d0971c1f5b60ab13ee5e76884623024be00e9`
- 실행 버전의 이전 공개 소스 기준 `25a1ba1fcb5021d438e5c2f581f31d823eb7b5d4`는 위 실제 신규 공개 커밋과 구분합니다.
- [이전 공식 소재 보완](ipas-fusrock-tensile-20261008.md) · [공개 검증 요약](verification/ipas-compact-sections-20261008.json)

## English

IPAS **v0.5.30-compact-sections** and strength **v0.27.0** are deployed and verified in production: 27 code revisions, 26 updates after initial import. G-code v0.28.0, quote v0.13.0 and pricing remain unchanged.

Dense local sections could exceed retained-piece limits despite complete source and material references. Bounded unions now compact declared rectangular roads while retaining voids, disconnected components and positive-area tool ownership by design. Union order can cause floating-point differences; whole-topology or bitwise identity is not guaranteed. No sampling, rasterization, simplification, hole filling or 100% infill substitution inflates the section. Compaction starts only at a bound; the previous collection order is retained below it. Normal regressions and selected-section numerical agreement are checked separately. Declared and command-volume collectors share a resource budget. Exhaustion or union failure withholds affected sections.

An additional product review identified 16 existing caches containing both valid and budget-limited declared sections. Valid partial results are retained so refresh does not discard existing reference loads. Pure budget failures with no valid declared section are retried with the improved computation; source, candidate and policy validation remain enforced. Final deployment was verified on 2026-10-09. [Corpus completion record](ipas-corpus-completion-20261009.md).

All **six reference sections** in the affected dense source now produce tensile and bending reference loads. The final image's full analysis peaks at **926.0 MiB RSS**, below 1,536 MiB. Tiny positive forces, areas and moduli remain visible in web/PDF output: the observed microscopic component displays **0.252 mg / 2.47e-6 N**, **0.00177 mm²**, **1.32e-6 mm³**. This is a hypothetical local-road-component comparison, not a whole-part fracture load. Short road fragments, real rounded bead ends and unmeasured interlayer bonding remain limitations. Unsupported arc volume allocation withholds the command-volume alternative without discarding the supported declared section.

The frozen image passes **982 ordinary host tests + 220 subtests**, with 22 explicit skips, and **319 ordinary strength tests + 710 subtests**, with 0 skips. Final scope is **1691 printing inputs + 2 controls**: **1654 numeric**, **37 explained withheld**, **0 unexplained nulls** and **0 invariant failures**. We reuse 1690 validated geometry records and recompute 1 in the new image. Four customer/admin PDFs total 36 pages, with 36 pages visually reviewed. Production checks preserve the previous six candidate values and 100 saved quotes, and verify four service images and health.

Evidence distinguishes **745 original-source geometry records** from **946 cache-only printing records**. The final image performs one additional complete selected-source geometry pass; mixed model replay performs none. Earlier experiments are recorded separately. Geometry algorithms changed, so a full inventory rescan under one unchanged algorithm is not claimed. EOF proves consumption of existing bytes, not completeness of the intended export.

Missing material/dimensions, genuine product conflicts, truncated exports, nonplanar paths and unsupported geometry retain explicit reasons instead of fabricated numbers. [Public JSON](verification/ipas-compact-sections-20261008.json) contains observed reason counts. Source temperatures, speeds, walls and infill inform recorded commands/sections; universal strength multipliers and actual weld properties are not invented. Measured failure load/location and safe allowable load remain unvalidated. Raw manufacturer properties stay separate from the scenario margin.

- [Public host patch](patches/ipas-compact-sections-20261008.patch), SHA-256 `706f9d2d27b1c4eed192d91d50afd1339755f7449ca6024c88b5f5519476cbd7`
- [Strength source publication](https://github.com/mk0000001/IPAS-STRENGTH-ENGINE/commit/7806089591b09d4f8e1b954a5219a2048eb3ca24) · [Host patch publication](https://github.com/mk0000001/IPAS-QUOTE-ENGINE/commit/14592d27bf782fae172a3c038764bf8969ec68f4)
- Freeze `b38289dc4bfc91928052c899fee34439b1ed647aff80c51b0a994ce584c0fcd8` · image `sha256:a8fa50491814f6ca5b6f4413aa9d0971c1f5b60ab13ee5e76884623024be00e9`
- Runtime previous-source anchor `25a1ba1fcb5021d438e5c2f581f31d823eb7b5d4` is distinct from the actual new publication commits.
- [Previous official material update](ipas-fusrock-tensile-20261008.md) · [Public evidence](verification/ipas-compact-sections-20261008.json)
