"""Create SVG source diagrams from committed aggregate and report metadata."""
import html
import json
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def text(x, y, value, size=16, fill="#1c3047", weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}">{html.escape(str(value))}</text>'


def rect(x, y, w, h, fill="#ffffff", stroke="#dce5ef", radius=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def svg(width, height, content, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}"><title>{html.escape(title)}</title><g font-family="Arial, Helvetica, sans-serif">{content}</g></svg>\n'


def overview():
    audit = json.loads((ROOT / "analysis/source-audit.json").read_text())
    content = rect(0, 0, 1200, 560, "#f3f6fa", "#f3f6fa", 0)
    content += rect(0, 0, 1200, 150, "#102b46", "#102b46", 0)
    content += text(40, 45, "LOAN DEFAULT ANALYTICS", 15, "#72d5ca", 700)
    content += text(40, 88, "From borrower data to reviewable risk analysis", 30, "#ffffff", 700)
    content += text(40, 121, "Power BI / DAX / Power Query / RapidMiner / Python", 17, "#d7e3ef")
    cards = [("Case records", f'{audit["total_rows"]:,}'), ("Known outcomes", f'{audit["valid_label_rows"]:,}'), ("Observed defaults", f'{audit["default_rows"]:,}'), ("Default rate on known outcomes", f'{audit["default_rate_known"]:.2%}')]
    for i, (label, value) in enumerate(cards):
        x = 40 + i * 285
        content += rect(x, 174, 265, 98)
        content += text(x + 18, 203, label, 13, "#536c83")
        content += text(x + 18, 246, value, 32, "#102b46", 700)
    content += text(40, 313, "Outcome reconciliation", 19, weight=700)
    content += text(40, 338, "Unknown outcomes stay outside the measured default-rate denominator.", 15, "#536c83")
    x = 40
    for n, color in [(audit["fully_paid_rows"], "#157f82"), (audit["default_rows"], "#d55c42"), (audit["missing_label_rows"] + audit["invalid_label_rows"], "#a5b4c5")]:
        w = n / audit["total_rows"] * 1120
        content += rect(round(x, 2), 357, round(w, 2), 26, color, color, 0)
        x += w
    for x, label, color in [(40, "8,937 fully paid", "#157f82"), (380, "1,061 default", "#b64a34"), (690, "5,001 missing / malformed", "#536c83")]:
        content += text(x, 410, label, 16, color, 700)
    for i, (name, detail) in enumerate([("Validate", "Labels and missing data"), ("Explore", "Two Power BI pages"), ("Model", "Cross-validation workflow"), ("Review", "Code, tests and limitations")]):
        x = 40 + i * 285
        content += rect(x, 441, 265, 75, "#e7eef6", "#e7eef6")
        content += text(x + 16, 468, name, 18, weight=700)
        content += text(x + 16, 493, detail, 14, "#536c83")
    content += text(40, 541, "Academic case / Aggregate audit results / No model performance claim", 13, "#536c83")
    (ASSETS / "project-overview.svg").write_text(svg(1200, 560, content, "Loan default analytics overview"))


def maps():
    metadata = json.loads((ROOT / "powerbi/report-metadata.json").read_text())
    for index, page in enumerate(metadata["pages"]):
        content = rect(0, 0, 1280, 840, "#f3f6fa", "#f3f6fa", 0)
        content += text(24, 35, page["name"], 25, weight=700)
        content += text(24, 63, "Design map from saved visual metadata. Not a Power BI screenshot. Decoration omitted.", 16, "#536c83")
        for visual in page["visuals"]:
            kind = visual["type"]
            if kind in {"shape", "image", "textbox", "actionButton"}:
                continue
            b = visual["bounds"]
            x, y, w, h = b["x"], b["y"] + 90, b["width"], b["height"]
            content += rect(x, y, w, h, "#e5f2f0" if kind == "card" else "#ffffff", "#a4bdcb", 6)
            font = 12 if w < 180 else 14
            fields = list(dict.fromkeys(f.replace("Loan.", "") for values in visual["fields"].values() for f in values))
            title = visual["title"] or (fields[0].replace("_", " ") if fields else kind)
            char_width = max(9, int((w - 16) / (font * .56)))
            title_lines = textwrap.wrap(title, width=char_width)[:3]
            line_y = y + 18
            for line in title_lines:
                if line_y < y + h - 5:
                    content += text(x + 8, line_y, line, font, weight=700)
                line_y += 16
            if kind == "card":
                continue
            detail = kind + " | " + ", ".join(fields)
            for line in textwrap.wrap(detail, width=char_width)[:6]:
                if line_y < y + h - 7:
                    content += text(x + 8, line_y + 3, line, font - 1, "#536c83")
                line_y += 15
        content += text(24, 824, "Source: Report/Layout inside the local PBIX. Field bindings are preserved for review.", 13, "#536c83")
        name = "customer-profile-map.svg" if index == 0 else "financial-risk-map.svg"
        (ASSETS / name).write_text(svg(1280, 840, content, page["name"] + " report design map"))


def income_chart():
    result = json.loads((ROOT / "analysis/income-segments.json").read_text())
    content = rect(0, 0, 1200, 390, "#f3f6fa", "#f3f6fa", 0)
    content += text(40, 42, "Observed default rate by income category", 26, weight=700)
    content += text(40, 72, "Recomputed from the supplied CSV / Valid labels only / October 2026 portfolio analysis", 16, "#536c83")
    order = {"<50K": 0, "50K\u2013250K": 1, ">250K": 2}
    for index, segment in enumerate(sorted(result["segments"], key=lambda s: order[s["income"]])):
        y = 116 + index * 77
        small = segment["known_customers"] < 100
        color = "#aa7429" if small else "#157f82"
        content += text(40, y + 18, segment["income"], 20, weight=700)
        content += text(40, y + 43, f'{segment["defaults"]:,} defaults / {segment["known_customers"]:,} known outcomes', 14, "#536c83")
        content += rect(365, y, 650, 38, "#e1e9f0", "#e1e9f0", 4)
        content += rect(365, y, round(segment["default_rate"] / .30 * 650, 2), 38, color, color, 4)
        content += text(1040, y + 26, f'{segment["default_rate"]:.2%}', 22, color, 700)
    content += text(40, 355, "The <50K group has only 40 known outcomes. Show denominators and investigate uncertainty before acting.", 15, "#536c83")
    content += text(40, 379, "These are unadjusted associations in a teaching case, not model performance or evidence of causality.", 13, "#536c83")
    (ASSETS / "income-comparison.svg").write_text(svg(1200, 390, content, "Observed income-category default rates and sample sizes"))


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    overview()
    maps()
    income_chart()
    print("Rendered four SVG figures from committed aggregate results and metadata.")
