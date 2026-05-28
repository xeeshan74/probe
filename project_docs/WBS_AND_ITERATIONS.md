# WBS & iterations ( PROBE )

**Team:** Zeeshan Taj · Abdul Hardi Umar · Pauline Chane · Brian Wai



---

## How we are using WBS in our project

A **Work Breakdown Structure** lists **deliverables** (things we must produce), not random tasks. Each row has an ID, an owner, a target week, and a status. We review it every Monday before class.

**100% rule:** Everything under 1.0 PROBE is either **done**, **in progress**, or listed in **P2 (later)**—nothing hidden.

**Prototype vs final design:** Sections **1.2–1.6** are a **baseline build** (Weeks 2–3) that proves the workflow. Week **5** (Jun 3) locks solution architecture; items in [week5/ARCHITECTURE_AND_DESIGN_NOTES.md](../week5/ARCHITECTURE_AND_DESIGN_NOTES.md) may add, cut, or reshape features.

---

## WBS hierarchy

```text
1.0  PROBE Capstone (May 6 – Aug 2026)
│
├── 1.1  Engineering foundation          [Baseline · Wks 2–3]
├── 1.2  Application — authorization     [Baseline · Wks 2–3 · design review W5]
├── 1.3  Application — discovery         [Baseline · Wks 2–3]
├── 1.4  Application — safe checks       [Baseline · Wks 2–3]
├── 1.5  Application — analysis & UI     [Baseline · Wks 2–3 · exec framing TBD]
├── 1.6  Application — workflow & data   [Baseline · Wks 2–3]
├── 1.7  AWS hosting & demo              [Brian · Week 8]
├── 1.8  Course deliverables (W1–W14)    [Ongoing]
└── P2   Stretch (only if time)          [Deferred]
```

---

## Work packages (detail)

### 1.1 Engineering foundation — **Baseline (Weeks 2–3)**

| ID | Deliverable | Owner | Module / artifact |
|----|-------------|-------|-------------------|
| 1.1.1 | Git repo + commit history | Team | `probe/.git` |
| 1.1.2 | GitHub remote, team access | Zeeshan | github.com/xeeshan74/probe |
| 1.1.3 | `.gitignore` (venv, DB, secrets) | Zeeshan | `probe/.gitignore` |
| 1.1.4 | Dependencies pinned | Zeeshan | `requirements.txt` |
| 1.1.5 | Clone / install / run docs | Zeeshan | `README.md` |
| 1.1.6 | Module layout, initial commit | Team | `app.py`, `models.py`, `config.py`, … |

### 1.2 Authorization & safety — **Baseline (Weeks 2–3)**

| ID | Deliverable | Owner | Module |
|----|-------------|-------|--------|
| 1.2.1 | DNS TXT verification | Zeeshan | `authorization.py` |
| 1.2.2 | Demo + manual classroom modes | Zeeshan | `authorization.py`, UI |
| 1.2.3 | Rate limit, private IP block | Zeeshan | `config.py`, `dns_utils.py` |

### 1.3 Discovery — **Baseline (Weeks 2–3)**

| ID | Deliverable | Owner | Module |
|----|-------------|-------|--------|
| 1.3.1 | Apex DNS resolution | Zeeshan | `discovery.py`, `dns_utils.py` |
| 1.3.2 | Wordlist subdomain discovery | Zeeshan | `discovery.py` |

### 1.4 Safe external checks — **Baseline (Weeks 2–3)**

| ID | Deliverable | Owner | Module |
|----|-------------|-------|--------|
| 1.4.1 | HTTP/HTTPS metadata (GET only) | Abdul / Zeeshan | `web_checks.py` |
| 1.4.2 | TLS certificate expiry | Abdul / Zeeshan | `tls_checks.py` |
| 1.4.3 | SPF / DMARC from DNS | Zeeshan | `email_checks.py` |
| 1.4.4 | Security header findings | Zeeshan | `risk_engine.py` |

### 1.5 Analysis & reporting — **Baseline (Weeks 2–3)**

| ID | Deliverable | Owner | Module |
|----|-------------|-------|--------|
| 1.5.1 | Page / surface classification + confidence | Abdul | `page_classifier.py` |
| 1.5.2 | Findings + risk scores | Zeeshan | `risk_engine.py` |
| 1.5.3 | Executive dashboard (charts) | Brian Wai | `charts.py`, `app.py` |
| 1.5.4 | Markdown report export | Brian Wai | `report_generator.py` |

### 1.6 Workflow & persistence — **Baseline (Weeks 2–3)**

| ID | Deliverable | Owner | Module |
|----|-------------|-------|--------|
| 1.6.1 | SQLite schema + CRUD | Zeeshan | `storage.py` |
| 1.6.2 | End-to-end assessment flow | Zeeshan | `assessment_controller.py` |

### 1.7 AWS hosting & demo — **In progress (Brian Wai)**

| ID | Deliverable | Target week | Status |
|----|-------------|-------------|--------|
| 1.7.1 | AWS credits, billing alert, tags | 4 | Prep |
| 1.7.2 | Deploy design (App Runner or Lightsail) | 5 | Planned |
| 1.7.3 | `deploy/` config in repo | 6 | Planned |
| 1.7.4 | Public HTTPS URL for class demo | **8** | Planned |
| 1.7.5 | Demo runbook + laptop fallback | 8 | Planned |
| 1.7.6 | *(Optional)* CodeBuild on push | 6–7 | Planned |

Checklist: [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md)

