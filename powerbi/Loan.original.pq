// Original Power Query, with the local source path replaced by CsvPath.
let
    Source = Csv.Document(File.Contents(CsvPath),[Delimiter=",", Columns=24, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Customer_id", type text}, {"Age", type text}, {"Work_class", type text}, {"Education", type text}, {"Years_of_education", Int64.Type}, {"Marital_status", type text}, {"Occupation", type text}, {"Race", type text}, {"Gender", type text}, {"State", type text}, {"Capital_gain", Int64.Type}, {"Loan_amount", Int64.Type}, {"Capital_loss", Int64.Type}, {"Weekly_work_hours", Int64.Type}, {"Country/area_of_origin", type text}, {"Income", type text}, {"Current_mortgage", Int64.Type}, {"Student_debt", Int64.Type}, {"Number_of_homes_owned", Int64.Type}, {"Bank_balance", type number}, {"Loan_purpose", type text}, {"Credit_history", type number}, {"Past_bankruptcy", Int64.Type}, {"Loan_defaulted", type text}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Income_Sort", each if [Income] = "<50K" then 1
else if [Income] = "50K-250K" then 2
else if [Income] = ">250K" then 3
else 99),
    #"Sorted Rows" = Table.Sort(#"Added Custom",{{"Income_Sort", Order.Ascending}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Sorted Rows",{{"Income_Sort", Int64.Type}})
in
    #"Changed Type1"
