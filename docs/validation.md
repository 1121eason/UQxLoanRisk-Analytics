# Validation status

Evidence reviewed on 26 October 2026. A successful offline inspection is distinct from execution in Power BI or RapidMiner.

| Check | Status and boundary |
| --- | --- |
| Input inventory and duplicate detection | SHA-256 and size recorded for eight supplied inputs; the two PBIX files are byte-identical |
| CSV structure and outcome audit | Executed on 14,999 rows; 24 fields; 9,998 valid targets; 1,061 defaults; no duplicate or empty IDs |
| Income aggregates | Recomputed from valid-label CSV rows and committed with the source hash |
| Power BI model extraction | 12 measures and 13 calculated-column expressions extracted; source paths parameterised before publication |
| PBIX stored outcomes | Decoded read-only: 14,999 rows/unique IDs, 8,937 fully paid, 1,061 default, 5,001 unknown; matches CSV outcome totals |
| PBIX source identity | Original M references another filename variant; no full record-by-record equivalence asserted |
| Report layout | Two pages and original field bindings inspected; design maps reconstructed from metadata |
| RapidMiner process | Both XML files parsed; operator state, settings and connections inspected |
| Public audit and regression tests | Executed on artificial fixtures; repository verification checks expected output and the publication boundary |
| GitHub Actions | Workflow runs the public audit, tests and verifier; consult the repository Actions tab for current remote results |
| Power BI Desktop refresh, DAX execution and interactions | Not performed |
| Portable M adaptation | Source reviewed; not executed in Power Query |
| RapidMiner training or model comparison | Not performed; no saved scores supplied |
| Holdout performance, calibration or fairness results | Unavailable |
| Final submitted report, grade or rubric compliance | Not supplied / not established |

The maps are source diagrams, not native dashboard screenshots. The 89.39% majority-class baseline is arithmetic on labels; it is not a classifier result. Neither this repository nor the original artifacts establish production readiness.
