# Interview walkthrough

Use the evidence links while explaining the work. Describe original implementation separately from the October 2026 portfolio additions, and adapt the wording to what you personally completed and can explain.

## A short project introduction

“This project explores loan default using Power BI and RapidMiner. I separated customer volume from known repayment outcomes, because about a third of the supplied records had no usable target. The Power BI model contains twelve DAX measures and two report pages. The RapidMiner process prepares mixed borrower data, uses ten-fold cross-validation and bootstraps the positive class inside the training fold. For the portfolio, I made the formulas and settings readable in GitHub and added reproducible data checks. I also documented evaluation weaknesses instead of claiming model scores that were not supplied.”

## A five-minute evidence route

| Time | Explain | Open |
| --- | --- | --- |
| First minute | Business question, 14,999 total rows, 9,998 known outcomes, correct denominator | [README](../README.md), [source audit](../analysis/source-audit.json) |
| Second minute | Filter context, safe division, sample-size suppression and interpretable groups | [DAX](../powerbi/measures.dax), [calculated columns](../powerbi/calculated-columns.json) |
| Third minute | Logistic regression, imbalance, training-fold sampling and the inactive forest | [RMP](../rapidminer/loan-default-original.rmp), [methodology](modelling.md) |
| Fourth minute | Encoding, category sorting, visual bindings and preprocessing leakage | [Power BI review](powerbi.md), [data quality](data-quality.md) |
| Final minute | Run the artificial fixture and describe the next valid evaluation | [Setup](setup.md), [evaluation proposal](modelling.md#next-evaluation-design) |

## Questions to prepare

| Interview question | Evidence-based answer to develop |
| --- | --- |
| Why exclude unknown outcomes? | A missing label is not a negative class. Explain numerator, denominator and which population the rate describes. |
| Why is 90% accuracy not enough? | The majority-class baseline is 89.39%. A model may appear accurate while missing nearly all defaults. |
| How does `ALLSELECTED` affect the risk ratio? | Explain current visual context versus selected comparison context using the actual formula. Verify interactions in Power BI before making a stronger claim. |
| Where should oversampling happen? | Inside each training fold. Show that the original bootstrap is there, then explain why preprocessing also needs to move inside. |
| Which model won? | No saved scores were supplied. Explain how identical folds, explicit default labels and recorded metrics would support a defensible comparison. |
| What did your review uncover? | Show the income dash/sort mismatch, duplicated combo-chart metric binding and missing-label denominator. |
| What is original and what used AI? | Original supplied Power BI/RMP artifacts are separated from the later extraction, scripts, docs and artificial fixture in the provenance register. |
| Could you deploy this for lending? | Explain the missing temporal validation, calibration, cost analysis, fairness review and operational inputs. Do not imply a production deployment. |

## 繁體中文講述重點

先說明商業問題與分母，再展示 DAX 與模型流程。說明「已設定流程」和「已驗證模型表現」的差異，並準備解釋為什麼只看準確率會誤導。最後挑一個實際發現的品質問題，展示如何找出原因、提出修正並安排驗證。

不要宣稱檔案中不存在的模型成績、最佳模型、財務效益或正式上線經驗。能清楚說明設計與限制，比單純列出工具名稱更能讓面試官判斷技術能力。
