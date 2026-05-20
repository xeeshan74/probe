"""Markdown / HTML-ish report text from stored findings."""

from __future__ import annotations

from typing import Any, Dict, List

from storage import get_assessment, list_assets, list_findings


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
