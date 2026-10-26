// October 2026 portfolio adaptation. Not executed in Power BI.
// Define a text parameter named CsvPath pointing to your authorised local CSV.
// Original DAX and original source files remain separate and unchanged.
let
    Source = Csv.Document(File.Contents(CsvPath), [Delimiter=",", Columns=24, Encoding=1252, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {
        {"Customer_id", type text}, {"Age", type text}, {"Work_class", type text},
        {"Loan_amount", Int64.Type}, {"Education", type text}, {"Years_of_education", Int64.Type},
        {"Marital_status", type text}, {"Occupation", type text}, {"Race", type text},
        {"Gender", type text}, {"State", type text}, {"Capital_gain", Int64.Type},
        {"Capital_loss", Int64.Type}, {"Weekly_work_hours", Int64.Type},
        {"Country/area_of_origin", type text}, {"Income", type text},
        {"Current_mortgage", Int64.Type}, {"Student_debt", Int64.Type},
        {"Number_of_homes_owned", Int64.Type}, {"Bank_balance", type number},
        {"Loan_purpose", type text}, {"Credit_history", type number},
        {"Past_bankruptcy", Int64.Type}, {"Loan_defaulted", type text}
    }),
    IncomeSort = Table.AddColumn(Typed, "Income_Sort", each
        let key = if [Income] = null then "" else Text.Replace(Text.Trim([Income]), "–", "-")
        in if key = "<50K" then 1 else if key = "50K-250K" then 2 else if key = ">250K" then 3 else 99,
        Int64.Type),
    Sorted = Table.Sort(IncomeSort, {{"Income_Sort", Order.Ascending}})
in
    Sorted
