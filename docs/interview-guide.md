# Interview walkthrough

Use the evidence links while explaining the work. Distinguish the original report and native-tool work from the October 2026 portfolio extraction and validation. Adapt the wording to what you personally completed and can explain.

## A short project introduction

“This project combines two Power BI dashboards with a comparison of Random Forest and Logistic Regression for loan default. I defined the default rate over known outcomes rather than all supplied customers, and the Power BI model uses twelve DAX measures. The report's model results show a clear tradeoff: Random Forest flags fewer cases and has higher precision, while Logistic Regression finds more defaults at the cost of many false positives. For the portfolio, I reconciled the original confusion matrices, made the code readable in GitHub, and documented weaknesses such as preprocessing before cross-validation.”

## A five-minute evidence route

| Time | Explain | Open |
| --- | --- | --- |
| First minute | Business problem and original two-page dashboard | [README](../README.md), [Power BI screenshots](powerbi.md) |
| Second minute | Known-outcome denominator, filter context, sample suppression and group sorting | [DAX](../powerbi/measures.dax), [M](../powerbi/Loan.original.pq) |
| Third minute | The original training/testing process, class imbalance and model switching | [Process screenshots](modelling.md#original-execution-screenshots) |
| Fourth minute | Actual model errors, review volume and majority-class baseline | [Matrices and metric audit](model-results.md) |
| Final minute | Reproducible checks and the evaluation improvements still needed | [Setup](setup.md), [validation](validation.md) |

## Questions to prepare

| Interview question | Evidence-based answer to develop |
| --- | --- |
| Why exclude unknown outcomes? | Missing labels are not negative labels. Explain numerator, denominator and population. |
| Which model did the report prefer? | Random Forest, for lower false-positive volume and higher precision in this comparison. Explain its 694 missed defaults and the validation still needed. |
| Why is 83.59% accuracy insufficient? | The all-fully-paid baseline reaches 89.39% with zero recall. Evaluate detected defaults, costs and review capacity rather than accuracy alone. |
| What does the tradeoff mean operationally? | Random Forest flags 1,314 cases; Logistic Regression flags 7,000. This is a count-based review-volume scenario, not measured staffing savings. |
| Why do the precision numbers differ slightly? | The report's fold mean is 27.94% for Random Forest, while pooled precision is 27.93%. A mean of ratios can differ from a pooled ratio. |
| Did you reproduce the reported performance? | I independently checked the screenshot arithmetic and population totals. I did not rerun training or reconstruct individual predictions. |
| Where should preprocessing and oversampling happen? | Fit learned preprocessing and sampling within each training fold; apply fitted transforms to validation data. The saved process needs this preprocessing improvement. |
| Which predictors matter most? | The report discusses financial risk factors, but the supplied images are one tree and a partial coefficient table. I would request full importance and stability evidence before claiming a global ranking. |
| What used AI? | The later portfolio documentation, extraction, metric checks and artificial fixtures used AI assistance; original figures are preserved and sourced. |

## 繁體中文講述重點

先展示實際儀表板，說明為什麼有效標籤才是分母。接著用混淆矩陣解釋模型取捨：隨機森林誤報少、漏判多；邏輯迴歸召回率高、審查量也高。最後說明你如何驗證數字，以及會如何改善前處理、閾值與獨立驗證。

不要把人工核對歷史數字說成重新訓練成功，也不要把作業選出的候選模型說成已能正式放款決策。能說明成果、取捨與證據限制，會比單獨列出工具或準確率更有說服力。
