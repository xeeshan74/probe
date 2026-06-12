"""Vulnerability guide: finding types, use cases, and exploitation context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import streamlit as st


@dataclass(frozen=True)
class VulnHelpEntry:
    key: str
    title: str
    category: str
    what_it_means: str
    use_cases: str
    direct_exploitation: str
    indirect_exploitation: str
    remediation: str


HELP: Dict[str, VulnHelpEntry] = {
    "no_spf": VulnHelpEntry(
        key="no_spf",
        title="No SPF record detected at apex",
        category="Email",
        what_it_means=(
            "The domain has no SPF (Sender Policy Framework) TXT record listing which mail servers "
            "may send email as `@yourdomain.com`."
        ),
        use_cases=(
            "Receiving mail systems use SPF to check whether a message came from an authorized sender. "
            "PROBE flags this when no `v=spf1` record exists at the domain apex."
        ),
        direct_exploitation=(
            "SPF alone does not stop spoofing by itself — attackers can still forge the From address. "
            "Without SPF, receivers have **weaker signals** to reject obvious forgeries."
        ),
        indirect_exploitation=(
            "Combined with missing or weak DMARC, spoofed invoices, password resets, or CEO fraud "
            "emails are more likely to reach inboxes. Finance and HR teams may trust `@yourdomain.com` "
            "messages that never touched your real mail servers."
        ),
        remediation=(
            "Publish an SPF TXT record aligned with all legitimate senders (Google, Microsoft 365, "
            "marketing tools, payroll). Use `-all` or `~all` only after testing. Pair with DKIM and DMARC."
        ),
    ),
    "no_dmarc": VulnHelpEntry(
        key="no_dmarc",
        title="No DMARC record (_dmarc) detected",
        category="Email",
        what_it_means=(
            "There is no DMARC policy at `_dmarc.yourdomain.com`. DMARC tells receivers what to do "
            "when SPF/DKIM checks fail for mail claiming to be from your domain."
        ),
        use_cases=(
            "Executive reporting on email trust, BEC (business email compromise) risk, and compliance "
            "readiness. Common on domains that send mail but never finished email authentication rollout."
        ),
        direct_exploitation=(
            "An attacker sends email **From: billing@yourdomain.com** from their own infrastructure. "
            "Without DMARC, many providers still **deliver** the message — employees or customers act on it."
        ),
        indirect_exploitation=(
            "Brand damage, fraudulent wire transfers, credential harvesting via fake IT notices, and "
            "customer payment diversion. No website hack required — only DNS-level impersonation."
        ),
        remediation=(
            "Add `v=DMARC1; p=none; rua=mailto:...` to collect reports, fix SPF/DKIM alignment, then "
            "move to `p=quarantine` and eventually `p=reject`."
        ),
    ),
    "dmarc_none": VulnHelpEntry(
        key="dmarc_none",
        title="DMARC present but not enforcing (p=none or unclear)",
        category="Email",
        what_it_means=(
            "A DMARC record exists but policy is `p=none` (monitor only) or unclear — receivers are "
            "told to **watch** failures, not block or quarantine spoofed mail."
        ),
        use_cases=(
            "Organizations in DMARC rollout phase: collecting reports before enforcement. PROBE flags "
            "this because spoofed mail may still be delivered."
        ),
        direct_exploitation=(
            "Same as full spoofing: fake `@yourdomain.com` messages can land in inboxes because "
            "providers honor `p=none` and do not reject failing mail."
        ),
        indirect_exploitation=(
            "Invoice fraud, vendor payment redirection, and internal phishing using your domain letterhead. "
            "Monitoring without enforcement gives visibility but **not protection**."
        ),
        remediation=(
            "Review DMARC aggregate reports (`rua`), fix misaligned senders, then tighten to "
            "`p=quarantine` and `p=reject` when confident legitimate mail will pass."
        ),
    ),
    "missing_hsts": VulnHelpEntry(
        key="missing_hsts",
        title="Missing Strict-Transport-Security (HSTS)",
        category="Headers",
        what_it_means=(
            "The HTTPS response does not include `Strict-Transport-Security`, so browsers are not "
            "instructed to always use HTTPS for this host."
        ),
        use_cases=(
            "Web hardening assessments, especially for login or admin hosts accessed on corporate "
            "or public Wi‑Fi."
        ),
        direct_exploitation=(
            "On a **hostile network**, an attacker may attempt SSL stripping — tricking the browser "
            "into staying on HTTP so credentials travel in cleartext. HSTS blocks repeat HTTP use "
            "after the first good HTTPS visit."
        ),
        indirect_exploitation=(
            "Session cookies or passwords captured on coffee-shop Wi‑Fi; users following old `http://` "
            "links or bookmarks without automatic upgrade."
        ),
        remediation=(
            "Add `Strict-Transport-Security: max-age=31536000; includeSubDomains` (and consider HSTS "
            "preload after testing). Ensure all paths redirect to HTTPS first."
        ),
    ),
    "missing_headers": VulnHelpEntry(
        key="missing_headers",
        title="Multiple security headers missing",
        category="Headers",
        what_it_means=(
            "Several baseline browser security headers are absent: typically CSP, X-Frame-Options, "
            "X-Content-Type-Options, and/or Referrer-Policy."
        ),
        use_cases=(
            "Defense-in-depth review for any public web app, portal, or admin interface."
        ),
        direct_exploitation=(
            "**X-Frame-Options / CSP frame-ancestors:** clickjacking — your site embedded in a fake page. "
            "**CSP:** limits script injection impact if XSS exists. **X-Content-Type-Options:** MIME confusion "
            "attacks. **Referrer-Policy:** leaks sensitive URL paths to third parties."
        ),
        indirect_exploitation=(
            "Combined with any XSS, weak auth, or social engineering, missing headers make user "
            "takeover and fraud easier. On admin portals, clickjacking can trick privileged actions."
        ),
        remediation=(
            "Configure headers at CDN, load balancer, or web server. Tune CSP to your app — start report-only "
            "if needed. Deny framing on sensitive apps."
        ),
    ),
    "expired_tls": VulnHelpEntry(
        key="expired_tls",
        title="Expired TLS certificate",
        category="TLS",
        what_it_means="The server presents a TLS certificate whose validity period has ended.",
        use_cases="Outage prevention, customer trust, and compliance (PCI, SOC2) certificate management.",
        direct_exploitation=(
            "Browsers show security warnings; users may be trained to click through, enabling "
            "man-in-the-middle if they accept invalid certs."
        ),
        indirect_exploitation=(
            "Service outage, failed API integrations, broken customer portals, and reputational harm. "
            "Attackers may register look-alike domains while yours shows errors."
        ),
        remediation="Renew or replace the certificate immediately. Automate renewal (e.g. ACME/Let's Encrypt).",
    ),
    "tls_30d": VulnHelpEntry(
        key="tls_30d",
        title="TLS certificate expiring within 30 days",
        category="TLS",
        what_it_means="Certificate expires within 30 days — renewal is overdue for planning purposes.",
        use_cases="Operational risk tracking before hard outage.",
        direct_exploitation="Same as expired cert once the date passes.",
        indirect_exploitation="Emergency renewals cause downtime or misconfiguration under pressure.",
        remediation="Renew before expiry. Set monitoring alerts at 60/30/14 days.",
    ),
    "tls_60d": VulnHelpEntry(
        key="tls_60d",
        title="TLS certificate expiring within 60 days",
        category="TLS",
        what_it_means="Certificate expires within 60 days.",
        use_cases="Early warning for certificate lifecycle management.",
        direct_exploitation="None until expiry — this is a planning finding.",
        indirect_exploitation="Unplanned outage if renewal is missed.",
        remediation="Schedule renewal and validate automation.",
    ),
    "admin_portal": VulnHelpEntry(
        key="admin_portal",
        title="Possible admin portal exposed",
        category="Surface",
        what_it_means=(
            "A hostname or page looks like an administrative interface (e.g. `admin.`, admin UI text) "
            "and is reachable from the public internet."
        ),
        use_cases=(
            "Attack surface mapping, M&A due diligence, and prioritizing MFA/network controls on "
            "privileged entry points."
        ),
        direct_exploitation=(
            "Credential stuffing, password spraying, exploitation of known admin-panel CVEs, and "
            "brute-force against weak passwords if MFA is absent."
        ),
        indirect_exploitation=(
            "Full tenant or infrastructure compromise after credential theft; lateral movement from a "
            "single reused password. Often paired with missing headers or no WAF."
        ),
        remediation=(
            "Restrict by IP/VPN, enforce MFA, patch promptly, monitor failed logins, and confirm "
            "public exposure is intentional."
        ),
    ),
    "vpn_portal": VulnHelpEntry(
        key="vpn_portal",
        title="Possible VPN / remote access portal",
        category="Surface",
        what_it_means="Public-facing remote access (VPN, Citrix, RD Gateway, etc.) was detected.",
        use_cases="Remote workforce exposure reviews.",
        direct_exploitation=(
            "Targeted credential attacks, exploitation of VPN appliance vulnerabilities, and MFA fatigue."
        ),
        indirect_exploitation=(
            "Network-wide breach — attackers use VPN as front door to internal systems."
        ),
        remediation="MFA, patching, geo/IP restrictions, logging, and vendor security advisories.",
    ),
    "login_surface": VulnHelpEntry(
        key="login_surface",
        title="Possible login / SSO surface",
        category="Surface",
        what_it_means="Authentication or single sign-on entry point detected on a public host.",
        use_cases="Identity attack surface mapping.",
        direct_exploitation="Phishing, credential stuffing, session hijacking if cookies lack Secure/HttpOnly.",
        indirect_exploitation="Account takeover leading to data theft or fraud.",
        remediation="MFA, rate limiting, bot detection, modern SSO hardening, monitor impossible travel.",
    ),
    "api_signal": VulnHelpEntry(
        key="api_signal",
        title="Public API endpoint signal",
        category="Surface",
        what_it_means="Response or path suggests a public API (JSON, `/api`, OpenAPI hints).",
        use_cases="Shadow API and data exposure reviews.",
        direct_exploitation=(
            "Unauthenticated endpoints, broken object level authorization (BOLA/IDOR), excessive data "
            "in responses, missing rate limits."
        ),
        indirect_exploitation=(
            "Bulk data exfiltration, scraping, and abuse of business logic without traditional 'hacking'."
        ),
        remediation="Authentication, authorization tests, rate limits, API gateway, minimal response data.",
    ),
    "dev_staging": VulnHelpEntry(
        key="dev_staging",
        title="Possible dev / staging / test system public",
        category="Surface",
        what_it_means="Non-production naming (`dev`, `staging`, `test`) or content is internet-reachable.",
        use_cases="Prevent prod-data leaks from lower environments.",
        direct_exploitation=(
            "Default credentials, debug endpoints, verbose errors revealing stack traces, unpatched test stacks."
        ),
        indirect_exploitation=(
            "Pivot to production using shared secrets, VPN creds, or API keys found in staging."
        ),
        remediation="Remove public DNS, require VPN, never use production data in dev, separate credentials.",
    ),
    "sensitive_web": VulnHelpEntry(
        key="sensitive_web",
        title="Web asset with sensitive keywords",
        category="Surface",
        what_it_means="URL or page content suggests payroll, HR, finance, or similar sensitivity.",
        use_cases="Prioritize controls on likely high-impact apps.",
        direct_exploitation="Depends on app — often auth bypass or data exposure if poorly secured.",
        indirect_exploitation="Regulatory and privacy impact if PII or financial data is exposed.",
        remediation="Validate classification, apply appropriate access controls and monitoring.",
    ),
    "notable_asset": VulnHelpEntry(
        key="notable_asset",
        title="Notable public-facing asset pattern",
        category="Surface",
        what_it_means="Hostname or content matched a sensitive pattern but did not fit a specific class.",
        use_cases="Manual validation of unexpected public services.",
        direct_exploitation="Varies — treat as worth manual review.",
        indirect_exploitation="Unknown exposure may expand attack surface over time.",
        remediation="Confirm ownership, business need, and security baseline.",
    ),
}

# Map PROBE finding titles (substring match order matters — more specific first).
_TITLE_RULES: List[tuple[str, str]] = [
    ("DMARC present but not enforcing", "dmarc_none"),
    ("No DMARC record", "no_dmarc"),
    ("No SPF record", "no_spf"),
    ("Strict-Transport-Security", "missing_hsts"),
    ("Multiple security headers missing", "missing_headers"),
    ("Expired TLS certificate", "expired_tls"),
    ("expiring within 30 days", "tls_30d"),
    ("expiring within 60 days", "tls_60d"),
    ("admin portal exposed", "admin_portal"),
    ("VPN / remote access", "vpn_portal"),
    ("login / SSO", "login_surface"),
    ("API endpoint signal", "api_signal"),
    ("dev / staging", "dev_staging"),
    ("sensitive keywords", "sensitive_web"),
    ("Notable public-facing", "notable_asset"),
]


def resolve_help_key(finding_title: str) -> Optional[str]:
    title = (finding_title or "").strip()
    for fragment, key in _TITLE_RULES:
        if fragment.lower() in title.lower():
            return key
    return None


def help_keys_by_category() -> Dict[str, List[str]]:
    cats: Dict[str, List[str]] = {}
    for entry in HELP.values():
        cats.setdefault(entry.category, []).append(entry.key)
    for cat in cats:
        cats[cat] = sorted(cats[cat], key=lambda k: HELP[k].title)
    return dict(sorted(cats.items()))


def all_help_keys() -> List[str]:
    keys: List[str] = []
    for cat_keys in help_keys_by_category().values():
        keys.extend(cat_keys)
    return keys


def render_finding_help_detail(key: str, *, container=None) -> None:
    target = container if container is not None else st
    entry = HELP.get(key)
    if not entry:
        target.warning("No guide entry for this finding type yet.")
        return
    target.markdown(f"### {entry.title}")
    target.markdown(f"*Category:* {entry.category}")
    target.markdown(f"**What it means**  \n{entry.what_it_means}")
    target.markdown(f"**When PROBE reports this**  \n{entry.use_cases}")
    target.markdown(f"**Direct exploitation**  \n{entry.direct_exploitation}")
    target.markdown(f"**Indirect exploitation**  \n{entry.indirect_exploitation}")
    target.markdown(f"**Remediation**  \n{entry.remediation}")


def render_guide_tab(selected_key: Optional[str] = None) -> None:
    """Vulnerability guide tab: topic picker + detailed write-up."""
    st.subheader("Vulnerability guide")
    st.caption(
        "What PROBE findings mean, real-world use cases, and how issues can be exploited "
        "directly or indirectly — plus remediation guidance."
    )

    if selected_key and selected_key in HELP:
        st.session_state.vuln_help_key = selected_key

    pending = st.session_state.pop("guide_from_finding", None)
    if pending:
        st.info(f"From your assessment findings: **{pending}**")

    keys = all_help_keys()
    if not keys:
        st.warning("No guide topics loaded.")
        return

    categories = list(help_keys_by_category().keys())
    current = st.session_state.get("vuln_help_key")
    default_cat = HELP[current].category if current in HELP else categories[0]
    cat_index = categories.index(default_cat) if default_cat in categories else 0
    picked_category = st.selectbox("Category", categories, index=cat_index, key="guide_category")
    cat_keys = help_keys_by_category()[picked_category]

    if current not in cat_keys:
        current = cat_keys[0]
        st.session_state.vuln_help_key = current

    idx = cat_keys.index(current) if current in cat_keys else 0
    picked = st.selectbox(
        "Topic",
        cat_keys,
        index=idx,
        format_func=lambda k: HELP[k].title,
        key="guide_topic_select",
    )
    st.session_state.vuln_help_key = picked

    with st.container(border=True):
        render_finding_help_detail(picked)
