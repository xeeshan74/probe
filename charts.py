"""Plotly chart builders for the Streamlit dashboard."""

from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import CONFIG


def fig_risk_gauge(score: int) -> go.Figure:
    score = max(0, min(100, int(score)))
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Aggregate exposure score (capped)"},
            number={"suffix": " / 100"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, CONFIG.risk.low], "color": "#d4edda"},
                    {"range": [CONFIG.risk.low, CONFIG.risk.medium], "color": "#fff3cd"},
                    {"range": [CONFIG.risk.medium, CONFIG.risk.high], "color": "#f8d7da"},
                    {"range": [CONFIG.risk.high, 100], "color": "#f5c6cb"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": CONFIG.risk.high,
                },
            },
        )
    )
    fig.update_layout(height=320, margin=dict(l=30, r=30, t=50, b=30))
    return fig


def fig_severity_counts(findings: List[Dict[str, Any]]) -> go.Figure:
    if not findings:
        fig = go.Figure()
        fig.update_layout(title="Findings by severity", annotations=[{"text": "No findings", "showarrow": False}])
        return fig
    df = pd.DataFrame(findings)
    order = ["critical", "high", "medium", "low"]
    counts = df["severity"].str.lower().value_counts().reindex(order, fill_value=0).reset_index()
    counts.columns = ["severity", "count"]
    fig = px.bar(
        counts,
        x="severity",
        y="count",
        color="severity",
        color_discrete_map={
            "critical": "#721c24",
            "high": "#dc3545",
            "medium": "#fd7e14",
            "low": "#28a745",
        },
        title="Findings by severity",
    )
    fig.update_layout(showlegend=False, height=360, xaxis_title=None, yaxis_title="Count")
    return fig


def fig_category_risk(findings: List[Dict[str, Any]]) -> go.Figure:
    if not findings:
        fig = go.Figure()
        fig.update_layout(title="Risk points by category", annotations=[{"text": "No findings", "showarrow": False}])
        return fig
    df = pd.DataFrame(findings)
    df["category"] = df.get("category", "").replace("", "uncategorized").fillna("uncategorized")
    g = df.groupby("category", as_index=False)["risk_score"].sum()
    if g["risk_score"].sum() == 0:
        fig = go.Figure()
        fig.update_layout(title="Weighted risk by category", annotations=[{"text": "No score mass", "showarrow": False}])
        return fig
    fig = px.treemap(
        g,
        path=["category"],
        values="risk_score",
        title="Weighted risk points by category (treemap)",
    )
    fig.update_layout(height=400, margin=dict(t=50, l=10, r=10, b=10))
    return fig


def fig_top_findings(findings: List[Dict[str, Any]], n: int = 8) -> go.Figure:
    if not findings:
        fig = go.Figure()
        fig.update_layout(title="Top findings", annotations=[{"text": "No findings", "showarrow": False}])
        return fig
    df = pd.DataFrame(findings).head(n).copy()
    df["label"] = df["title"].astype(str).apply(lambda t: (t[:56] + "…") if len(t) > 56 else t)
    df = df.iloc[::-1]
    fig = px.bar(
        df,
        x="risk_score",
        y="label",
        color="severity",
        orientation="h",
        title=f"Top {n} findings by score",
        color_discrete_map={
            "critical": "#721c24",
            "high": "#dc3545",
            "medium": "#fd7e14",
            "low": "#28a745",
        },
    )
    fig.update_layout(height=min(900, 400 + n * 36), yaxis_title=None, xaxis_title="Risk score")
    return fig


def fig_confidence_severity(findings: List[Dict[str, Any]]) -> go.Figure:
    if not findings:
        fig = go.Figure()
        fig.update_layout(title="Confidence vs severity", annotations=[{"text": "No findings", "showarrow": False}])
        return fig
    df = pd.DataFrame(findings)
    sev_map = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    conf_map = {"low": 1, "medium": 2, "high": 3}
    df["sev_n"] = df["severity"].str.lower().map(sev_map).fillna(1)
    df["conf_n"] = df["confidence"].str.lower().map(conf_map).fillna(1)
    fig = px.scatter(
        df,
        x="sev_n",
        y="conf_n",
        size="risk_score",
        hover_name="title",
        hover_data=["hostname", "risk_score"],
        title="Severity vs confidence (bubble size = risk score)",
        labels={"sev_n": "Severity (ordinal)", "conf_n": "Confidence (ordinal)"},
    )
    fig.update_layout(height=420)
    return fig
