"""Check public artifacts, arithmetic consistency and the synthetic example."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

from audit_data import audit, read_csv

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    toplevel = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=ROOT).decode().strip()
    require(Path(toplevel).resolve() == ROOT.resolve(), "Run verification inside this portfolio's own Git checkout")
    public = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
    ).decode().split("\0")
    files = sorted({name for name in public if name})
    require(bool(files), "No public files found")
    for name in files:
        path = Path(name)
        require(not name.startswith("private/"), f"Private file selected: {name}")
        require(path.suffix.lower() not in {".pbix", ".docx", ".pdf"}, f"Original binary selected: {name}")
        require(":Zone.Identifier" not in name, f"Download metadata selected: {name}")
        require(path.suffix.lower() != ".csv" or name == "data/demo/loan_demo.csv", f"Unexpected CSV selected: {name}")
        if path.suffix.lower() in {".md", ".py", ".pq", ".json", ".dax", ".rmp", ".svg", ".yml"}:
            content = (ROOT / path).read_text(encoding="utf-8")
            mac_home = "/" + "Users" + "/"
            windows_home = "C:" + chr(92) + "Users" + chr(92)
            require(mac_home not in content and windows_home not in content, f"Personal path found: {name}")
            if path.suffix == ".md":
                for target in re.findall(r"\]\(([^)]+)\)", content):
                    target = target.split("#")[0]
                    if target and "://" not in target:
                        require((ROOT / path.parent / target).exists(), f"Broken link in {name}: {target}")
    source = json.loads((ROOT / "analysis/source-audit.json").read_text())
    require(source["total_rows"] == source["valid_label_rows"] + source["missing_label_rows"] + source["invalid_label_rows"], "Source cohort does not reconcile")
    require(source["valid_label_rows"] == source["default_rows"] + source["fully_paid_rows"], "Known outcomes do not reconcile")
    require(abs(source["default_rate_known"] - source["default_rows"] / source["valid_label_rows"]) < 1e-12, "Wrong default-rate denominator")
    stored = json.loads((ROOT / "analysis/pbix-stored-summary.json").read_text())
    require(stored["row_count"] == source["total_rows"], "Stored PBIX / CSV totals differ")
    require(stored["outcomes"]["Default"] == source["default_rows"], "Stored PBIX defaults differ")
    require(stored["outcomes"]["Unknown"] == source["missing_label_rows"] + source["invalid_label_rows"], "Stored PBIX unknowns differ")
    segments = json.loads((ROOT / "analysis/income-segments.json").read_text())
    require(segments["source_sha256"] == source["source_sha256"], "Income source hash differs")
    require(sum(s["known_customers"] for s in segments["segments"]) == source["valid_label_rows"], "Income cohort does not reconcile")
    require(sum(s["defaults"] for s in segments["segments"]) == source["default_rows"], "Income defaults do not reconcile")
    demo_path = ROOT / "data/demo/loan_demo.csv"
    rows, encoding = read_csv(demo_path)
    require(all(r["Customer_id"].startswith("DEMO-") for r in rows), "Example contains non-demo IDs")
    expected = json.loads((ROOT / "data/expected/demo-audit.json").read_text())
    actual = audit(rows)
    actual.update(source_sha256=hashlib.sha256(demo_path.read_bytes()).hexdigest(), decoded_as=encoding)
    require(actual == expected, "Synthetic audit differs from committed expected output")
    metadata = json.loads((ROOT / "powerbi/report-metadata.json").read_text())
    require(metadata["measure_count"] == 12 and metadata["calculated_column_count"] == 13, "Unexpected model inventory")
    require(len(metadata["pages"]) == 2, "Expected two report pages")
    for path in (ROOT / "rapidminer").rglob("*.rmp"):
        process = ET.parse(path)
        require(process.getroot().tag == "process", f"Invalid RapidMiner XML: {path.name}")
    inventory = json.loads((ROOT / "evidence/input-inventory.json").read_text())
    for item in inventory["inputs"]:
        if item["public_copy"]:
            require(hashlib.sha256((ROOT / item["public_copy"]).read_bytes()).hexdigest() == item["sha256"], "Original workflow checksum differs")
    for path in (ROOT / "assets").glob("*.svg"):
        ET.parse(path)
    print(f"Verified {len(files)} public files: links, publication boundary, cohort reconciliation, original XML and synthetic expected output.")


if __name__ == "__main__":
    main()
