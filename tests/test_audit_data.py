"""Behaviour tests for the portfolio audit, using artificial records only."""
import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("audit_data", ROOT / "scripts/audit_data.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def row(label="0", identifier="DEMO-1", **changes):
    record = {key: "0" for key in module.FIELDS}
    record.update(Customer_id=identifier, Loan_defaulted=label)
    record.update(changes)
    return record


class AuditTests(unittest.TestCase):
    def test_unknown_and_corrupt_labels_do_not_dilute_default_rate(self):
        result = module.audit([row("1"), row("0"), row(""), row("0+T4261")])
        self.assertEqual(result["valid_label_rows"], 2)
        self.assertEqual(result["missing_label_rows"], 1)
        self.assertEqual(result["invalid_label_rows"], 1)
        self.assertEqual(result["default_rate_known"], .5)

    def test_unlabelled_population_has_no_measured_rate(self):
        result = module.audit([row("")])
        self.assertIsNone(result["default_rate_known"])
        self.assertIsNone(result["majority_class_accuracy"])

    def test_observed_zero_defaults_is_zero(self):
        self.assertEqual(module.audit([row("0")])["default_rate_known"], 0)

    def test_missing_markers_are_counted_separately(self):
        result = module.audit([row(Work_class="?"), row(Work_class="  ")])
        self.assertEqual(result["missing_values"]["Work_class"], {"blank": 1, "question_mark": 1})

    def test_duplicate_ids_and_empty_ids_are_distinct(self):
        result = module.audit([row(identifier="A"), row(identifier="A"), row(identifier="")])
        self.assertEqual(result["duplicate_customer_id_excess_rows"], 1)
        self.assertEqual(result["empty_customer_ids"], 1)

    def test_equal_debt_flags_are_measured_not_assumed(self):
        result = module.audit([row(), row(Current_mortgage="1", Student_debt="0")])
        self.assertEqual(result["mortgage_student_debt_equal_rows"], 1)

    def test_cp1252_income_en_dash_survives_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.csv"
            with path.open("w", encoding="cp1252", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=module.FIELDS)
                writer.writeheader()
                writer.writerow(row(Income="50K\u2013250K"))
            records, encoding = module.read_csv(path)
            self.assertEqual(encoding, "cp1252")
            self.assertEqual(records[0]["Income"], "50K\u2013250K")

    def test_invalid_schema_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.csv"
            path.write_text("Customer_id,Loan_defaulted\nA,0\n")
            with self.assertRaises(ValueError):
                module.read_csv(path)

    def test_ragged_rows_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.csv"
            path.write_text(",".join(module.FIELDS) + "\nA,0\n")
            with self.assertRaises(ValueError):
                module.read_csv(path)

    def test_empty_population_has_no_rate(self):
        result = module.audit([])
        self.assertEqual(result["total_rows"], 0)
        self.assertIsNone(result["default_rate_known"])


if __name__ == "__main__":
    unittest.main()
