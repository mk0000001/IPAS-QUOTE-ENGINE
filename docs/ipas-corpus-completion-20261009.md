# G-code 전수 검증 완료 기록 / Corpus completion record

## 한국어

IPAS **v0.5.30-compact-sections**, 강도 **v0.27.0**의 운영 배포와 최종 검증을 완료했습니다. 인쇄 입력 **1,691개 중 1654개**에서 조건부 예상 하중이 계산됐으며, **37개**는 구체적 근거 부족 또는 지원 범위 문제로 보류했습니다. 별도 제어 입력 2개를 포함한 전체 검증 범위는 1,693개입니다. 보류를 성공적인 강도 계산으로 세지 않았습니다.

| 보완 단계 | 인쇄 입력 | 수치 산출 | 사유가 있는 보류 |
| --- | ---: | ---: | ---: |
| 기준 단면 보완 / Reference sections | 1691 | 1645 | 46 |
| PAHT 제품 식별 / PAHT identity | 1691 | 1646 | 45 |
| FusRock 인장 자료 / FusRock tensile data | 1691 | 1653 | 38 |
| 최종 단면 자원 개선 / Final section resources | 1691 | 1654 | 37 |

원본 끝까지 확인한 입력 745개와 기존 기하 캐시에 기반한 인쇄 입력 946개를 구분합니다. 최종 모델 재생에서 원본 1,691개를 새로 스캔했다고 주장하지 않습니다. 최종 단면 정책으로 다시 계산한 대형 파일 1개와 재사용한 나머지 기하도 구분했습니다. 이 과정은 시험 및 결정론적 모델 검증이며, 출력물 파단 시험을 통한 학습이나 실측 보정은 아닙니다.

원본 745개 계산이 끝난 뒤 집계 파일 교체에서 발생한 권한 오류(exit 1)는 실패 기록으로 보존했습니다. 원본·산출물 해시와 전체 결과를 독립 확인한 후, 계산 재실행 없이 별도 집계 복구를 완료했습니다. 이전 소재 검증 대기 시간 초과와 경로 표기 불일치 실패도 보존했으며, 검토한 별도 실행 어댑터로 소재 모델 1회와 병합 1회를 완료했습니다.

최종 단면 검증의 대기 시간 초과, 검증 메타데이터 불일치와 모델 재생 실패 2회를 별도 기록으로 보존했습니다. 원본 메타데이터를 수정하지 않고 실제 부모·소스·기하·네이티브 증거를 확인하는 QA 연결부를 사용했으며, 빈 제어 입력 2개에만 검증된 메타데이터 별칭을 적용했습니다. 전체 1,693개 진단에서 기존 유효 단면과 자원 제한 단면이 함께 있는 캐시 16건의 갱신 문제를 확인했습니다. 제품 정책을 수정해 유효한 부분 결과를 보존하고, 유효 단면이 없는 순수 자원 제한 캐시만 재계산하도록 했습니다. 잘못된 원본·후보 식별·자원 정책 표시는 계속 거부합니다. 최종 모델 재생은 수정된 실제 제품 정책을 사용했으며 과거 캐시에 대한 검사 우회는 없습니다. 원래 모델 main은 실패 2회와 최종 성공 1회, 원래 gate 명령은 1회 실행했습니다. 전체 진단은 이 main 시도 횟수와 별도로 기록합니다.

이미지 검증은 첫 이미지의 오래된 시험 fixture 실패와 이후 세 이미지 통과로 이어졌습니다. 해당 네 이미지 실행에서 실제 선택 G-code 경로 계산은 총 4회였으며, 원본 745개 처리의 재시작은 없었습니다. 고정 fixture의 해시 확인 읽기와 초기 비공개 실험은 이 4회에 포함하지 않습니다. 마지막 두 이미지의 대상 기하 산출물 6개는 바이트 단위로 동일했습니다. 합성 시험의 교차 연산 호출 감소를 실제 전체 파일의 속도 향상률로 주장하지 않습니다.

