# 貸款違約分析作品集

**Power BI、DAX、Power Query、RapidMiner、分類模型、Python 資料驗證**

本專案源自昆士蘭大學 BISM7233 貸款違約案例，結合 Power BI 客戶輪廓分析與 RapidMiner 預測流程。作品集讓面試官直接檢查計算公式、視覺設計、模型設定與資料處理判斷。

資料共有 **14,999 筆客戶、24 個欄位**。其中 **9,998 筆具有有效還款標籤，1,061 筆違約，違約率為 10.61%**。PBIX 儲存的結果與這些人數一致。其餘 5,000 筆沒有標籤，另有一筆格式異常，均不放進已觀察違約率的分母。

![專案架構與資料核對結果](assets/project-overview.svg)

## 能力與實作證據

| 能力 | 具體實作 | 證據 |
| --- | --- | --- |
| 商業問題與指標定義 | 區分客戶數、有效標籤數、違約人數與違約率 | [分析解讀](docs/business-analysis.md) |
| Power BI 視覺化 | 客戶輪廓、財務與信用風險兩頁；十個分析圖表／矩陣、六張 KPI 卡、四個篩選器 | [儀表板導讀](docs/powerbi.md) |
| DAX | 12 個指標，使用 CALCULATE、DIVIDE、ALLSELECTED 等函數 | [從原檔擷取的公式](powerbi/measures.dax) |
| 特徵工程 | 13 個計算欄位，涵蓋年齡、教育、貸款分組與排序 | [計算欄位](powerbi/calculated-columns.json) |
| Power Query | CSV 匯入、型態設定、收入排序 | [原始邏輯](powerbi/Loan.original.pq)與[可攜版本](powerbi/Loan.portable.pq) |
| 預測流程設計 | ID／目標角色、缺失值處理、標準化、虛擬變數、十折交叉驗證、訓練折內重抽樣 | [原始 RapidMiner 流程](rapidminer/loan-default-original.rmp) |
| 模型評估思考 | 以召回率為主，設定準確率、精確率與 AUC；保留隨機森林比較設定 | [方法與限制](docs/modelling.md) |
| 可重現性 | Python 標籤與缺失值檢查、人工範例、行為測試、GitHub Actions | [驗證狀態](docs/validation.md) |

## 可以在面試中說明的判斷

1. **先確認分母。** 缺少標籤不代表沒有違約，不能直接把全部 14,999 筆當成已知結果。
2. **不能只看準確率。** 全部預測為未違約，在這批有效標籤中就能得到 89.39% 的準確率，因此還要看違約類別的召回率、精確率與 AUC。
3. **一起呈現比例與樣本數。** `<50K` 收入組的違約率為 25%，但只有 40 筆有效樣本；這個數字不足以直接建立放款規則。
4. **檢查資料文字與圖表綁定。** 收入字串中的短橫線與 en dash 不同，造成原始排序未命中；貸款金額組合圖也有兩軸皆綁定違約率的問題。
5. **檢查評估流程。** 原始流程在交叉驗證前完成部分可學習前處理，會影響驗證的獨立性；改善方案需把這些步驟放進訓練折。

以上區分原始設計、重新核算的結果與後續改善建議。這批檔案沒有提供模型成績、混淆矩陣或最終報告，因此不宣稱最佳模型或特定準確率。

## 執行範例

需要 Python 3.10 以上，不需安裝套件。

```bash
python scripts/audit_data.py data/demo/loan_demo.csv --output output/demo-audit.json
python -m unittest discover -s tests -v
python scripts/verify_repository.py
```

公開範例的 12 筆資料全部為人工建立，不是原始客戶資料。原始 CSV、PBIX 與課程文件保存在本機 `private/`，不會推送至 GitHub。原始 RMP、DAX、M 程式、視覺中繼資料及彙總結果可供公開檢查。

**建議面試閱讀順序：** [英文主頁](README.md) → [Power BI 實作](docs/powerbi.md) → [預測流程](docs/modelling.md) → [資料品質](docs/data-quality.md) → [面試導讀](docs/interview-guide.md)。

作者：Yi Cheng Lee（Eason）。原始 Power BI／RapidMiner 成果保留；2026 年 10 月的文件整理、程式擷取、核對腳本與人工範例使用 AI 協助，詳見[來源與貢獻紀錄](evidence/README.md)。
