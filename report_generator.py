"""Markdown / HTML-ish report text from stored findings."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional

import fitz
from PIL import Image, ImageDraw, ImageFont

from storage import get_assessment, list_assets, list_findings

from markdown_pdf import MarkdownPdf, Section

def convert_markdown_to_pdf(assessment_id: str, logo_path: Optional[str] = None) -> bytes:

    # If no logo_path provided, prefer a PNG logo asset first and fall back to the SVG file.
    if not logo_path:
        default_png = Path(__file__).resolve().parent / "assets" / "berkeley.png"
        default_svg = Path(__file__).resolve().parent / "assets" / "berkeley.svg"
        if default_png.exists():
            logo_path = str(default_png)
        elif default_svg.exists():
            logo_path = str(default_svg)

    markdown_content = build_markdown_report(assessment_id)

    # 2. Initialize the PDF builder
    pdf = MarkdownPdf()

    # 3. Add the content as a document section
    pdf.add_section(Section(markdown_content))

    # 4. If a logo exists, insert it into the generated PDF directly.
    if logo_path:
        p = Path(logo_path)
        if p.exists() and p.is_file():
            image_bytes: Optional[bytes] = None
            if p.suffix.lower() == ".svg":
                try:
                    import cairosvg

                    image_bytes = cairosvg.svg2png(bytestring=p.read_bytes(), dpi=200)
                except Exception:
                    image_bytes = None

            if not image_bytes:
                if p.suffix.lower() == ".svg":
                    img = Image.new("RGBA", (400, 120), "#003262")
                    draw = ImageDraw.Draw(img)
                    draw.rounded_rectangle((10, 10, 390, 110), radius=8, fill="#003262", outline="#FDB515", width=3)
                    try:
                        font = ImageFont.load_default()
                    except Exception:
                        font = None
                    if font is not None:
                        draw.text((60, 42), "BERKELEY", fill="#FDB515", font=font)
                    else:
                        draw.text((60, 42), "BERKELEY", fill="#FDB515")
                    output_img = BytesIO()
                    img.save(output_img, format="PNG")
                    image_bytes = output_img.getvalue()
                else:
                    image_bytes = p.read_bytes()

            if image_bytes:
                buffer = BytesIO()
                pdf.save(buffer)
                doc = fitz.open("pdf", buffer)
                page = doc[0]
                rect = fitz.Rect(430, 20, 560, 90)
                page.insert_image(rect, stream=image_bytes)
                output = BytesIO()
                doc.save(output)
                doc.close()
                return output.getvalue()

    buffer = BytesIO()
    pdf.save(buffer)

    return buffer.getvalue()


def build_markdown_report(assessment_id: str) -> str:
    a = get_assessment(assessment_id)
    if not a:
        return "# Error\nAssessment not found."
    findings = list_findings(assessment_id)
    assets = list_assets(assessment_id)

    lines: List[str] = [
        f"# PROBE Outside-In Exposure Report",
        f"",
        f"**Organization:** {a.company_name}",
        f"**Primary domain:** {a.primary_domain}",
        f"**Assessment:** {a.assessment_name or '—'}",
        f"**Date:** {a.assessment_date or a.created_at.date().isoformat()}",
        f"",
        f"## Executive summary",
        f"",
        f"PROBE identified **{len(assets)}** public-facing hostnames in scope for this pass and **{len(findings)}** findings from non-intrusive checks.",
        f"",
        f"> This assessment is an outside-in exposure review based on safe public checks. "
        f"It does not perform exploitation, authenticated testing, or internal network assessment.",
        f"",
        f"## Top findings",
        f"",
    ]
    for i, f in enumerate(findings[:10], start=1):
        lines.append(
            f"{i}. **{f['title']}** ({f['hostname']}) — *{f['severity']}* / confidence *{f['confidence']}*"
        )
        lines.append(f"   - {f['business_impact']}")
        lines.append("")

    lines.append("## Technical appendix (abbreviated)")
    lines.append("")
    for f in findings:
        lines.append(f"### {f['title']}")
        lines.append(f"- **Asset:** `{f['hostname']}`")
        lines.append(f"- **Severity:** {f['severity']} | **Score:** {f['risk_score']}")
        lines.append(f"- **Evidence:** {f['technical_evidence']}")
        lines.append(f"- **Recommendation:** {f['recommended_action']}")
        lines.append("")

    return "\n".join(lines)
