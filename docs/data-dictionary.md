# Data dictionary

Field meanings are paraphrased from the supplied BISM7233 dictionary. Monetary currency, observation dates and the unit of the income period are not established by the dictionary; they should not be invented from the case's geographic context.

| Field | Role and meaning | Preparation / interpretation |
| --- | --- | --- |
| `Customer_id` | Customer identifier | Use as ID, not a predictor; unique in supplied CSV |
| `Age` | Customer age | 68 blanks; stored as text in PBIX, grouped with numeric conversion |
| `Work_class` | Employment category | Blanks and `?`; nominal |
| `Loan_amount` | Requested loan amount | Numeric; unit/currency and scale require source confirmation |
| `Education` | Educational qualification | Nominal; mapped to broader report groups |
| `Years_of_education` | Years of education | Numeric; overlaps conceptually with qualification |
| `Marital_status` | Marital-status category | Nominal; demographic interpretation |
| `Occupation` | Occupation category | Blanks and `?`; nominal |
| `Race` | Racial/ethnic category | Sensitive demographic field in original predictors |
| `Gender` | Gender category | Sensitive demographic field in original predictors |
| `State` | Residence state or region | Nominal; slicer in Customer Profile |
| `Capital_gain` | Investment/asset gains | Numeric; period unspecified |
| `Capital_loss` | Investment/asset losses | Numeric; period unspecified |
| `Weekly_work_hours` | Weekly working hours | Numeric |
| `Country/area_of_origin` | Origin category | Blanks and `?`; sensitive field |
| `Income` | Income band | `<50K`, `50K–250K`, `>250K`; normalise dash when comparing strings |
| `Current_mortgage` | Mortgage flag | 0=no, 1=yes |
| `Student_debt` | Student debt flag | 0=no, 1=yes; not identical to the mortgage flag |
| `Number_of_homes_owned` | Properties owned | Numeric count |
| `Bank_balance` | Bank-account balance | Numeric; currency and date unspecified |
| `Loan_purpose` | Loan-purpose category | Mixed wording; retain source labels unless mapping is justified |
| `Credit_history` | Credit-history length | Years according to source dictionary |
| `Past_bankruptcy` | Previous bankruptcies | Numeric count; report derives any/none status |
| `Loan_defaulted` | Observed target | 0=fully paid, 1=default/charged off; missing/corrupt values unknown |

There are 24 source fields. Power BI additionally has 13 calculated columns and the Power Query `Income_Sort` column. The source's collection process and representativeness are not established by these files.
