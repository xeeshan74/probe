"""Map observations to findings and weighted scores (spec §11)."""

from __future__ import annotations

import uuid
from typing import List

from models import Finding, FindingConfidence, FindingSeverity


def severity_from_points(points: int) -> str:
    if points <= 20:
        return FindingSeverity.LOW.value
    if points <= 50:
        return FindingSeverity.MEDIUM.value
    if points <= 75:
        return FindingSeverity.HIGH.value
    return FindingSeverity.CRITICAL.value


REQUIRED_HEADERS = [
    "strict-transport-security",
    "content-security-policy",
    "x-frame-options",
    "x-content-type-options",
    "referrer-policy",
]


def findings_from_tls(
    asset_id: str,
    hostname: str,
    days_to_expiry: int | None,
    tls_error: str | None,
) -> List[Finding]:
    out: List[Finding] = []
    if tls_error:
        return out
    if days_to_expiry is None:
        return out
    if days_to_expiry < 0:
        out.append(
            Finding(
                finding_id="",
                asset_id=asset_id,
                title="Expired TLS certificate",
                severity=FindingSeverity.HIGH.value,
                confidence=FindingConfidence.HIGH.value,
                risk_score=20,
                business_impact="A public TLS certificate is expired, which can break access and erode trust.",
                technical_evidence=f"Host {hostname}: certificate notAfter is in the past.",
                recommended_action="Renew or replace the certificate immediately.",
                category="tls",
            )
        )
    elif days_to_expiry <= 30:
        out.append(
            Finding(
                finding_id="",
                asset_id=asset_id,
                title="TLS certificate expiring within 30 days",
                severity=FindingSeverity.MEDIUM.value,
                confidence=FindingConfidence.HIGH.value,
                risk_score=15,
                business_impact="Certificate renewal is due soon; lapse can cause outages.",
                technical_evidence=f"Host {hostname}: expires in {days_to_expiry} days.",
                recommended_action="Renew the certificate before expiry.",
                category="tls",
            )
        )
    elif days_to_expiry <= 60:
        out.append(
            Finding(
                finding_id="",
                asset_id=asset_id,
                title="TLS certificate expiring within 60 days",
                severity=FindingSeverity.LOW.value,
                confidence=FindingConfidence.HIGH.value,
                risk_score=5,
                business_impact="Plan renewal to avoid last-minute outages.",
                technical_evidence=f"Host {hostname}: expires in {days_to_expiry} days.",
                recommended_action="Schedule certificate renewal.",
                category="tls",
            )
        )
    return out


def findings_from_headers(asset_id: str, hostname: str, headers: dict) -> List[Finding]:
    missing = [h for h in REQUIRED_HEADERS if h not in headers]
    out: List[Finding] = []
    if "strict-transport-security" not in headers:
        out.append(
            Finding(
                finding_id="",
                asset_id=asset_id,
                title="Missing Strict-Transport-Security (HSTS)",
                severity=FindingSeverity.LOW.value,
                confidence=FindingConfidence.MEDIUM.value,
                risk_score=10,
                business_impact="Users may be downgraded to insecure HTTP in some scenarios.",
                technical_evidence=f"{hostname}: HSTS header not present on HTTPS response.",
                recommended_action="Enable HSTS with an appropriate max-age for production sites.",
                category="headers",
            )
        )
    non_hsts = [h for h in missing if h != "strict-transport-security"]
    if len(non_hsts) >= 2:
        out.append(
            Finding(
                finding_id="",
                asset_id=asset_id,
                title="Multiple security headers missing",
                severity=FindingSeverity.LOW.value,
                confidence=FindingConfidence.MEDIUM.value,
                risk_score=10,
                business_impact="Several baseline hardening headers are absent.",
                technical_evidence=f"{hostname}: missing {', '.join(non_hsts)}.",
                recommended_action="Add CSP, frame protections, MIME sniffing protection, and Referrer-Policy as appropriate.",
                category="headers",
            )
        )
    return out


def findings_from_classification(
    asset_id: str, hostname: str, asset_type: str, confidence: str
) -> List[Finding]:
    if asset_type == "unknown":
        return []
    points = 0
    title = "Notable public-facing asset pattern"
    business = "Hostname or page content matches patterns often used for sensitive entry points."
    if asset_type == "admin":
        points = 30
        title = "Possible admin portal exposed"
        business = "An administrative-style hostname or page is reachable from the internet."
    elif asset_type == "vpn":
        points = 30
        title = "Possible VPN / remote access portal"
        business = "Remote access entry points are high-value targets for credential attacks."
    elif asset_type == "login":
        points = 25
        title = "Possible login / SSO surface"
        business = "Authentication entry points warrant strong controls (MFA, monitoring)."
    elif asset_type == "api":
        points = 10
        title = "Public API endpoint signal"
        business = "APIs may expose organization data if not properly authenticated and rate-limited."
    elif asset_type == "dev_staging":
        points = 20
        title = "Possible dev / staging / test system public"
        business = "Non-production systems often have weaker controls and should not be broadly exposed."
    elif asset_type == "sensitive_web":
        points = 15
        title = "Web asset with sensitive keywords"
        business = "Naming or content suggests elevated sensitivity; validate intent and controls."

    sev = severity_from_points(points)
    return [
        Finding(
            finding_id="",
            asset_id=asset_id,
            title=title,
            severity=sev,
            confidence=confidence,
            risk_score=min(100, points),
            business_impact=business,
            technical_evidence=f"Host {hostname}: classifier={asset_type}.",
            recommended_action="Confirm business need for public exposure, enforce MFA where applicable, and patch/monitor.",
            category="surface",
        )
    ]


def findings_from_email(asset_id: str, domain: str, posture) -> List[Finding]:  # noqa: ANN001
    out: List[Finding] = []
    if not posture.spf_present:
        out.append(
            Finding(
                finding_id="",
                asset_id=asset_id,
                title="No SPF record detected at apex",
                severity=FindingSeverity.MEDIUM.value,
                confidence=FindingConfidence.HIGH.value,
                risk_score=15,
                business_impact="Without SPF, receiving servers have weaker signals for authentic mail.",
                technical_evidence=f"No v=spf1 TXT at {domain}.",
                recommended_action="Publish an appropriate SPF TXT record aligned with sending infrastructure.",
                category="email",
            )
        )
    if not posture.dmarc_present:
        out.append(
            Finding(
                finding_id="",
                asset_id=asset_id,
                title="No DMARC record (_dmarc) detected",
                severity=FindingSeverity.HIGH.value,
                confidence=FindingConfidence.HIGH.value,
                risk_score=25,
                business_impact="Email spoofing protection is weak or incomplete without DMARC.",
                technical_evidence=f"No DMARC TXT at _dmarc.{domain}.",
                recommended_action="Publish a DMARC record and move policy toward quarantine/reject after testing.",
                category="email",
            )
        )
    elif posture.dmarc_policy in (None, "none"):
        out.append(
            Finding(
                finding_id="",
                asset_id=asset_id,
                title="DMARC present but not enforcing (p=none or unclear)",
                severity=FindingSeverity.MEDIUM.value,
                confidence=FindingConfidence.HIGH.value,
                risk_score=20,
                business_impact="Monitoring may exist, but spoofed messages may still be delivered.",
                technical_evidence=f"DMARC: {posture.dmarc_record[:500]}",
                recommended_action="Gradually tighten DMARC policy after alignment review.",
                category="email",
            )
        )
    return out


def new_finding_id() -> str:
    return f"find_{uuid.uuid4().hex}"
