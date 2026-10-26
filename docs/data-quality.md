# Data quality and analytical consequences

The source audit uses the supplied CSV's exact bytes, with SHA-256 recorded in [`source-audit.json`](../analysis/source-audit.json). It does not overwrite the source or export individual customer records.

| Issue | Observed evidence | Treatment or interpretation |
| --- | --- | --- |
| Missing target | 5,000 blank `Loan_defaulted` values | Exclude from measured outcome rates and supervised fitting; do not relabel as fully paid |
| Malformed target | One value outside `0` and `1`, recorded as `0+T4261` in the original RMP filter | Treat as unknown; do not infer its intended outcome |
| Age gaps | 68 blank ages | Original RMP uses a fixed value of 39; a future fitted imputer belongs inside training folds |
| Employment gaps | 551 blanks and 278 literal `?` | Explicitly define whether both represent missingness |
| Occupation gaps | 551 blanks and 279 literal `?` | Same policy; do not assume an import tool converts `?` to null |
| Origin gaps | 190 blanks and 76 literal `?` | Preserve missingness and assess whether the field belongs in the model |
| Encoding mismatch | Supplied bytes require CP1252 decoding; original M requests UTF-8 | Use the right encoding and verify resulting category labels |
| Income sort mismatch | `50K–250K` uses en dash; original M matches ASCII hyphen | Normalise the comparison key; keep display text separate |
| Identical marginal debt counts | Mortgage and student debt each have 9,113 positive flags | These are **not duplicate columns**: only 7,921 of 14,999 row pairs match |
| ID integrity | 14,999 nonempty, distinct IDs | Confirms the current row/customer denominator reconciliation |

## Why the denominator matters

`1,061 / 14,999 = 7.07%` answers defaults as a share of all supplied rows, including unobserved outcomes. `1,061 / 9,998 = 10.61%` answers the default proportion among known outcomes. The latter is the portfolio's reported default rate, consistent with the original `Known_Customers` DAX design.

## What is tested

Behavioural tests check that missing and corrupt labels do not dilute rates, an entirely unlabelled cohort yields an unavailable rate, zero observed defaults remains a real zero, blanks and `?` stay distinct, duplicate and empty IDs are separated, CP1252 text survives loading, debt flags are compared per row, and malformed CSV structures fail visibly.

The source audit and PBIX stored counts are separate evidence. Equal aggregate counts do not prove the CSV and embedded data match for every customer and field. No data collection provenance or representativeness claim can be established from the filenames alone.
