# PROBE for Executives — Project Overview

**Public Risk Observation and Business Exposure Reporting**

---

## MVP statement

PROBE delivers **authorized** outside-in visibility on a **verified primary domain**. After DNS TXT verification (or clearly labeled demo/manual authorization for controlled environments), the tool runs **safe** public checks only: DNS-based discovery (apex plus a small wordlist), non-invasive HTTPS/HTTP metadata, TLS certificate health, SPF/DMARC, and basic security headers. It classifies surfaced assets with **confidence** separate from severity, applies a **transparent** risk-style score, and presents results in a **Streamlit executive dashboard** with charts plus a **downloadable Markdown report** (executive summary and technical appendix). It does not perform exploitation, authenticated testing, or internal scanning.

---

## Problem and benefit

Enterprises expose many hostnames, web applications, portals, and mail controls to the public internet. Security teams often have technical data (ports, CVEs, raw DNS), while executives need clear answers: what outsiders can see, what looks risky, whether email anti-spoofing is adequate, and what to prioritize.

PROBE closes that gap with **authorized, non-intrusive outside-in checks** and reporting that translates observations into **business risk**, **confidence**, and **actionable recommendations**. It improves leadership visibility and decision-making; it does **not** replace penetration testing or enterprise attack-surface management platforms.

---

## MVP outcomes (what the product delivers)

| Outcome | Description |
|---------|-------------|
| **Authorized assessment** | Domain control via DNS TXT token; demo and manual modes for lab use only. |
| **Asset discovery** | Public hostnames from apex resolution and a built-in subdomain wordlist. |
| **Safe external checks** | Reachability and metadata from HTTPS/HTTP GET; TLS expiry and certificate signals; SPF/DMARC; common security headers. |
| **Surface awareness** | Heuristic classification of likely login, admin, VPN, API, and dev/staging patterns. |
| **Risk communication** | Weighted findings with severity, confidence, business impact, evidence, and remediation text. |
| **Executive dashboard** | Aggregate exposure score, severity breakdown, category and top-finding charts. |
| **Exportable report** | Markdown download suitable for executives and a technical appendix for analysts. |
| **Run persistence** | SQLite storage of assessments, assets, observations, and findings for review and re-export. |

**End-to-end flow:** authorize → discover → check → score → dashboard → report.

---

## MVP scope — included

| Area | Behavior |
|------|----------|
| **Inputs** | Company name, primary domain; optional assessment name, date, business owner; optional public IPs (stored for future correlation). |
| **Authorization** | `probe-verification=<token>` at domain apex; labeled demo and manual modes. |
| **Discovery** | Apex DNS; wordlist subdomains (e.g. www, mail, vpn, portal, login, admin, api, dev, staging). |
| **Safe checks** | Status, redirects, page title, response headers; TLS notAfter and related metadata; SPF/DMARC; HSTS and related header gaps. |
| **Classification** | Keyword-based asset typing with low/medium/high confidence. |
| **Outputs** | Plotly charts, findings table, Markdown report with limitations disclosure. |

---

## MVP scope — excluded

**Non-goals (never in scope for this product):**

- Vulnerability exploitation or proof-of-concept attacks  
- Authentication bypass, credential attacks, or form submission  
- SQL injection, directory brute forcing, or intrusive scanner plugins  
- Assessment of unauthorized targets or internal/private networks  
- Replacement of full pentest or commercial ASM programs  

**Planned enhancements (post-MVP, if pursued):**

- Certificate Transparency discovery  
- PDF/HTML export beyond Markdown  
- Historical comparison across assessments  
- Optional REST API  
- Full public-IP correlation and infrastructure grouping  

Current implementation is **hostname-centric**; optional IPs may be recorded but are not yet fully correlated in checks.

---

## Personas

1. **Executive (CEO / CIO / CISO)** — Overall exposure rating, top risks in plain language, prioritized actions.  
2. **Security analyst** — Evidence (hostnames, headers, certificates, DNS), severity, confidence, appendix detail.  
3. **IT owner** — Concrete remediation steps and timing (immediate vs near term).

---

## Known limitations

PROBE cannot guarantee:

- Discovery of every public asset  
- Detection of every vulnerability  
- That any exposed service is exploitable  
- Perfect page or hostname classification  
- IP ownership without supporting evidence  

Internal security and authenticated application risks are **out of scope**.

**Assessment disclosure:**  
*This assessment is an outside-in exposure review based on safe public checks. It does not perform exploitation, authenticated testing, source-code review, or internal network assessment. Findings should be validated by the organization before remediation decisions are finalized.*

---

## Operational considerations

| Consideration | Approach |
|---------------|----------|
| DNS TXT delays | Pre-publish TXT for production runs; use demo/manual for demos. |
| Classification false positives | Show confidence; validate findings before action. |
| Incomplete discovery vs ASM | Document as lightweight outside-in, not exhaustive inventory. |
| External API use (future CT) | Rate limits and respectful request volume in configuration. |
| Local data | `probe_data.db` is local and gitignored; not shared via the repository. |

---

## Success criteria for the MVP

The MVP is successful when a user with authorization can:

1. Create and verify an assessment for a domain they control (or use an approved demo mode).  
2. Run safe checks and receive scored findings with business-readable text.  
3. Review results on the executive dashboard with charts.  
4. Download a report that leadership and analysts can use without reading raw scanner output.  
5. Understand product limits and non-goals from the report and this overview.
