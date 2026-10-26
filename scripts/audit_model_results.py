"""Recompute aggregate classification metrics from transcribed report matrices.

These are checks of historical report evidence, not a model training run.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def metrics(counts: dict) -> dict:
    if set(counts) != {"tn", "fp", "fn", "tp"} or any(type(v) is not int or v < 0 for v in counts.values()):
        raise ValueError("Confusion counts must be four nonnegative integers: tn, fp, fn, tp")
    tn, fp, fn, tp = (counts[key] for key in ["tn", "fp", "fn", "tp"])
    total = tn + fp + fn + tp
    return {
        "n": total, "actual_default": tp + fn, "actual_fully_paid": tn + fp,
        "flagged": tp + fp,
        "accuracy": (tp + tn) / total if total else None,
        "precision": tp / (tp + fp) if tp + fp else None,
        "recall": tp / (tp + fn) if tp + fn else None,
        "f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None,
        "flag_rate": (tp + fp) / total if total else None,
        "specificity": tn / (tn + fp) if tn + fp else None,
    }


def reconcile(evidence: dict, source: dict) -> dict:
    models = []
    for model in evidence["models"]:
        computed = metrics(model["confusion_matrix"])
        if (computed["n"], computed["actual_default"], computed["actual_fully_paid"]) != (
            source["valid_label_rows"], source["default_rows"], source["fully_paid_rows"]
        ):
            raise ValueError("Report confusion matrix does not reconcile to the labelled cohort")
        for key, reported in model["reported_micro_percent"].items():
            if round(computed[key] * 100, 2) != reported:
                raise ValueError(f"Reported {key} differs from the confusion matrix")
        models.append({"name": model["name"], "confusion_matrix": model["confusion_matrix"], "recomputed": computed, "reported_micro_percent": model["reported_micro_percent"], "report_figure": model["report_figure"]})
    return {
        "source_report_sha256": evidence["source_report_sha256"],
        "source_csv_sha256": source["source_sha256"],
        "evidence_type": "Historical report screenshots; metrics recomputed from aggregate counts; no model rerun",
        "positive_class": "default (true / Loan_defaulted = 1)",
        "models": models,
        "baseline": {"name": "Predict every known outcome as fully paid", "accuracy": source["fully_paid_rows"] / source["valid_label_rows"], "recall": 0.0, "flagged": 0},
        "limitations": ["No prediction-level output or trained model supplied", "No reported ROC AUC, PR AUC or calibration results", "Saved process preprocessing precedes cross-validation", "Matching cohort totals do not establish exact run-to-file provenance"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "output/model-comparison.json")
    args = parser.parse_args()
    evidence = json.loads((ROOT / "evidence/reported-model-results.json").read_text())
    source = json.loads((ROOT / "analysis/source-audit.json").read_text())
    result = reconcile(evidence, source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print("Reconciled both reported model matrices to 9,998 known outcomes and recomputed metrics.")
