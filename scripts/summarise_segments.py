"""Publish aggregate income evidence, using the same labelled cohort as the audit."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from audit_data import read_csv


def summarise(path: Path) -> dict:
    rows, _ = read_csv(path)
    groups = defaultdict(lambda: {"known_customers": 0, "defaults": 0})
    for row in rows:
        label = row["Loan_defaulted"].strip()
        if label not in {"0", "1"}:
            continue
        group = groups[row["Income"].strip()]
        group["known_customers"] += 1
        group["defaults"] += label == "1"
    return {"source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "cohort": "Loan_defaulted exactly 0 or 1 after trimming", "segments": [{"income": name, **values, "default_rate": values["defaults"] / values["known_customers"]} for name, values in sorted(groups.items())]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summarise(args.csv), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
