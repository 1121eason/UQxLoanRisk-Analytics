"""Check important metric boundaries without training models."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_model_results import metrics, reconcile


class ModelMetricTests(unittest.TestCase):
    def test_all_negative_predictions_hide_defaults_behind_accuracy(self):
        result = metrics({"tn": 90, "fp": 0, "fn": 10, "tp": 0})
        self.assertEqual(result["accuracy"], .9)
        self.assertEqual(result["recall"], 0)
        self.assertIsNone(result["precision"])
        self.assertEqual(result["f1"], 0)

    def test_no_actual_positives_has_no_measured_recall(self):
        self.assertIsNone(metrics({"tn": 8, "fp": 2, "fn": 0, "tp": 0})["recall"])

    def test_invalid_counts_are_rejected(self):
        for counts in [{"tn": -1, "fp": 0, "fn": 0, "tp": 1}, {"tn": True, "fp": 0, "fn": 0, "tp": 1}]:
            with self.assertRaises(ValueError):
                metrics(counts)

    def test_mismatched_evaluation_population_is_rejected(self):
        evidence = {"models": [{"confusion_matrix": {"tn": 8, "fp": 1, "fn": 1, "tp": 0}}]}
        with self.assertRaisesRegex(ValueError, "cohort"):
            reconcile(evidence, {"valid_label_rows": 11, "default_rows": 1, "fully_paid_rows": 10})

    def test_rounded_reported_score_must_match_counts(self):
        evidence = {"models": [{"confusion_matrix": {"tn": 8, "fp": 1, "fn": 1, "tp": 0}, "reported_micro_percent": {"accuracy": 90}}]}
        with self.assertRaisesRegex(ValueError, "accuracy"):
            reconcile(evidence, {"valid_label_rows": 10, "default_rows": 1, "fully_paid_rows": 9})


if __name__ == "__main__":
    unittest.main()
