"""Extract reviewable logic and visual metadata; never write table records.

Optional dependency: pbixray==0.15.5. Install in your own environment.
The original M source path is replaced by CsvPath before writing.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile


def extract(pbix: Path, output: Path) -> None:
    from pbixray import PBIXRay

    model = PBIXRay(str(pbix))
    output.mkdir(parents=True, exist_ok=True)
    measures = model.dax_measures.to_dict(orient="records")
    columns = model.dax_columns.to_dict(orient="records")
    dax = ["// Extracted measure definitions. Run as a DAX query against the Loan model.", "DEFINE"]
    for item in measures:
        dax.append(f"    MEASURE '{item['TableName']}'[{item['Name']}] = {item['Expression'].strip()}\n")
    dax.append('EVALUATE ROW("Known customers", [Known_Customers], "Defaults", [Default_Customers], "Default rate", [Default_Rate])')
    (output / "measures.dax").write_text("\n".join(dax) + "\n", encoding="utf-8")
    (output / "calculated-columns.json").write_text(json.dumps(columns, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for item in model.power_query.to_dict(orient="records"):
        expression = re.sub(r'File\.Contents\("[^"\r\n]*"\)', 'File.Contents(CsvPath)', item["Expression"])
        (output / f"{item['TableName']}.original.pq").write_text(
            "// Original Power Query, with the local source path replaced by CsvPath.\n" + expression + "\n", encoding="utf-8"
        )
    with ZipFile(pbix) as archive:
        layout = json.loads(archive.read("Report/Layout").decode("utf-16-le"))
    pages = []
    for page in layout["sections"]:
        visuals = []
        for container in page.get("visualContainers", []):
            config = json.loads(container["config"])
            visual = config.get("singleVisual", {})
            title_objects = visual.get("vcObjects", {}).get("title", [])
            title = next((t.get("properties", {}).get("text", {}).get("expr", {}).get("Literal", {}).get("Value") for t in title_objects if "text" in t.get("properties", {})), None)
            visuals.append({
                "type": visual.get("visualType"),
                "title": title.strip("'") if title else None,
                "fields": {key: [f["queryRef"] for f in fields] for key, fields in visual.get("projections", {}).items()},
                "bounds": {key: container.get(key) for key in ["x", "y", "width", "height"]},
            })
        pages.append({"name": page["displayName"], "width": page["width"], "height": page["height"], "types": dict(Counter(v["type"] for v in visuals)), "visuals": visuals})
    result = {"source_sha256": hashlib.sha256(pbix.read_bytes()).hexdigest(), "extractor": "pbixray==0.15.5 + Python zipfile/json", "measure_count": len(measures), "calculated_column_count": len(columns), "pages": pages}
    (output / "report-metadata.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Extracted {len(measures)} measures, {len(columns)} calculated columns and {len(pages)} report pages; zero data rows exported.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pbix", type=Path)
    parser.add_argument("--output", type=Path, default=Path("powerbi"))
    args = parser.parse_args()
    extract(args.pbix, args.output)
