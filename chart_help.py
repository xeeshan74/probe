"""Plain-language help text for executive dashboard charts."""

from __future__ import annotations

import streamlit as st

SUMMARY_TABLE = (
    "At-a-glance counts for this assessment. **Assets in scope** are public hostnames we "
    "discovered from DNS and light wordlist checks. **Findings** are individual security "
    "gaps we scored. **High / critical** counts findings rated high or critical severity. "
    "**Exposure score** is the sum of finding risk scores, capped at 100 — higher means "
    "more overall exposure, not necessarily an active breach."
)

EXPOSURE_SCORE = (
    "Your headline risk number for this domain (0–100). The needle shows where the total "
    "weighted finding score lands: green is lower exposure, yellow/orange is moderate, red "
    "is elevated. Use this in leadership summaries — then drill into severity and "
    "priority charts to see what is driving the score."
)

FINDINGS_BY_SEVERITY = (
    "How many findings fall into each severity band (Low → Critical). Taller bars mean more "
    "issues in that band. Percentages show each band’s share of all findings. Many low items "
    "can still add up; a single high or critical item usually deserves faster action."
)

SEVERITY_TREND = (
    "Whether findings lean toward lower or higher severity. The line runs from Low (left) to "
    "Critical (right). A **declining** trend means most items are lower severity; an "
    "**inclining** trend means more weight on the right (higher severity). The ratio summary "
    "compares lower-tier (Low+Medium) vs higher-tier (High+Critical) counts."
)

TOP_FINDINGS = (
    "What to fix first, ranked by **risk score** (severity × confidence weighting). Longer "
    "bars mean higher priority. Orange/red items are typically email or exposure issues; "
    "green items are often hardening gaps (e.g. missing headers). Start remediation at the top "
    "of this list for the biggest risk reduction."
)

TOP_FINDINGS_TABLE = (
    "Ranked list of the highest-scoring findings when a bar chart would not add clarity "
    "(very few findings or all the same score). **Risk score** combines severity and "
    "confidence — higher rank means address sooner."
)

RISK_BY_CATEGORY = (
    "Where exposure points come from by issue type: **Email** (SPF/DMARC), **TLS** "
    "(certificates and transport), **Headers** (HSTS and security headers), **Surface** "
    "(discovered hosts and exposed services). Longer bars show which area contributes most "
    "to the overall score — useful for assigning work to the right team."
)

CONFIDENCE_VS_SEVERITY = (
    "Each dot is one finding. **Severity** (horizontal) is how bad the issue could be; "
    "**Confidence** (vertical) is how sure we are from passive, outside-in checks. Larger "
    "dots have higher risk scores. Prioritize items that are **high severity and high "
    "confidence** (upper right). Lower confidence may need manual validation before action."
)


def chart_help(text: str) -> None:
    """Render a help paragraph under a chart."""
    st.caption(text)