### 1.8 Course deliverables — **Ongoing**

| ID | Deliverable | Week | Owner | Status |
|----|-------------|------|-------|--------|
| 1.8.1 | Team + topic | 1 | Pauline | Done |
| 1.8.2 | 5W1H presentation | 2 | Team | Done |
| 1.8.3 | MVP overview + instructor OK | 3 | Pauline | Done |
| 1.8.4 | Milestone report + planning pres. | 4 | Pauline / Team | Done |
| 1.8.5 | Architecture presentation | 5 | Abdul + Zeeshan | **Now** |
| 1.8.6 | Threat model artifact | 6 | Team | Planned |
| 1.8.7 | 5-point presentation | 7 | Abdul + Team | Planned |
| 1.8.8 | Mid-point demo (20 min) | 8 | Team + Brian (host) | Planned |
| 1.8.9 | Bias / privacy learnings | 9 | Team | Planned |
| 1.8.10 | Competitive retro brief | 10 | Pauline | Planned |
| 1.8.11 | 2-minute pitch | 11 | Team | Planned |
| 1.8.12 | Project webpage | 12 | Brian / Pauline | Planned |
| 1.8.13 | Final package + dry run | 13 | Team | Planned |
| 1.8.14 | Industry showcase | 14 | Team | Planned |

### P2 — Stretch (deferred unless schedule allows)

| Item | Notes |
|------|--------|
| Certificate Transparency discovery | Rate limits, extra API work |
| PDF / HTML report export | Markdown is MVP |
| REST API (FastAPI) | Streamlit-only for now |
| Historical compare across runs | Needs schema design |
| Full public IP correlation | Optional field only today |

---

## Iterations

One **iteration** = one pass of **plan → build → test → improve**, ending when a **capstone deliverable** is done—not always after exactly one calendar week.

**Iteration vs course week:** The course uses **Week 1, Week 2, …** on the syllabus. We use **iteration 1, 2, 3, …** for delivery cycles. They usually match, but **iteration 2 = Weeks 2 and 3** because pitch, scope, instructor approval, and the working prototype all fall within the same build phase.

Iterations follow [SCHEDULE.md](SCHEDULE.md).

### Why iteration length varies

Iteration length follows **milestone size**, not a fixed seven-day box.

- **Weeks 2–3 (iteration 2)** — Longer on purpose. Week 2 was the 5W1H presentation; Week 3 was MVP refinement and instructor confirmation. We also built the first runnable `probe/` in that window. Splitting that into two one-week iterations would mark half the app “done” before it was usable.
- **Week 4 (iteration 3)** — Shorter. Planning, WBS, and milestone report—little new feature work.
- **Weeks 5–7** — Mostly **one week each** because each session has its own deliverable (architecture, threat model, 5-point).
- **Week 8 (iteration 7)** — One iteration for the mid-point demo and AWS URL—a single gate, even though prep runs in Weeks 5–7.

We still run plan → build → test → improve inside every iteration; we only combine weeks when the **outcome** spans both.

| Iter | Course weeks | Dates | Session deliverable | WBS closed (main) |
|------|-------|-------|---------------------|-------------------|
| 1 | 1 | May 6 | Team + topic | 1.8.1 |
| 2 | 2–3 | May 13–20 | 5W1H; overview; instructor OK | 1.1–1.6, 1.8.2–1.8.3 |
| 3 | 4 | May 27 | **Milestone report** | 1.8.4; 1.7.1 prep |
| 4 | 5 | Jun 3 | Architecture deck | 1.8.5, 1.7.2 |
| 5 | 6 | Jun 10 | Threat modeling | 1.8.6, 1.7.3 |
| 6 | 7 | Jun 17 | 5-point presentation | 1.8.7 |
| 7 | 8 | Jun 24 | **Mid demo + AWS URL** | 1.7.4–1.7.5, 1.8.8 |
| 8 | 9 | Jul 1 | Privacy learnings | 1.8.9 |
| 9 | 10 | Jul 8 | Competitive retro | 1.8.10 |
| 10 | 11 | Jul 15 | 2-min pitch | 1.8.11 |
| 11 | 12 | Jul 22 | Project webpage | 1.8.12 |
| 12 | 13 | Jul 29 | Final deliverables | 1.8.13 |
| 13 | 14 | Aug | Showcase | 1.8.14 |

**Current:** iteration 3 = **course Week 4** (milestone report).

```text
May        Jun              Jul              Aug
W1  W2 W3  W4  W5 W6 W7 W8  W9 W10 W11 W12 W13  W14
│   └──┘   │   └──── demo ────┘   └──── finish ────┘
topic  build   plan   arch→5pt→AWS URL
```

---

## Integrated delivery

How WBS work packages move through the delivery scope:

```text
  CODE          BUILD / TEST        DEPLOY              REVIEW
  GitHub    →   laptop + pip    →   AWS URL (Brian)  →  class / instructor
  probe/        optional CodeBuild   Week 8 demo         close WBS rows
```

- **GitHub Projects** = day-to-day tasks
- **WBS (this doc)** = scope, owners, project alignment
- **Weekly call** = mark done / at risk / blocked

---

## Status legend

| Label | Meaning |
|-------|---------|
| Baseline | Working in repo; may change after Week 5 design |
| Done | Accepted; in repo or submitted (course docs, etc.) |
| **Now** | Active this week |
| Planned | Scheduled; not started |
| Prep | Brian AWS setup, Week 4 |
| P2 | Out of MVP commit |