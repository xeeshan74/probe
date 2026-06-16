"""PROBE for Executives — Streamlit UI."""

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from assessment_controller import (
    authorize_demo,
    authorize_dns,
    authorize_manual,
    create_assessment,
    run_assessment,
)
from authorization import verification_record_value
from finding_help import render_guide_tab, resolve_help_key
from chart_help import (
    CONFIDENCE_VS_SEVERITY,
    EXPOSURE_SCORE,
    FINDINGS_BY_SEVERITY,
    RISK_BY_CATEGORY,
    SEVERITY_TREND,
    SUMMARY_TABLE,
    TOP_FINDINGS,
    TOP_FINDINGS_TABLE,
    chart_help,
)
from charts import (
    fig_category_risk,
    fig_confidence_severity,
    fig_risk_gauge,
    fig_severity_counts,
    fig_severity_trend,
    fig_top_findings,
    top_findings_ranked_table,
    top_findings_use_table,
)
from report_generator import build_markdown_report, convert_markdown_to_pdf
from storage import (
    assessment_summary_metrics,
    delete_assessment_cascade,
    get_assessment,
    init_db,
    list_assets,
    list_assessments,
    list_findings,
)

FINDINGS_TABLE_COLUMNS = [
    ("title", "Finding"),
    ("severity", "Severity"),
    ("confidence", "Confidence"),
    ("risk_score", "Risk score"),
    ("hostname", "Host"),
    ("category", "Category"),
    ("business_impact", "Business impact"),
    ("technical_evidence", "Technical evidence"),
    ("recommended_action", "Remediation (best practice)"),
]


def findings_display_dataframe(findings: list) -> pd.DataFrame:
    """Executive findings table with remediation and evidence."""
    if not findings:
        return pd.DataFrame()
    df = pd.DataFrame(findings)
    src_cols = [src for src, _ in FINDINGS_TABLE_COLUMNS if src in df.columns]
    out = df[src_cols].copy()
    out.columns = [label for src, label in FINDINGS_TABLE_COLUMNS if src in df.columns]
    if "Severity" in out.columns:
        out["Severity"] = out["Severity"].str.title()
    if "Confidence" in out.columns:
        out["Confidence"] = out["Confidence"].str.title()
    if "Category" in out.columns:
        out["Category"] = out["Category"].replace("", "—").fillna("—")
    return out


def findings_table_column_config() -> dict:
    return {
        "Finding": st.column_config.TextColumn(width="medium"),
        "Severity": st.column_config.TextColumn(width="small"),
        "Confidence": st.column_config.TextColumn(width="small"),
        "Risk score": st.column_config.NumberColumn(format="%d", width="small"),
        "Host": st.column_config.TextColumn(width="small"),
        "Category": st.column_config.TextColumn(width="small"),
        "Business impact": st.column_config.TextColumn(width="medium"),
        "Technical evidence": st.column_config.TextColumn(width="large"),
        "Remediation (best practice)": st.column_config.TextColumn(width="large"),
    }

st.set_page_config(page_title="PROBE for Executives", layout="wide")

init_db()

if "selected_assessment_id" not in st.session_state:
    st.session_state.selected_assessment_id = None
if "vuln_help_key" not in st.session_state:
    st.session_state.vuln_help_key = None
if "selected_tab_index" not in st.session_state:
    st.session_state.selected_tab_index = 0

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

