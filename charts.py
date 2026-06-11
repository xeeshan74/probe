"""Plotly chart builders for the Streamlit executive dashboard."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import CONFIG

# Executive dashboard palette (works on Streamlit dark + light)
SEVERITY_COLORS = {
    "critical": "#ff4d6d",
    "high": "#ff8c42",
    "medium": "#ffc857",
    "low": "#4ade80",
}

CATEGORY_COLORS = {
    "headers": "#60a5fa",
    "tls": "#a78bfa",
    "email": "#22d3ee",
    "surface": "#f472b6",
    "uncategorized": "#94a3b8",
}

GAUGE_BANDS = [
    (0, CONFIG.risk.low, "rgba(74, 222, 128, 0.35)"),
    (CONFIG.risk.low, CONFIG.risk.medium, "rgba(255, 200, 87, 0.35)"),
    (CONFIG.risk.medium, CONFIG.risk.high, "rgba(255, 140, 66, 0.4)"),
    (CONFIG.risk.high, 100, "rgba(255, 77, 109, 0.45)"),
]


def _gauge_bar_color(score: int) -> str:
    if score >= CONFIG.risk.high:
        return "#ff4d6d"
    if score >= CONFIG.risk.medium:
        return "#ff8c42"
    if score >= CONFIG.risk.low:
        return "#ffc857"
    return "#4ade80"


def _apply_layout(
    fig: go.Figure,
    *,
    title: str,
    height: int = 400,
    show_legend: bool = False,
) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17, 24, 39, 0.45)",
        font=dict(family="Segoe UI, Inter, Roboto, sans-serif", size=13, color="#e5e7eb"),
        title=dict(
            text=title,
            font=dict(size=17, color="#f9fafb", family="Segoe UI, Inter, sans-serif"),
            x=0,
            xanchor="left",
            pad=dict(t=4, b=12),
        ),
        margin=dict(l=48, r=28, t=72, b=48),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(
            bgcolor="#1f2937",
            bordercolor="#374151",
            font=dict(color="#f3f4f6", size=13),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(148, 163, 184, 0.15)",
        linecolor="rgba(148, 163, 184, 0.25)",
        zerolinecolor="rgba(148, 163, 184, 0.2)",
        tickfont=dict(color="#cbd5e1"),
        title_font=dict(color="#e2e8f0"),
    )
    fig.update_yaxes(
        gridcolor="rgba(148, 163, 184, 0.15)",
        linecolor="rgba(148, 163, 184, 0.25)",
        zerolinecolor="rgba(148, 163, 184, 0.2)",
        tickfont=dict(color="#cbd5e1"),
        title_font=dict(color="#e2e8f0"),
    )
    return fig


def _empty_figure(title: str, message: str = "No data yet") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=15, color="#94a3b8"),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return _apply_layout(fig, title=title, height=320)


def fig_risk_gauge(score: int) -> go.Figure:
    score = max(0, min(100, int(score)))
    steps = [{"range": [lo, hi], "color": color} for lo, hi, color in GAUGE_BANDS]
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={
                "text": "Exposure score",
                "font": {"size": 16, "color": "#e5e7eb", "family": "Segoe UI, Inter, sans-serif"},
            },
            number={
                "suffix": " / 100",
                "font": {"size": 42, "color": "#f9fafb", "family": "Segoe UI, Inter, sans-serif"},
            },
            gauge={
                "shape": "angular",
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#64748b",
                    "tickfont": {"color": "#94a3b8", "size": 11},
                },
                "bar": {"color": _gauge_bar_color(score), "thickness": 0.28},
                "bgcolor": "rgba(30, 41, 59, 0.6)",
                "borderwidth": 0,
                "steps": steps,
            },
        )
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(l=24, r=24, t=64, b=16),
    )
    return fig


def fig_severity_counts(findings: List[Dict[str, Any]]) -> go.Figure:
    title = "Findings by severity"
    if not findings:
        return _empty_figure(title, "No findings")

    df = pd.DataFrame(findings)
    order = ["critical", "high", "medium", "low"]
    counts = df["severity"].str.lower().value_counts().reindex(order, fill_value=0).reset_index()
    counts.columns = ["severity", "count"]
    counts["severity"] = pd.Categorical(counts["severity"], categories=order, ordered=True)
    counts["label"] = counts["severity"].str.title()

    fig = px.bar(
        counts,
        x="label",
        y="count",
        color="severity",
        color_discrete_map=SEVERITY_COLORS,
        text="count",
        category_orders={"label": [s.title() for s in order]},
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=14, color="#f1f5f9"),
        marker=dict(line=dict(width=0), cornerradius=8),
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
    )
    fig.update_layout(bargap=0.35)
    return _apply_layout(fig, title=title, height=360)


def fig_category_risk(findings: List[Dict[str, Any]]) -> go.Figure:
    title = "Risk by category"
    if not findings:
        return _empty_figure(title, "No findings")

    df = pd.DataFrame(findings)
    df["category"] = df.get("category", "").replace("", "uncategorized").fillna("uncategorized")
    g = df.groupby("category", as_index=False)["risk_score"].sum()
    if g["risk_score"].sum() == 0:
        return _empty_figure(title, "No scored findings")

    g["label"] = g["category"].str.replace("_", " ").str.title()
    g["color_key"] = g["category"].str.lower()

    fig = px.bar(
        g.sort_values("risk_score", ascending=True),
        x="risk_score",
        y="label",
        orientation="h",
        color="color_key",
        color_discrete_map=CATEGORY_COLORS,
        text="risk_score",
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=13, color="#e2e8f0"),
        marker=dict(line=dict(width=0), cornerradius=6),
        hovertemplate="<b>%{y}</b><br>Risk points: %{x}<extra></extra>",
    )
    fig.update_layout(bargap=0.28, xaxis_title="Weighted risk points", yaxis_title=None)
    return _apply_layout(fig, title=title, height=380)


def _top_findings_df(findings: List[Dict[str, Any]], n: int = 8) -> pd.DataFrame:
    df = (
        pd.DataFrame(findings)
        .sort_values("risk_score", ascending=False)
        .head(n)
        .copy()
    )
    df["severity"] = df["severity"].str.lower()
    df["label"] = df["title"].astype(str).apply(lambda t: (t[:52] + "…") if len(t) > 52 else t)
    return df


def top_findings_use_table(findings: List[Dict[str, Any]]) -> bool:
    """Use a ranked table when a bar chart would not add clarity."""
    if not findings:
        return False
    if len(findings) <= 2:
        return True
    scores = {int(f.get("risk_score", 0)) for f in findings}
    return len(scores) == 1


def top_findings_ranked_table(findings: List[Dict[str, Any]], n: int = 8) -> pd.DataFrame:
    df = _top_findings_df(findings, n=n)
    df.insert(0, "Rank", range(1, len(df) + 1))
    return df.rename(
        columns={
            "title": "Finding",
            "severity": "Severity",
            "risk_score": "Risk score",
            "hostname": "Host",
        }
    )[["Rank", "Finding", "Severity", "Risk score", "Host"]]


def fig_top_findings(findings: List[Dict[str, Any]], n: int = 8) -> go.Figure:
    title = "Highest-priority findings"
    subtitle = "Longer bar = address sooner (by risk score)"
    if not findings:
        return _empty_figure(title, "No findings")

    if top_findings_use_table(findings):
        return _empty_figure(title, "Use ranked table view")

    df = _top_findings_df(findings, n=n)
    df = df.iloc[::-1]

    max_score = int(df["risk_score"].max())
    x_max = max(max_score + 2, round(max_score * 1.15))

    fig = px.bar(
        df,
        x="risk_score",
        y="label",
        color="severity",
        orientation="h",
        color_discrete_map=SEVERITY_COLORS,
        text="risk_score",
        hover_data={"hostname": True, "severity": True, "label": False, "risk_score": False},
    )
    fig.update_traces(
        texttemplate="%{x}",
        textposition="outside",
        textfont=dict(size=12, color="#e2e8f0"),
        marker=dict(line=dict(width=0), cornerradius=6),
        hovertemplate="<b>%{y}</b><br>Score: %{x}<br>Host: %{customdata[0]}<extra></extra>",
        cliponaxis=False,
    )
    fig.update_layout(
        bargap=0.22,
        xaxis_title="Risk score",
        yaxis_title=None,
    )
    fig.update_xaxes(range=[0, x_max])
    height = min(520, 280 + len(df) * 34)
    fig = _apply_layout(fig, title=title, height=height, show_legend=True)
    fig.add_annotation(
        text=subtitle,
        xref="paper",
        yref="paper",
        x=0,
        y=1.08,
        showarrow=False,
        font=dict(size=12, color="#94a3b8"),
        xanchor="left",
    )
    return fig


def fig_confidence_severity(findings: List[Dict[str, Any]]) -> go.Figure:
    title = "Confidence vs severity"
    if not findings:
        return _empty_figure(title, "No findings")

    df = pd.DataFrame(findings).copy()
    sev_order = ["low", "medium", "high", "critical"]
    conf_order = ["low", "medium", "high"]
    df["severity"] = df["severity"].str.lower()
    df["confidence"] = df["confidence"].str.lower()
    df["severity"] = pd.Categorical(df["severity"], categories=sev_order, ordered=True)
    df["confidence"] = pd.Categorical(df["confidence"], categories=conf_order, ordered=True)

    size = df["risk_score"].clip(lower=8) * 2.5

    fig = px.scatter(
        df,
        x="severity",
        y="confidence",
        size=size,
        color="severity",
        color_discrete_map=SEVERITY_COLORS,
        hover_name="title",
        hover_data={"hostname": True, "risk_score": True, "severity": False, "confidence": False},
        category_orders={"severity": sev_order, "confidence": conf_order},
    )
    fig.update_traces(
        marker=dict(line=dict(width=1.5, color="#1e293b"), opacity=0.88),
        hovertemplate="<b>%{hovertext}</b><br>Severity: %{x}<br>Confidence: %{y}<br>Score: %{customdata[1]}<extra></extra>",
    )
    fig.update_layout(
        xaxis_title="Severity",
        yaxis_title="Confidence",
    )
    return _apply_layout(fig, title=title, height=420, show_legend=False)
