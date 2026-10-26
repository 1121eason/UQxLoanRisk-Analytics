# 貸款違約分析作品集

**Power BI、DAX、Power Query、RapidMiner、分類模型、Python 資料驗證**

本專案源自昆士蘭大學 BISM7233 貸款違約案例，結合兩頁 Power BI 儀表板與隨機森林、邏輯迴歸的模型比較。本次加入實際作業報告的原始截圖，讓面試官直接檢查視覺成果、模型結果與分析判斷。

資料共有 **14,999 筆客戶、24 個欄位**。**9,998 筆具有有效還款標籤，1,061 筆違約，比例為 10.61%**。報告兩個混淆矩陣、CSV 核對結果與 PBIX 儲存的人數均能對上這個母體。

![作業原始客戶輪廓儀表板](evidence/figures/customer-profile-dashboard.png)

第二頁[財務與信用風險儀表板](docs/powerbi.md#original-dashboard-screenshots)探討收入、貸款金額、貸款用途與破產紀錄。這些是從實際作業抽出的畫面；另外製作的圖解與驗證程式有分別標示。

## 實際模型比較

| 模型 | 準確率 | 違約精確率 | 違約召回率 | 由合併計數重算的 F1 |
| --- | ---: | ---: | ---: | ---: |
| 隨機森林 | 83.59% | 27.93% | 34.59% | 30.91% |
| 邏輯迴歸 | 37.08% | 12.64% | 83.41% | 21.96% |

以上為作業報告中的歷史交叉驗證結果。前三項採用報告的 micro／合併數值，並以混淆矩陣重新核算。F1 由合併的 TP、FP、FN 重算，不是各折 F1 的平均值。本次整理沒有重新訓練模型。

![模型比較圖](assets/model-comparison.svg)

報告偏好隨機森林作為人工審查的候選模型，因為它標示 1,314 筆，其中誤報 947 筆；邏輯迴歸標示 7,000 筆，其中誤報 6,115 筆。代價是隨機森林只找到 367 筆違約，漏掉 694 筆；邏輯迴歸找到 885 筆，漏掉 176 筆。這說明模型選擇必須考慮審查量與漏判成本。

全部預測為未違約就有 **89.39% 準確率，但違約召回率為零**。兩個模型的準確率都低於這個基準，所以不能只靠準確率宣稱模型較好。部署前仍需要成本分析、閾值調整、校準與獨立驗證。[原始矩陣與完整解讀](docs/model-results.md)。

## 能力與實作證據

| 能力 | 具體實作 | 證據 |
| --- | --- | --- |
| 商業分析與指標定義 | 區分總人數、有效標籤數、違約數與比例 | [商業解讀](docs/business-analysis.md) |
| Power BI 視覺化 | 兩頁、十個分析圖表／矩陣、六張 KPI 卡、四個篩選器 | [原始畫面與技術導讀](docs/powerbi.md) |
| DAX | 12 個指標，使用 CALCULATE、DIVIDE、ALLSELECTED 等函數 | [實際公式](powerbi/measures.dax) |
| 特徵工程 | 13 個計算欄位，涵蓋標籤、年齡、教育、財務分組及排序 | [計算欄位](powerbi/calculated-columns.json) |
| Power Query | CSV 匯入、型態設定與收入排序 | [原始邏輯](powerbi/Loan.original.pq)、[可攜版本](powerbi/Loan.portable.pq) |
| 預測流程 | 角色設定、前處理、十折交叉驗證、訓練折內重抽樣與模型切換 | [原始流程與執行截圖](docs/modelling.md) |
| 模型評估 | 核對混淆矩陣、精確率／召回率、誤報與漏判取捨 | [實際比較](docs/model-results.md) |
| 驗證與溝通 | 資料品質檢查、人工範例、行為測試、GitHub Actions | [驗證狀態](docs/validation.md) |

## 面試中值得說明的判斷

- 缺少標籤不代表未違約，不能把全部資料列當成違約率分母。
- 同時看比例與樣本數；最低收入組只有 40 筆有效樣本。
- 區分「報告實際觀察到的模型表現」與「可重現、可部署的模型表現」。
- 訓練折內重抽樣有保留，但可學習前處理位於交叉驗證前，仍需要改善。
- 檢查原始收入排序的文字格式差異，以及貸款金額圖兩軸皆綁定違約率的設定。

## 執行公開驗證

需要 Python 3.10 以上，不需安裝套件。

```bash
python scripts/audit_data.py data/demo/loan_demo.csv --output output/demo-audit.json
python scripts/audit_model_results.py --output output/model-comparison.json
python -m unittest discover -s tests -v
python scripts/verify_repository.py
```

12 筆範例全部為人工建立；模型核對則使用報告的彙總計數。原始 CSV、PBIX 與完整 PDF 保存在本機 `private/`。GitHub 僅公開程式、彙總結果及九張經檢查的原始畫面。

**建議閱讀順序：** [英文主頁](README.md) → [儀表板](docs/powerbi.md) → [模型結果](docs/model-results.md) → [預測流程](docs/modelling.md) → [面試導讀](docs/interview-guide.md)。

作者：Yi Cheng Lee（Eason）。原始作業成果與 2026 年 10 月使用 AI 協助的作品集整理分別記錄於[來源與貢獻紀錄](evidence/README.md)。
