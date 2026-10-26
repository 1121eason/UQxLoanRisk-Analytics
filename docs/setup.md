# Setup and reproduction

## Public demo

Use Python 3.10 or newer. The audit and tests need only the standard library:

```bash
python scripts/audit_data.py data/demo/loan_demo.csv --output output/demo-audit.json
python -m unittest discover -s tests -v
python scripts/verify_repository.py
```

The 12-row example is artificial. `data/expected/demo-audit.json` records its expected result. It exercises label handling, missing markers and ID checks; it does not train or evaluate a classifier. GitHub Actions runs this same public path.

## Local original files

The original CSV, PBIX files, two RMP inputs, case brief, dictionary and rubric are retained under ignored `private/source/` in the author's local checkout. They are absent after cloning the public repository. There is no public data-download step. Obtain authorised source materials independently before using the native paths.

To check an authorised case CSV:

```bash
python scripts/audit_data.py /path/to/loan-data.csv --output output/source-audit.json
python scripts/summarise_segments.py /path/to/loan-data.csv --output output/income-segments.json
```

The reader attempts UTF-8 with BOM handling, then CP1252, requires the exact 24-field schema and rejects malformed row widths. JSON outputs contain aggregates and source hashes, not customer records. A source hash match establishes identical CSV bytes; aggregate similarity alone does not.

## Power BI path

1. Open the local PBIX in a compatible Power BI Desktop installation. The public clone does not contain it.
2. Inspect the original source and transformations before refreshing. Its stored M query points to a different local CSV filename variant and requests UTF-8. The separately supplied CSV was decoded as CP1252.
3. For a new review copy, define a text parameter `CsvPath` and inspect [`Loan.portable.pq`](../powerbi/Loan.portable.pq). It proposes a parameterised path and repaired income-sort comparison. Preserve the original PBIX for comparison.
4. Reconcile total/known/default counts, inspect categories and sort order, and verify each chart's numerator and denominator. Check the loan-amount column/line bindings described in [the review](powerbi.md).
5. Test slicer interactions and refresh behaviour in Desktop. Offline source extraction does not perform these checks.

The combined `measures.dax` file is a DAX **query** with query-scoped measure definitions and an `EVALUATE ROW` statement. It requires an existing compatible `Loan` model. The calculated-column JSON is a source register; create or edit individual model columns in the native tool rather than executing the JSON.

## RapidMiner path

1. Use a compatible RapidMiner / Altair AI Studio environment. The saved process declares version `10.3.001` and includes H2O and `blending` operators; compatibility is unverified here.
2. Import the authorised CSV into a local repository, with an explicit encoding and missing-value policy. Match the Retrieve operator's entry or update a copy to your local entry.
3. Open [`loan-default-original.rmp`](../rapidminer/loan-default-original.rmp), inspect its operators and validate repository metadata, target values and positive-label mapping.
4. Execute the saved logistic-regression path only after inspecting the known [evaluation limitations](modelling.md). Save performance and scored-fold outputs if a new run is conducted.
5. For comparison, use a separate process copy, disable/disconnect logistic regression and enable/connect random forest appropriately. Use identical folds and save both configurations and outputs. The disabled operator alone is not a completed comparison.

Do not use the archived alternative as a corrected pipeline; it contains the `age` operator's attribute-selection discrepancy. No native run is claimed in this repository.

## Optional PBIX code extraction

Use a separate environment if you want to repeat extraction:

```bash
python -m venv .venv
# Activate the environment using your platform's standard command.
python -m pip install -r requirements-extraction.txt
python scripts/extract_powerbi.py /path/to/local-report.pbix --output output/powerbi
python scripts/reconcile_pbix.py /path/to/local-report.pbix --output output/pbix-summary.json
```

This uses [PBIXRay](https://github.com/Hugoberry/pbixray) 0.15.5. The script exports expressions and visual metadata only, replacing the original file path with `CsvPath`. It does not refresh a model, evaluate DAX, render a dashboard or export table records. This optional dependency is not required by CI or the synthetic demo.