FusRock ABS-GF 공식 인장 파단 자료는 XY **43.44 ± 0.86 MPa**, Z **19.02 ± 0.90 MPa**입니다. 건조 조건으로 표기된 시편·ISO 527·0.4 mm 노즐·250 °C 노즐·100 °C 베드·인쇄 속도 50 mm/s·100% 인필·±45° 조건의 자료로 구분했습니다. ± 값의 통계적 정의, 인장 시험 속도, 실제 함수율과 열처리 상태는 확인되지 않았습니다. 원자료에 내부 여유계수를 곱해 덮어쓰지 않습니다. 예상 하중 시나리오의 0.85 계수는 실측 보정이나 검증된 안전율이 아닙니다. [제조사 원자료](https://wiki.fusrock.com/zh/ABS-GF10/ABS-GF10)

실제 제품이 불명확한 복수 소재, 경로·압출 치수 누락, 비평면 경로, 불완전한 파일과 지원하지 않는 파손 역학에는 임의 숫자를 만들지 않았습니다. 가정한 국부 인장·굽힘 하중은 실제 전체 출력물의 파단 하중 또는 안전 사용 하중이 아닙니다. [최종 릴리스 상세](ipas-compact-sections-20261008.md), [검증 JSON](verification/ipas-corpus-completion-20261009.json). 이전 [부분 진행 기록](ipas-reference-capacity-20261008.md)은 당시 상태의 기록으로 보존합니다.

## English

Production IPAS **v0.5.30-compact-sections**, strength **v0.27.0**, was deployed and verified. Of **1,691 printing inputs, 1654** produce conditional reference loads and **37** retain explicit withholding reasons. Two controls bring the complete scope to 1,693. Withheld cases are not counted as numerical strength results.

The same table above records each completed model stage. The 745 inputs checked through original-source EOF are distinct from 946 cached printing geometry records. The final mixed replay reuses validated geometry and substitutes one independently computed dense-source record; it is not a fresh scan of all 1,691 sources or physical failure-data training.

The original 745-input orchestrator failed during receipt replacement after its computations completed. Its exit 1 remains recorded. Verified receipt aggregation recovered the complete ledger without rescanning or restarting source calculations. The earlier material-pipeline timeout and relative/absolute receipt-key guard failure remain separate failures; a reviewed adapter then ran one material replay and one merge.

The final-section timeout, metadata guard failures and two failed model replays remain preserved. Reviewed QA adapters derive invariants from pinned model, geometry, source and native evidence, and apply a verified metadata alias only to two empty controls. A diagnostic across all 1,693 inputs identified 16 legacy caches containing both valid and budget-limited declared sections. The product policy now preserves valid partial results and retries pure budget failures only when no valid declared section remains. Invalid source, candidate and resource-policy proofs remain rejected. The final replay uses the actual revised product policy with no historical cache-validation override. There were three original model-main attempts, two failed and one successful, followed by one original gate command. The diagnostic is counted separately; raw metadata and original failures remain unchanged.

Image lineage preserves the first stale-fixture failure and three later passes. There were four actual selected-source geometry passes across these images, no restarts of the original 745-input producer, and separate hash-only fixture reads. Earlier private experiments are not included in this image-pass count. Six target artifacts are byte-exact between the last two images. Synthetic overlay-call reductions are not a measured whole-file speedup.

The official FusRock ABS-GF tensile-break references, labeled dry and ISO 527, are **43.44 ± 0.86 MPa XY** and **19.02 ± 0.90 MPa Z**, under 0.4 mm nozzle, 250 °C nozzle, 100 °C bed, 50 mm/s printing speed, 100% infill and ±45° conditions. The statistical meaning of the ± values, tensile test speed, measured moisture content and annealing state are unknown. Raw properties remain unchanged. The scenario margin of 0.85 is not empirical calibration or a validated safety factor. [Manufacturer reference](https://wiki.fusrock.com/zh/ABS-GF10/ABS-GF10)

Missing material or deposition dimensions, conflicting exact products, incomplete exports, nonplanar paths and unsupported failure mechanics retain explicit reasons rather than invented numbers. Conditional local tensile/bending references do not establish whole-part fracture accuracy or safe working loads. [Final release](ipas-compact-sections-20261008.md), [verification JSON](verification/ipas-corpus-completion-20261009.json). The earlier partial snapshot remains a historical record.
