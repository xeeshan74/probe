"""Plotly chart builders for the Streamlit executive dashboard."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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

# Hero gauge vs supporting tiles on the executive dashboard.
DASHBOARD_HERO_HEIGHT = 500
DASHBOARD_CHART_HEIGHT = 235
DASHBOARD_PANEL_HEIGHT = 255


@dataclass(frozen=True)
class ChartTheme:
    template: str
    paper_bg: str
    plot_bg: str
    font: str
    title: str
    tick: str
    axis_title: str
    grid: str
    line: str
    marker_fill: str
    marker_line: str
    bar_text: str
    muted: str
    hover_bg: str
    hover_font: str
    hover_border: str
    gauge_number: str
    gauge_title: str
    gauge_bg: str
    gauge_tick: str
    scatter_stroke: str
    trend_decline: str
    trend_incline: str


def _streamlit_is_light() -> bool:
    try:
        return st.get_option("theme.base") == "light"
    except Exception:
        return False


def chart_theme() -> ChartTheme:
    if _streamlit_is_light():
        return ChartTheme(
            template="plotly_white",
            paper_bg="rgba(0,0,0,0)",
            plot_bg="rgba(248, 250, 252, 0.95)",
            font="#1f2937",
            title="#111827",
            tick="#374151",
            axis_title="#374151",
            grid="rgba(148, 163, 184, 0.35)",
            line="#64748b",
            marker_fill="#ffffff",
            marker_line="#64748b",
            bar_text="#111827",
            muted="#475569",
            hover_bg="#ffffff",
            hover_font="#111827",
            hover_border="#cbd5e1",
            gauge_number="#111827",
            gauge_title="#374151",
            gauge_bg="rgba(226, 232, 240, 0.65)",
            gauge_tick="#64748b",
            scatter_stroke="#334155",
            trend_decline="#166534",
            trend_incline="#c2410c",
        )
    return ChartTheme(
        template="plotly_dark",
        paper_bg="rgba(0,0,0,0)",
        plot_bg="rgba(17, 24, 39, 0.45)",
        font="#e5e7eb",
        title="#f9fafb",
        tick="#cbd5e1",
        axis_title="#e2e8f0",
        grid="rgba(148, 163, 184, 0.15)",
        line="#cbd5e1",
        marker_fill="#f8fafc",
        marker_line="#64748b",
        bar_text="#f1f5f9",
        muted="#94a3b8",
        hover_bg="#1f2937",
        hover_font="#f3f4f6",
        hover_border="#374151",
        gauge_number="#f9fafb",
        gauge_title="#e5e7eb",
        gauge_bg="rgba(30, 41, 59, 0.6)",
        gauge_tick="#94a3b8",
        scatter_stroke="#1e293b",
        trend_decline="#4ade80",
        trend_incline="#ff8c42",
    )


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
    t = chart_theme()
    compact = height <= 300
    fig.update_layout(
        template=t.template,
        paper_bgcolor=t.paper_bg,
        plot_bgcolor=t.plot_bg,
        font=dict(
            family="Segoe UI, Inter, Roboto, sans-serif",
            size=12 if compact else 13,
            color=t.font,
        ),
        title=dict(
            text=title,
            font=dict(
                size=15 if compact else 17,
                color=t.title,
                family="Segoe UI, Inter, sans-serif",
            ),
            x=0,
            xanchor="left",
            pad=dict(t=2 if compact else 4, b=8 if compact else 12),
        ),
        margin=dict(
            l=40 if compact else 48,
            r=20 if compact else 28,
            t=56 if compact else 72,
            b=36 if compact else 48,
        ),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=t.font),
        ),
        hoverlabel=dict(
            bgcolor=t.hover_bg,
            bordercolor=t.hover_border,
            font=dict(color=t.hover_font, size=13),
        ),
    )
    fig.update_xaxes(
        gridcolor=t.grid,
        linecolor=t.grid,
        zerolinecolor=t.grid,
        tickfont=dict(color=t.tick),
        title_font=dict(color=t.axis_title),
    )
    fig.update_yaxes(
        gridcolor=t.grid,
        linecolor=t.grid,
        zerolinecolor=t.grid,
        tickfont=dict(color=t.tick),
        title_font=dict(color=t.axis_title),
    )
    return fig


def _empty_figure(title: str, message: str = "No data yet") -> go.Figure:
    t = chart_theme()
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=15, color=t.muted),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return _apply_layout(fig, title=title, height=DASHBOARD_CHART_HEIGHT)


def fig_risk_gauge(score: int) -> go.Figure:
    t = chart_theme()
    score = max(0, min(100, int(score)))
    steps = [{"range": [lo, hi], "color": color} for lo, hi, color in GAUGE_BANDS]
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={
                "text": "Exposure score",
                "font": {"size": 16, "color": t.gauge_title, "family": "Segoe UI, Inter, sans-serif"},
            },
            number={
                "suffix": " / 100",
                "font": {"size": 48, "color": t.gauge_number, "family": "Segoe UI, Inter, sans-serif"},
            },
            gauge={
                "shape": "angular",
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": t.gauge_tick,
                    "tickfont": {"color": t.gauge_tick, "size": 11},
                },
                "bar": {"color": _gauge_bar_color(score), "thickness": 0.28},
                "bgcolor": t.gauge_bg,
                "borderwidth": 0,
                "steps": steps,
            },
        )
    )
    fig.update_layout(
        template=t.template,
        paper_bgcolor=t.paper_bg,
        plot_bgcolor=t.paper_bg,
        height=DASHBOARD_HERO_HEIGHT,
        margin=dict(l=24, r=24, t=64, b=24),
    )
    return fig


def _severity_trend_summary(counts: pd.DataFrame) -> tuple[str, str, str]:
    """Return (ratio label, trend label, trend color) for low→high severity bars."""
    t = chart_theme()
    order = ["low", "medium", "high", "critical"]
    total = int(counts["count"].sum())
    if total == 0:
        return "No findings", "—", t.muted

    by_sev = {row["severity"]: int(row["count"]) for _, row in counts.iterrows()}
    low_tier = by_sev.get("low", 0) + by_sev.get("medium", 0)
    high_tier = by_sev.get("high", 0) + by_sev.get("critical", 0)
    pct_parts = [f"{sev.title()} {by_sev.get(sev, 0) / total * 100:.0f}%" for sev in order]
    ratio_label = (
        f"Low→High ratio {low_tier}:{high_tier} · High→Low {high_tier}:{low_tier} · "
        + " · ".join(pct_parts)
    )

    # Slope of counts from low (left) to critical (right)
    y = [by_sev.get(s, 0) for s in order]
    n = len(y)
    x_mean = (n - 1) / 2
    y_mean = sum(y) / n
    num = sum((i - x_mean) * (y[i] - y_mean) for i in range(n))
    den = sum((i - x_mean) ** 2 for i in range(n)) or 1
    slope = num / den

    if slope > 0.2:
        trend_label = "Trend: inclining ↗ (counts rise toward Critical — review high-severity items)"
        color = t.trend_incline
    elif slope < -0.2:
        trend_label = "Trend: declining ↘ (counts fall toward Critical — mostly lower severity)"
        color = t.trend_decline
    else:
        trend_label = "Trend: flat → (even mix across severities)"
        color = t.muted

    return ratio_label, trend_label, color


def fig_severity_counts(findings: List[Dict[str, Any]]) -> go.Figure:
    title = "Findings by severity"
    if not findings:
        return _empty_figure(title, "No findings")

    df = pd.DataFrame(findings)
    order = ["low", "medium", "high", "critical"]
    counts = df["severity"].str.lower().value_counts().reindex(order, fill_value=0).reset_index()
    counts.columns = ["severity", "count"]
    counts["severity"] = pd.Categorical(counts["severity"], categories=order, ordered=True)
    counts["label"] = counts["severity"].str.title()
    total = int(counts["count"].sum())
    counts["pct"] = (counts["count"] / total * 100).round(0).astype(int)
    counts["bar_text"] = counts.apply(
        lambda r: f"{int(r['count'])}<br>({int(r['pct'])}%)", axis=1
    )

    fig = px.bar(
        counts,
        x="label",
        y="count",
        color="severity",
        color_discrete_map=SEVERITY_COLORS,
        text="bar_text",
        category_orders={"label": [s.title() for s in order]},
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="%{text}",
        textfont=dict(size=12, color=chart_theme().bar_text),
        marker=dict(line=dict(width=0), cornerradius=8),
        hovertemplate="<b>%{x}</b><br>Count: %{y}<br>Share: %{customdata[0]}%<extra></extra>",
        customdata=counts[["pct"]].values,
        cliponaxis=False,
    )
    y_max = int(counts["count"].max()) or 1
    fig.update_layout(bargap=0.35, showlegend=False)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title="Count", range=[0, y_max + max(2, round(y_max * 0.45))])
    fig = _apply_layout(fig, title=title, height=DASHBOARD_CHART_HEIGHT, show_legend=False)
    fig.update_layout(margin=dict(l=40, r=20, t=64, b=36))
    return fig


def fig_severity_trend(findings: List[Dict[str, Any]], *, compact: bool = False) -> go.Figure:
    """Low→Critical severity trend line (shown beside highest-priority findings)."""
    title = "Severity trend"
    if not findings:
        return _empty_figure(title, "No findings")

    df = pd.DataFrame(findings)
    order = ["low", "medium", "high", "critical"]
    counts = df["severity"].str.lower().value_counts().reindex(order, fill_value=0).reset_index()
    counts.columns = ["severity", "count"]
    counts["label"] = counts["severity"].str.title()
    ratio_label, trend_label, trend_color = _severity_trend_summary(counts)

    y_max = int(counts["count"].max()) or 1
    t = chart_theme()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=counts["label"],
            y=counts["count"],
            mode="lines+markers",
            name="Severity trend",
            line=dict(color=t.line, width=2 if compact else 2.5),
            marker=dict(
                size=8 if compact else 10,
                color=t.marker_fill,
                line=dict(width=2, color=t.marker_line),
            ),
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
        )
    )
    chart_height = DASHBOARD_CHART_HEIGHT
    caption = trend_label if compact else f"{ratio_label}<br><span style='color:{trend_color}'><b>{trend_label}</b></span>"
    fig.update_layout(
        xaxis_title="Severity (low → critical)" if not compact else None,
        yaxis_title="Count",
        yaxis=dict(range=[0, y_max + max(1, y_max * 0.25)]),
        showlegend=False,
    )
    fig = _apply_layout(fig, title=title, height=chart_height, show_legend=False)
    fig.update_layout(margin=dict(t=72, b=32, l=40, r=24))
    fig.add_annotation(
        text=f"<span style='color:{trend_color}'><b>{caption}</b></span>" if compact else caption,
        xref="paper",
        yref="paper",
        x=0,
        y=1.10 if compact else 1.14,
        showarrow=False,
        align="left",
        font=dict(size=9 if compact else 10, color=chart_theme().muted),
    )
    return fig


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
        textfont=dict(size=13, color=chart_theme().bar_text),
        marker=dict(line=dict(width=0), cornerradius=6),
        hovertemplate="<b>%{y}</b><br>Risk points: %{x}<extra></extra>",
    )
    fig.update_layout(bargap=0.28, xaxis_title="Weighted risk points", yaxis_title=None)
    return _apply_layout(fig, title=title, height=DASHBOARD_CHART_HEIGHT)


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


def fig_top_findings(findings: List[Dict[str, Any]], n: int = 8, *, compact: bool = False) -> go.Figure:
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
        textfont=dict(size=12, color=chart_theme().bar_text),
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
    height = DASHBOARD_PANEL_HEIGHT if compact else DASHBOARD_CHART_HEIGHT
    show_legend = not compact
    fig = _apply_layout(fig, title=title, height=height, show_legend=show_legend)
    if not compact:
        fig.add_annotation(
            text=subtitle,
            xref="paper",
            yref="paper",
            x=0,
            y=1.08,
            showarrow=False,
            font=dict(size=12, color=chart_theme().muted),
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
        marker=dict(line=dict(width=1.5, color=chart_theme().scatter_stroke), opacity=0.88),
        hovertemplate="<b>%{hovertext}</b><br>Severity: %{x}<br>Confidence: %{y}<br>Score: %{customdata[1]}<extra></extra>",
    )
    fig.update_layout(
        xaxis_title="Severity",
        yaxis_title="Confidence",
        xaxis=dict(type="category"),
        yaxis=dict(type="category"),
    )
    return _apply_layout(fig, title=title, height=DASHBOARD_CHART_HEIGHT, show_legend=False)