TABS = ["New assessment", "Authorize & run", "Dashboard", "Guide"]
tab_new, tab_auth, tab_dash, tab_guide = st.tabs(
    TABS,
    default=TABS[st.session_state.selected_tab_index]
)

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
            st.session_state.selected_tab_index = 1
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
                    st.session_state.selected_tab_index = 1
                    ok, msg = authorize_dns(current_id)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
            with c2:
                if st.button("Authorize (demo mode)"):
                    st.session_state.selected_tab_index = 1
                    ok, msg = authorize_demo(current_id)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
            with c3:
                if st.button("Authorize (manual / class demo)"):
                    st.session_state.selected_tab_index = 1
                    ok, msg = authorize_manual(current_id)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)

            if st.button("Run assessment (safe checks)", type="primary"):
                st.session_state.selected_tab_index = 1
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
        summary_df = pd.DataFrame(
            [
                {
                    "Assets in scope": metrics["asset_count"],
                    "Findings": metrics["finding_count"],
                    "High / critical": metrics["high_risk_findings"],
                    "Exposure score (sum cap)": metrics["aggregate_risk_score"],
                }
            ]
        )
        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Assets in scope": st.column_config.NumberColumn(format="%d"),
                "Findings": st.column_config.NumberColumn(format="%d"),
                "High / critical": st.column_config.NumberColumn(format="%d"),
                "Exposure score (sum cap)": st.column_config.NumberColumn(format="%d"),
            },
        )
        chart_help(SUMMARY_TABLE)

        # Bento layout: hero gauge left; severity + trend + priorities stacked right.
        hero_col, detail_col = st.columns([2, 3], gap="medium")
        with hero_col:
            st.plotly_chart(
                fig_risk_gauge(metrics["aggregate_risk_score"]),
                use_container_width=True,
            )
            chart_help(EXPOSURE_SCORE)
        with detail_col:
            snap_a, snap_b = st.columns(2, gap="small")
            with snap_a:
                st.plotly_chart(fig_severity_counts(findings), use_container_width=True)
                chart_help(FINDINGS_BY_SEVERITY)
            with snap_b:
                st.plotly_chart(fig_severity_trend(findings, compact=True), use_container_width=True)
                chart_help(SEVERITY_TREND)

            if top_findings_use_table(findings):
                st.markdown("##### Highest-priority findings")
                st.dataframe(
                    top_findings_ranked_table(findings),
                    use_container_width=True,
                    hide_index=True,
                )
                chart_help(TOP_FINDINGS_TABLE)
            else:
                st.plotly_chart(fig_top_findings(findings, compact=True), use_container_width=True)
                chart_help(TOP_FINDINGS)

        insight_a, insight_b = st.columns(2, gap="medium")
        with insight_a:
            st.plotly_chart(fig_category_risk(findings), use_container_width=True)
            chart_help(RISK_BY_CATEGORY)
        with insight_b:
            st.plotly_chart(fig_confidence_severity(findings), use_container_width=True)
            chart_help(CONFIDENCE_VS_SEVERITY)

        with st.expander("Findings table", expanded=True):
            if not findings:
                st.info("No findings yet. Run an assessment from **Authorize & run**.")
            else:
                display_df = findings_display_dataframe(findings)
                st.caption(
                    "Full finding detail including **remediation (best practice)**. "
                    "Select a row, then open the **Guide** tab for exploitation context."
                )
                picked_idx: int | None = None
                try:
                    table_event = st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config=findings_table_column_config(),
                        on_select="rerun",
                        selection_mode="single-row",
                        key="findings_table_select",
                    )
                    if table_event.selection.rows:
                        picked_idx = int(table_event.selection.rows[0])
                except TypeError:
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config=findings_table_column_config(),
                    )

                if picked_idx is not None:
                    active_title = str(findings[picked_idx]["title"])
                    help_key = resolve_help_key(active_title)
                    if help_key:
                        st.session_state.vuln_help_key = help_key
                        st.session_state.guide_from_finding = active_title
                        st.success(f"Open the **Guide** tab for: **{active_title}**")
                    else:
                        st.warning(f"No guide entry yet for: **{active_title}**")

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
        pdf = convert_markdown_to_pdf(current_id)
        st.download_button(
            "Download PDF report",
            data=pdf,
            file_name=f"probe_report_{current_id}.pdf",
            mime="application/pdf",
        )

with tab_guide:
    render_guide_tab(st.session_state.get("vuln_help_key"))
