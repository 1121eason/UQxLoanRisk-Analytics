# Business interpretation

The analytical question is whether borrower profiles and financial characteristics differ between observed default and fully paid outcomes. The supplied data provide no loan observation date, repayment horizon, interest margin or realised loss. The analysis therefore supports case exploration and model design, rather than measured portfolio return or a live lending rule.

## Population and metric definitions

| Metric | Definition | Observed value |
| --- | --- | --- |
| Total customers | Distinct supplied customer IDs | 14,999 |
| Known outcomes | Target exactly `0` or `1` after trimming | 9,998 |
| Defaults | Target `1` | 1,061 |
| Fully paid | Target `0` | 8,937 |
| Unknown outcomes | Missing or malformed target | 5,001 |
| Default rate | Defaults / known outcomes | 10.61% |

The raw CSV has one row per unique ID, so row counts and distinct-customer counts reconcile for this input. That equality must be checked again if future data contain multiple loans per borrower. The default rate applies only to the labelled cohort; it cannot establish the outcomes of unlabelled customers.

## Income comparison

The [`income-segments.json`](../analysis/income-segments.json) output is recomputed from the supplied CSV using [`summarise_segments.py`](../scripts/summarise_segments.py).

| Income category as supplied | Known outcomes | Defaults | Default rate |
| --- | ---: | ---: | ---: |
| `<50K` | 40 | 10 | 25.00% |
| `50K–250K` | 6,407 | 826 | 12.89% |
| `>250K` | 3,551 | 225 | 6.34% |

The middle-income group has a higher observed default proportion than the highest-income group. This is an unadjusted association in a teaching dataset. Differences in employment, loan characteristics, observation periods or selection could explain part of the relationship. The smallest income group contains only 40 labelled cases, so its percentage should be accompanied by the denominator and uncertainty.

## Decisions the analysis can inform

| Analytical observation | Useful follow-up | Additional evidence needed |
| --- | --- | --- |
| Different observed rates across income groups | Investigate affordability and segment stability | Verified income, repayment obligations, observation horizon and adjusted analysis |
| Strong class imbalance | Compare default recall and precision with accuracy | Confusion matrices, validation predictions and decision costs |
| Missing labels and mixed missing-value markers | Clarify the eligible modelling population and import rules | Data lineage, missingness mechanism and label availability dates |
| Small segment denominators | Suppress unstable rates or show uncertainty | Agreed reporting threshold and larger representative samples |

These are proposed investigations. They are not evidence that changing a borrower characteristic changes risk, that a bank should decline a segment, or that the model produces a financial gain.

## Model choice and review workload

The actual report prefers Random Forest over Logistic Regression for its lower false-positive burden. Its confusion matrix implies 1,314 flagged cases, with 367 defaults detected and 947 fully paid cases flagged. Logistic Regression implies 7,000 flagged cases, with 885 defaults detected and 6,115 fully paid cases flagged. The counts describe historical predictions, not measured staff workload or a future approval policy.

This comparison connects modelling to review capacity: fewer flags reduce the number of cases a reviewer would inspect, while lower recall leaves more defaults undetected. The report's preferred candidate still misses 694 defaults and has lower accuracy than the all-fully-paid baseline. Without loss exposures, review costs, calibrated probabilities and independent validation, the evidence cannot select a profitable threshold. [Metric reconciliation and original matrices](model-results.md).

The report also discusses affordability, credit history and financial distress as factors for further investigation. The financial dashboard actually shown covers income, loan amount, purpose and bankruptcy. Strong claims about credit-history effects or global feature importance require additional model output beyond the partial figures supplied.

## Responsible use

The original model includes race, gender and country/area of origin among dummy-coded attributes. A future candidate should document why each feature is available and appropriate, compare versions with and without sensitive predictors, and evaluate subgroup errors and calibration. Removing a sensitive column alone does not establish fairness because other fields can act as proxies. No fairness result is claimed here.
