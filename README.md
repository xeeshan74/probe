# PROBE for Executives

**Public Risk Observation and Business Exposure Reporting**

A lightweight, report-oriented **outside-in exposure assessment** tool for enterprise security leaders. PROBE helps answer what an attacker, vendor, customer, or external observer can see about an organization from the public internet—without exploitation or internal scanning.

> **Positioning:** Executive-readable risk reporting from safe public checknot a penetration test or full attack-surface management (ASM) platform.

## Features

- **Authorization:** DNS TXT verification (`probe-verification=<token>`), plus clearly labeled demo and manual (classroom) modes
- **Discovery:** Apex domain + built-in subdomain wordlist (DNS)
- **Safe checks:** HTTPS/HTTP metadata, TLS certificate health, SPF/DMARC, security headers
- **Classification:** Heuristic signals for login/admin/VPN/API/dev-style surfaces with separate **confidence**
- **Outputs:** Weighted risk-style scoring, Plotly dashboard, downloadable Markdown report (executive summary + technical appendix)
- **Storage:** SQLite-backed assessment history (local `probe_data.db`, gitignored)

## Requirements

- Python 3.10+
- Network access for DNS and HTTPS checks against **authorized** targets only

## Quick start

```bash
git clone https://github.com/xeeshan74/probe.git
cd probe
pip install -r requirements.txt
python -m streamlit run app.py
```

Open **http://localhost:8501** in your browser.

## AWS mock
moto_server -p 5000

## Usage workflow

1. **New assessment** — Enter company name and primary domain.
2. **Authorize & run**
   - **Production-like:** Add the DNS TXT record shown in the UI, then click **Verify DNS TXT**.
   - **Quick demo:** Use **Authorize (demo mode)** or **Authorize (manual / class demo)** for lab presentations.
3. **Run assessment** — Runs discovery and non-intrusive checks (rate-limited).
4. **Dashboard** — Review charts, findings table, and download the Markdown report.

## Project layout

| Module | Purpose |
|--------|---------|
| `app.py` | Streamlit UI |
| `assessment_controller.py` | Orchestrates create → authorize → run |
| `authorization.py` | DNS TXT token verification |
| `discovery.py` | Subdomain discovery (apex + wordlist) |
| `dns_utils.py` | DNS resolution helpers |
| `web_checks.py` | Safe HTTP/HTTPS requests |
| `tls_checks.py` | TLS certificate metadata |
| `email_checks.py` | SPF / DMARC analysis |
| `page_classifier.py` | Surface classification heuristics |
| `risk_engine.py` | Findings and scoring |
| `charts.py` | Plotly dashboard charts |
| `report_generator.py` | Markdown report export |
| `storage.py` | SQLite persistence |
| `config.py` | Timeouts, wordlist, safety settings |

## Ethics and scope

PROBE performs **authorized, non-intrusive** checks only. It does **not**:

- Exploit vulnerabilities or attempt authentication bypass
- Brute-force credentials or run intrusive scanner plugins
- Scan unauthorized organizations or internal private networks

Findings should be validated by the organization before remediation decisions. Discovery is not guaranteed to be complete compared to commercial ASM tools.

## Configuration

Edit defaults in `config.py` (request timeouts, subdomain wordlist, rate limits, risk thresholds).

## Documentation

- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) — MVP outcomes, scope, personas, limitations, and success criteria (no course-week framing)

## License

Academic / capstone use unless otherwise specified by the project team.
