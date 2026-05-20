"""Orchestrates discovery, checks, scoring, and persistence."""

from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

from authorization import generate_verification_token, verification_record_value, verify_dns_txt
from config import CONFIG
from discovery import discover_hostnames
from dns_utils import normalize_domain
from email_checks import analyze_email_security
from models import Asset, Assessment, AssessmentStatus, AuthMethod, Observation
from page_classifier import classify_asset
from risk_engine import (
    findings_from_classification,
    findings_from_email,
    findings_from_headers,
    findings_from_tls,
    new_finding_id,
)
from storage import (
    clear_assessment_results,
    get_assessment,
    insert_assessment,
    insert_asset,
    insert_finding,
    insert_observation,
    update_assessment_auth,
    update_assessment_status,
    update_asset_classification,
)
from tls_checks import check_tls
from web_checks import check_https_and_http


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def create_assessment(
    company_name: str,
    primary_domain: str,
    assessment_name: str = "",
    assessment_date: str = "",
    business_owner: str = "",
    public_ips: str = "",
) -> Tuple[Assessment, str]:
    """Creates assessment in pending_authorization state. Returns (assessment, txt_instruction)."""
    aid = f"asm_{uuid.uuid4().hex[:10]}"
    token = generate_verification_token()
    domain = normalize_domain(primary_domain)
    a = Assessment(
        assessment_id=aid,
        company_name=company_name.strip(),
        primary_domain=domain,
        created_at=_utcnow(),
        status=AssessmentStatus.PENDING_AUTHORIZATION,
        authorization_method=AuthMethod.DNS_TXT,
        verification_token=token,
        public_ips=public_ips.strip(),
        assessment_name=assessment_name.strip(),
        business_owner=business_owner.strip(),
        assessment_date=assessment_date.strip(),
    )
    insert_assessment(a)
    instr = (
        f"Add a DNS TXT record at **{domain}** with value: `{verification_record_value(token)}` "
        f"then click **Verify DNS**."
    )
    return a, instr


def authorize_demo(assessment_id: str) -> Tuple[bool, str]:
    if not CONFIG.safety.allow_demo_mode:
        return False, "Demo mode disabled in configuration."
    a = get_assessment(assessment_id)
    if not a:
        return False, "Assessment not found."
    update_assessment_auth(assessment_id, AuthMethod.DEMO_MODE, AssessmentStatus.AUTHORIZED)
    return True, "Demo authorization applied (not for production)."


def authorize_manual(assessment_id: str) -> Tuple[bool, str]:
    a = get_assessment(assessment_id)
    if not a:
        return False, "Assessment not found."
    update_assessment_auth(assessment_id, AuthMethod.MANUAL, AssessmentStatus.AUTHORIZED)
    return True, "Manual authorization recorded (classroom / non-production only)."


def authorize_dns(assessment_id: str) -> Tuple[bool, str]:
    a = get_assessment(assessment_id)
    if not a:
        return False, "Assessment not found."
    ok, msg = verify_dns_txt(a.primary_domain, a.verification_token)
    if not ok:
        return False, msg
    update_assessment_auth(assessment_id, AuthMethod.DNS_TXT, AssessmentStatus.AUTHORIZED)
    return True, msg


def _days_to_expiry(not_after) -> Optional[int]:  # noqa: ANN001
    if not_after is None:
        return None
    delta = not_after - _utcnow()
    return int(delta.total_seconds() // 86400)


def run_assessment(assessment_id: str) -> tuple[bool, str]:
    a = get_assessment(assessment_id)
    if not a:
        return False, "Assessment not found."
    if a.status not in (
        AssessmentStatus.AUTHORIZED,
        AssessmentStatus.COMPLETE,
        AssessmentStatus.FAILED,
    ):
        return False, "Assessment is not authorized yet."

    update_assessment_status(assessment_id, AssessmentStatus.RUNNING)
    clear_assessment_results(assessment_id)

    try:
        domain = normalize_domain(a.primary_domain)
        discoveries = discover_hostnames(domain)

        hostname_to_id: Dict[str, str] = {}
        apex_asset_id: Optional[str] = None

        for d in discoveries:
            aid = f"ast_{uuid.uuid4().hex[:12]}"
            hostname_to_id[d.hostname] = aid
            if d.hostname == domain:
                apex_asset_id = aid
            ip = d.ip_addresses[0] if d.ip_addresses else ""
            insert_asset(
                Asset(
                    asset_id=aid,
                    assessment_id=assessment_id,
                    hostname=d.hostname,
                    ip_address=ip,
                    source=d.source,
                    asset_type="unknown",
                    confidence=d.confidence,
                )
            )

        if apex_asset_id is None:
            update_assessment_status(assessment_id, AssessmentStatus.FAILED)
            return False, "Discovery failed to include apex domain."

        posture = analyze_email_security(domain)
        for f in findings_from_email(apex_asset_id, domain, posture):
            f.finding_id = new_finding_id()
            insert_finding(f)

        delay = CONFIG.assessment.rate_limit_delay_seconds

        for d in discoveries:
            aid = hostname_to_id[d.hostname]
            hostname = d.hostname

            tls = check_tls(hostname, 443)
            days = _days_to_expiry(tls.not_after) if not tls.error else None
            for f in findings_from_tls(aid, hostname, days, tls.error):
                f.finding_id = new_finding_id()
                insert_finding(f)

            insert_observation(
                Observation(
                    observation_id=f"obs_{uuid.uuid4().hex[:10]}",
                    asset_id=aid,
                    observation_type="tls",
                    raw_value=(tls.error or str(tls.not_after)),
                    normalized_value="ok" if not tls.error else "error",
                    created_at=_utcnow(),
                )
            )

            web_results = check_https_and_http(hostname)
            time.sleep(delay)

            best = None
            for wr in web_results:
                if wr.error:
                    continue
                if wr.status_code and wr.final_url.startswith("https"):
                    best = wr
                    break
            if best is None:
                for wr in web_results:
                    if not wr.error and wr.status_code:
                        best = wr
                        break

            headers = best.headers if best else {}
            title = best.title if best else ""
            final_url = best.final_url if best else f"https://{hostname}/"

            if (
                best
                and best.final_url.startswith("https")
                and best.status_code
                and 200 <= best.status_code < 600
            ):
                for f in findings_from_headers(aid, hostname, headers):
                    f.finding_id = new_finding_id()
                    insert_finding(f)

            asset_type, cls_conf = classify_asset(hostname, title, final_url)
            update_asset_classification(aid, asset_type, cls_conf)

            for f in findings_from_classification(aid, hostname, asset_type, cls_conf):
                f.finding_id = new_finding_id()
                insert_finding(f)

            insert_observation(
                Observation(
                    observation_id=f"obs_{uuid.uuid4().hex[:10]}",
                    asset_id=aid,
                    observation_type="http_summary",
                    raw_value=f"status={getattr(best, 'status_code', None)} title={title[:200]}",
                    normalized_value=asset_type,
                    created_at=_utcnow(),
                )
            )

        update_assessment_status(assessment_id, AssessmentStatus.COMPLETE)
        return True, "Assessment complete."
    except Exception as exc:  # noqa: BLE001
        update_assessment_status(assessment_id, AssessmentStatus.FAILED)
        return False, f"Assessment failed: {exc}"
