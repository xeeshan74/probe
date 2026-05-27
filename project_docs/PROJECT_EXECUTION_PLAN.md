## 1. PROBE project summary

| | |
|--|--|
| **Product** | PROBE — Public Risk Observation and Business Exposure Reporting |
| **Type** | Authorized outside-in exposure reporting (Python / Streamlit) |
| **Users** | Executives, security analysts, IT operations, compliance |
| **Focus** | Bridge the gap between raw security data and what leadership needs to decide—safe public checks, executive-readable output, analyst appendix |

Repo: `github.com/xeeshan74/probe`

---

## 2. Milestone objective

Week 4 is about **planning**, not building new features.

This milestone we:

- Formed the team and split responsibilities
- Got the project proposal **approved by the instructor**
- Refined the MVP scope (Week 3)
- Defined how we will build and deliver the product through Week 14

Our next major checkpoint is a **working demo in Week 8** (June 24).

---

## 3. Current status

**On track** · At risk ☐ · Behind ☐

---

## 4. Deliverables completed this milestone

- Team and roles set
- Proposal review
- Design analysis (SWOT, Golden Circle, competitive positioning) — Week 3
- MVP scoped and refined (need document please see rrepositorry)
- Execution plan and integrated delivery method (this report)
- **Ahead of schedule:** GitHub prototype live; P0 workflow working (authorize → discover → check → dashboard → Markdown report); component ownership assigned

---

## 5. Challenges & risks

**Challenges**

- DNS TXT may not propagate in time for live demos
- CT and similar APIs are rate-limited (deferred from MVP)
- Heuristic findings can false-positive—users must validate before acting
- Executive report needs clear writing, not just technical output
- AWS demo depends on lab credits
- Team is fully remote (US time zones)

**Mitigations**

- Demo/manual auth; pre-publish TXT when testing real verification
- Respect rate limits; position as periodic assessment, not continuous ASM
- Show confidence on findings; limitations in every report
- Separate report content from core scan logic where possible
- Local dev first; Brian moves to AWS for Week 8; billing alerts
- Weekly calls + Slack/GitHub; async updates

---

## 6. Project management execution plan

**Roles** (everyone contributes to code and design; leads below):

| Lead | Area |
|------|------|
| Zeeshan Taj | Core app, auth, discovery, architecture |
| Brian Wai | AWS deploy, demo URL, CI/CD prep |
| Pauline Chane | PM, docs, instructor comms |
| Abdul Hardi Umar | Shared development & solution design |

**Cadence:** Weekly call; Slack + GitHub; 1:1 as needed
**Tracking:** GitHub Projects; progress via weekly deliverables

Detail: [WBS_AND_ITERATIONS.md](WBS_AND_ITERATIONS.md)

---

## 7. Integrated delivery method

**Phases**

- **Weeks 1–4:** Team, proposal, MVP scope, planning (now)
- **Weeks 5–8:** Architecture, threat model, 5-point presentation, **mid-point demo (Jun 24)**
- **Weeks 9–14:** Pitch, project site, final demo, expert panel

**Development**

- GitHub; modular `probe/` layout
- Local dev + Streamlit; AWS hosting for class demos (Brian)
- Demo/manual mode for presentations
- Python, Streamlit, open-source libraries

---
## 8. Personas and Use Cases

**Personas**

- **Executive** — exposure rating, top risks, prioritized actions
- **Security analyst** — evidence, severity, confidence, appendix
- **IT owner** — remediation and timing
- **Compliance** — audit-friendly report output

**Use Case Scenarios**

- **Scenario 1 — SMB E-Commerce Launch —** A small-to-medium size organization is looking to expand e-commerce operations and wants to assess its external attack surface through outside-in checks, but is on a time and resource sensitive launch schedule and cannot prioritize a full red team audit. 

- **Scenario 2 — MSSP-Dependent Organization —** Organization A relies on an MSSP to manage large-scale SIEM, EDR, ASM, etc, but this group is responsible for managing the same concerns for multiple organizations. Organization A's leadership is seeking an on-demand solution to do a quick, lightweight attack-surface assessment of current and future online assets that can be completed without waiting on the MSSP. 

- **Scenario 3 — C-Suite Reporting Gap —** A cybersecurity task force for Organization B has identified several potential vulnerabilities that could be addressed through prioritizing ASM, but the platforms and tools that provide relevant evidence use domain-specific jargon that leadership is not familiar with. The task force is seeking a tool that can easily generate a report to show the high impact of known attack-surface vulnerabilities to the organization's C-Suite. This report should also be able to map the "executive friendly" output to technical breakdowns for security analysts to review. 

- **Scenario 4 — Stakeholder Accountability —** Executive leadership for a large organization is meeting with stakeholders who are concerned about how the organization plans to respond to the growing threat landscape within their industry. Leadership would like to demonstrate their ability to optimize cybersecurity workflows through their inclusion of lightweight assessments in their processes. In addition, leadership requires clear, convenient reports that can easily show stakeholders that the organization is proactively assessing attack surfaces of public-facing assets. 

---

## 9. Delivery roadmap 
| Priority | Status | Scope |
|----------|--------|-------|
| P0 | Complete | Core flow assessment scanning and report generation |
| P1 | In Progress | Demo/presentation ready product; Live AWS deployment and CI/CD |
| P2 | Time-Permitting | Additional scanning functionalities (Certificate Transparency log checks, PDF formatted report, REST API architecture refactoring) |

---

## 10. Next steps (Weeks 5–8)

| Week | Focus |
|------|--------|
| 5 | Solution design & architecture presentation |
| 6 | Threat modeling |
| 7 | Five-point presentation |
| 8 | Proof-of-concept demo (+ AWS URL) |

**Next milestone:** Mid-point review · **Week 8 · Jun 24, 2026**