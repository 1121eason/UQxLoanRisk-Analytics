# Validation status

Evidence reviewed on 26 October 2026. A successful offline inspection is distinct from execution in Power BI or RapidMiner.

| Check | Status and boundary |
| --- | --- |
| Input inventory and duplicate detection | SHA-256 and size recorded for ten supplied inputs, including two completed report PDFs; the two PBIX files are byte-identical |
| CSV structure and outcome audit | Executed on 14,999 rows; 24 fields; 9,998 valid targets; 1,061 defaults; no duplicate or empty IDs |
| Income aggregates | Recomputed from valid-label CSV rows and committed with the source hash |
| Power BI model extraction | 12 measures and 13 calculated-column expressions extracted; source paths parameterised before publication |
| PBIX stored outcomes | Decoded read-only: 14,999 rows/unique IDs, 8,937 fully paid, 1,061 default, 5,001 unknown; matches CSV outcome totals |
| PBIX source identity | Original M references another filename variant; no full record-by-record equivalence asserted |
| Report layout and original screenshots | Two Power BI pages and saved bindings inspected; actual dashboard screenshots extracted from report pages 3–4; metadata maps retained as supplements |
| RapidMiner process | Both XML files parsed; operator state, settings and connections inspected |
| Historical model evidence | Original process/result screenshots and confusion matrices visually checked; nine selected PNG figures published with source/hash manifest |
| Model arithmetic and cohort reconciliation | Both matrices total 9,998 outcomes and 1,061 defaults; reported micro metrics checked; pooled F1 and flag counts recomputed |
| Public audit and regression tests | Executed on artificial fixtures and metric edge cases; verifier checks source/figure hashes, model reconciliation, expected outputs and publication boundary |
| GitHub Actions | Workflow runs the public audit, tests and verifier; consult the repository Actions tab for current remote results |
| Power BI Desktop refresh, DAX execution and interactions | Not performed |
| Portable M adaptation | Source reviewed; not executed in Power Query |
| Fresh RapidMiner training or end-to-end reproduction | Not performed; report documents historical classifier runs and scores, but prediction-level outputs and trained models remain unavailable |
| Holdout performance, calibration or fairness results | Unavailable |
| Completed reports | Two supplied and inspected; student-named report is the main public-figure source. Submission receipt, grade and rubric compliance are not established |

Original screenshots and metadata design maps are labelled separately. The 89.39% majority-class baseline is arithmetic on labels; it is not a trained classifier result. Both reported models have lower accuracy than this baseline, while detecting some defaults. The evidence supports a historical tradeoff comparison, not production readiness.
