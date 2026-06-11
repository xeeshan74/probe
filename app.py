"""PROBE for Executives — Streamlit UI."""

from __future__ import annotations

from datetime import date

import streamlit as st

from assessment_controller import (
    authorize_demo,
    authorize_dns,
    authorize_manual,
    create_assessment,
    run_assessment,
)
from authorization import verification_record_value
from charts import (
    fig_category_risk,
    fig_confidence_severity,
    fig_risk_gauge,
    fig_severity_counts,
    fig_top_findings,
    top_findings_ranked_table,
    top_findings_use_table,
)
from report_generator import build_markdown_report
from storage import (
    assessment_summary_metrics,
    delete_assessment_cascade,
    get_assessment,
    init_db,
    list_assets,
    list_assessments,
    list_findings,
)

st.set_page_config(page_title="PROBE for Executives", layout="wide")

init_db()

if "selected_assessment_id" not in st.session_state:
    st.session_state.selected_assessment_id = None

st.title("PROBE for Executives")
st.caption("Public Risk Observation and Business Exposure Reporting — outside-in, non-intrusive checks.")

if st.session_state.get("flash_message"):
    st.success(st.session_state.flash_message)
    del st.session_state.flash_message

with st.sidebar:
    st.subheader("Assessments")
    assessments = list_assessments(30)
    options = {f"{a.company_name} ({a.primary_domain})": a.assessment_id for a in assessments}
    if options:
        labels = list(options.keys())
        ids = list(options.values())
        default_index = 0
        if st.session_state.selected_assessment_id in ids:
            default_index = ids.index(st.session_state.selected_assessment_id)
        selected_label = st.selectbox("Open", labels, index=default_index)
        current_id = options[selected_label]
        st.session_state.selected_assessment_id = current_id
    else:
        st.selectbox("Open", ["No assessments yet"], disabled=True)
        current_id = None
    if st.button("Delete selected", disabled=not current_id):
        if current_id:
            delete_assessment_cascade(current_id)
            st.rerun()

tab_new, tab_auth, tab_dash = st.tabs(["New assessment", "Authorize & run", "Dashboard"])

with tab_new:
    st.markdown("Create an assessment. You will verify control of the domain before scans run.")
    st.caption("Defaults are prefilled for demo — edit any field before submitting.")
    _today = date.today().isoformat()
    with st.form("new_asm", clear_on_submit=True):
        company = st.text_input(
            "Company name *",
            value="DemoCorp",
            help="Legal or display name for the report.",
            key="new_company",
        )
        domain = st.text_input(
            "Primary domain *",
            value="example.com",
            help="Apex domain preferred (no https://). Use example.com for demo mode.",
            key="new_domain",
        )
        asm_name = st.text_input(
            "Assessment name",
            value="Outside-In Demo",
            help="Label for this assessment run.",
            key="new_asm_name",
        )
        asm_date = st.text_input(
            "Assessment date",
            value=_today,
            help="Report date (YYYY-MM-DD).",
            key="new_asm_date",
        )
        owner = st.text_input(
            "Business owner (optional)",
            value="IT Security",
            help="Optional contact or team name.",
            key="new_owner",
        )
        ips = st.text_input(
            "Public IPs (optional, comma-separated)",
            value="",
            help="Optional; reserved for future IP correlation.",
            key="new_ips",
        )
        submitted = st.form_submit_button("Create assessment")
    if submitted:
        if not company.strip() or not domain.strip():
            st.error("Company name and primary domain are required.")
        else:
            a, instr = create_assessment(
                company_name=company,
                primary_domain=domain,
                assessment_name=asm_name,
                assessment_date=asm_date,
                business_owner=owner,
                public_ips=ips,
            )
            st.session_state.selected_assessment_id = a.assessment_id
            st.session_state.flash_message = (
                f"Created **{a.assessment_id}**. Open **Authorize & run** → "
                f"**Authorize (demo mode)** for class, or add the DNS TXT record then **Verify DNS TXT**."
            )
            st.rerun()

with tab_auth:
    if not current_id:
        st.warning("Select or create an assessment in the sidebar.")
    else:
        a = get_assessment(current_id)
        if not a:
            st.error("Assessment not found.")
        else:
            st.subheader(f"{a.company_name} — `{a.primary_domain}`")
            st.write(f"**Status:** `{a.status.value}`  ·  **Auth:** `{a.authorization_method.value}`")
            st.code(verification_record_value(a.verification_token), language="text")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Verify DNS TXT"):
                    ok, msg = authorize_dns(current_id)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
            with c2:
                if st.button("Authorize (demo mode)"):
                    ok, msg = authorize_demo(current_id)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
            with c3:
                if st.button("Authorize (manual / class demo)"):
                    ok, msg = authorize_manual(current_id)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)

            if st.button("Run assessment (safe checks)", type="primary"):
                with st.spinner("Running discovery and checks…"):
                    ok, msg = run_assessment(current_id)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

with tab_dash:
    if not current_id:
        st.warning("Select an assessment in the sidebar.")
    else:
        a = get_assessment(current_id)
        findings = list_findings(current_id)
        assets = list_assets(current_id)
        metrics = assessment_summary_metrics(current_id)

        st.subheader("Executive view")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Assets in scope", metrics["asset_count"])
        m2.metric("Findings", metrics["finding_count"])
        m3.metric("High / critical", metrics["high_risk_findings"])
        m4.metric("Exposure score (sum cap)", metrics["aggregate_risk_score"])

        g1, g2 = st.columns([1, 1])
        with g1:
            st.plotly_chart(fig_risk_gauge(metrics["aggregate_risk_score"]), use_container_width=True)
        with g2:
            st.plotly_chart(fig_severity_counts(findings), use_container_width=True)

        if top_findings_use_table(findings):
            st.markdown("#### Highest-priority findings")
            st.caption(
                "Ranked list — bar chart is hidden when there are only a few findings "
                "or every finding has the same risk score."
            )
            st.dataframe(
                top_findings_ranked_table(findings),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.plotly_chart(fig_top_findings(findings), use_container_width=True)
        c3, c4 = st.columns(2)
        with c3:
            st.plotly_chart(fig_category_risk(findings), use_container_width=True)
        with c4:
            st.plotly_chart(fig_confidence_severity(findings), use_container_width=True)

        with st.expander("Findings table"):
            st.dataframe(findings, use_container_width=True, hide_index=True)
        with st.expander("Assets"):
            st.dataframe(
                [
                    {
                        "hostname": x.hostname,
                        "ip": x.ip_address,
                        "source": x.source,
                        "type": x.asset_type,
                        "confidence": x.confidence,
                    }
                    for x in assets
                ],
                use_container_width=True,
                hide_index=True,
            )

        md = build_markdown_report(current_id)
        st.download_button(
            "Download Markdown report",
            data=md,
            file_name=f"probe_report_{current_id}.md",
            mime="text/markdown",
        )
