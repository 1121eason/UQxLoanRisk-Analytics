"""Extract selected embedded report screenshots without publishing the PDF.

Optional dependency: pypdf. Page and image indexes refer to the supplied
15-page report. Source SHA-256 is required to avoid extracting another edition.
"""
import argparse
import hashlib
import json
from pathlib import Path

REPORT_SHA = "8f4185ae1bb024d37f9e9befbadee4ecd4bec051511696fc38d637a95115abbc"
SELECTION = [
    (3, 1, "customer-profile-dashboard.png", "Original customer profile dashboard"),
    (4, 1, "financial-risk-dashboard.png", "Original financial and credit risk dashboard"),
    (7, 1, "rapidminer-overall-process.png", "Historical overall preprocessing and cross-validation process"),
    (7, 2, "random-forest-cv.png", "Random forest enabled within cross-validation"),
    (8, 2, "logistic-regression-cv.png", "Logistic regression enabled within cross-validation"),
    (9, 1, "forest-tree-example.png", "Reported tree view; not global forest feature importance"),
    (9, 2, "logistic-coefficients-excerpt.png", "Partial logistic-regression coefficient table"),
    (11, 1, "random-forest-confusion-matrix.png", "Random forest historical confusion matrix"),
    (11, 2, "logistic-regression-confusion-matrix.png", "Logistic regression historical confusion matrix"),
]


def main():
    from pypdf import PdfReader
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--output", type=Path, default=Path("evidence/figures"))
    args = parser.parse_args()
    digest = hashlib.sha256(args.report.read_bytes()).hexdigest()
    if digest != REPORT_SHA:
        raise ValueError("Report checksum differs from the visually reviewed edition")
    reader = PdfReader(args.report)
    args.output.mkdir(parents=True, exist_ok=True)
    figures = []
    for page, image_index, name, caption in SELECTION:
        image = reader.pages[page - 1].images[image_index]
        if not image.name.lower().endswith(".png"):
            raise ValueError("Expected PNG report figure")
        data = image.data
        (args.output / name).write_bytes(data)
        figures.append({"file": name, "page": page, "page_image_index_zero_based": image_index, "caption": caption, "width": image.image.width, "height": image.image.height, "sha256": hashlib.sha256(data).hexdigest()})
    (args.output / "manifest.json").write_text(json.dumps({"source_file": "s4972258_report.pdf", "source_sha256": digest, "source_pages": len(reader.pages), "extraction": "Selected embedded PNG images; no generative edits or PDF page text published", "figures": figures}, indent=2) + "\n")
    print(f"Extracted {len(figures)} original screenshots; PDF remains local.")


if __name__ == "__main__":
    main()
