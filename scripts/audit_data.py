"""Reconcile a loan case CSV without exporting customer-level records.

This is an October 2026 portfolio extension, separate from the original
Power BI and RapidMiner work. Uses Python's standard library only.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path

FIELDS = (
    "Customer_id Age Work_class Loan_amount Education Years_of_education "
    "Marital_status Occupation Race Gender State Capital_gain Capital_loss "
    "Weekly_work_hours Country/area_of_origin Income Current_mortgage "
    "Student_debt Number_of_homes_owned Bank_balance Loan_purpose "
    "Credit_history Past_bankruptcy Loan_defaulted"
).split()


def read_csv(path: Path) -> tuple[list[dict[str, str]], str]:
    raw = path.read_bytes()
    try:
        decoded, encoding = raw.decode("utf-8-sig"), "utf-8-sig"
    except UnicodeDecodeError:
        decoded, encoding = raw.decode("cp1252"), "cp1252"
    reader = csv.DictReader(io.StringIO(decoded, newline=""))
    if reader.fieldnames != FIELDS:
        raise ValueError("CSV columns or column order do not match the documented case schema")
    rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError("CSV contains rows with too many or too few fields")
    return rows, encoding


def audit(rows: list[dict[str, str]]) -> dict:
    labels = Counter(row["Loan_defaulted"].strip() for row in rows)
    known = labels["0"] + labels["1"]
    defaults = labels["1"]
    ids = Counter(row["Customer_id"].strip() for row in rows)
    return {
        "total_rows": len(rows),
        "columns": len(FIELDS),
        "valid_label_rows": known,
        "fully_paid_rows": labels["0"],
        "default_rows": defaults,
        "missing_label_rows": labels[""],
        "invalid_label_rows": sum(v for k, v in labels.items() if k not in {"", "0", "1"}),
        "default_rate_known": defaults / known if known else None,
        "majority_class_accuracy": max(labels["0"], defaults) / known if known else None,
        "empty_customer_ids": ids[""],
        "duplicate_customer_id_excess_rows": sum(n - 1 for k, n in ids.items() if k and n > 1),
        "missing_values": {
            column: {
                "blank": sum(not row[column].strip() for row in rows),
                "question_mark": sum(row[column].strip() == "?" for row in rows),
            }
            for column in FIELDS
            if any(row[column].strip() in {"", "?"} for row in rows)
        },
        "mortgage_student_debt_equal_rows": sum(
            row["Current_mortgage"].strip() == row["Student_debt"].strip() for row in rows
        ),
        "rate_definition": "Loan_defaulted = 1 / rows with Loan_defaulted exactly 0 or 1 after trimming",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows, encoding = read_csv(args.csv)
    result = audit(rows)
    result["source_sha256"] = hashlib.sha256(args.csv.read_bytes()).hexdigest()
    result["decoded_as"] = encoding
    content = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    print(content, end="")


if __name__ == "__main__":
    main()
