"""Read local stored outcomes and write counts only; requires optional PBIXRay."""
import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    from pbixray import PBIXRay

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pbix", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    model = PBIXRay(str(args.pbix))
    table = model.get_table("Loan")
    result = {
        "pbix_sha256": hashlib.sha256(args.pbix.read_bytes()).hexdigest(),
        "row_count": len(table),
        "unique_customer_ids": int(table.Customer_id.nunique()),
        "outcomes": {str(k): int(v) for k, v in table.Loan_Outcome.value_counts(dropna=False).items()},
        "income_sort_counts": {str(k): int(v) for k, v in table.Income_Sort.value_counts(dropna=False).items()},
        "note": "Read-only decode of stored column values, not DAX execution or Power BI UI validation. The Power Query source filename differs from the separately supplied CSV.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print("Reconciled stored PBIX counts; zero customer records written.")


if __name__ == "__main__":
    main()
