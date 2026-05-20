"""SQLite persistence for assessments, assets, observations, findings."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

from config import CONFIG
from models import (
    Assessment,
    AssessmentStatus,
    Asset,
    AuthMethod,
    Finding,
    Observation,
)


def _db_path() -> Path:
    return Path(__file__).resolve().parent / CONFIG.database_path


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    path = _db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS assessments (
                assessment_id TEXT PRIMARY KEY,
                company_name TEXT NOT NULL,
                primary_domain TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL,
                authorization_method TEXT NOT NULL,
                verification_token TEXT NOT NULL,
                public_ips TEXT DEFAULT '',
                assessment_name TEXT DEFAULT '',
                business_owner TEXT DEFAULT '',
                assessment_date TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS assets (
                asset_id TEXT PRIMARY KEY,
                assessment_id TEXT NOT NULL,
                hostname TEXT NOT NULL,
                ip_address TEXT,
                source TEXT,
                asset_type TEXT,
                confidence TEXT,
                FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
            );
            CREATE TABLE IF NOT EXISTS observations (
                observation_id TEXT PRIMARY KEY,
                asset_id TEXT NOT NULL,
                observation_type TEXT NOT NULL,
                raw_value TEXT,
                normalized_value TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
            );
            CREATE TABLE IF NOT EXISTS findings (
                finding_id TEXT PRIMARY KEY,
                asset_id TEXT NOT NULL,
                title TEXT NOT NULL,
                severity TEXT NOT NULL,
                confidence TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                business_impact TEXT,
                technical_evidence TEXT,
                recommended_action TEXT,
                status TEXT DEFAULT 'open',
                category TEXT DEFAULT '',
                FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
            );
            """
        )


def insert_assessment(a: Assessment) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO assessments (
                assessment_id, company_name, primary_domain, created_at, status,
                authorization_method, verification_token, public_ips,
                assessment_name, business_owner, assessment_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                a.assessment_id,
                a.company_name,
                a.primary_domain,
                a.created_at.isoformat(),
                a.status.value,
                a.authorization_method.value,
                a.verification_token,
                a.public_ips,
                a.assessment_name,
                a.business_owner,
                a.assessment_date,
            ),
        )


def update_assessment_status(assessment_id: str, status: AssessmentStatus) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE assessments SET status = ? WHERE assessment_id = ?",
            (status.value, assessment_id),
        )


def update_assessment_auth(
    assessment_id: str,
    method: AuthMethod,
    status: AssessmentStatus,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE assessments SET authorization_method = ?, status = ?
            WHERE assessment_id = ?
            """,
            (method.value, status.value, assessment_id),
        )


def get_assessment(assessment_id: str) -> Optional[Assessment]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM assessments WHERE assessment_id = ?",
            (assessment_id,),
        ).fetchone()
    if not row:
        return None
    return _row_to_assessment(row)


def list_assessments(limit: int = 50) -> List[Assessment]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM assessments ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [_row_to_assessment(r) for r in rows]


def _row_to_assessment(row: sqlite3.Row) -> Assessment:
    return Assessment(
        assessment_id=row["assessment_id"],
        company_name=row["company_name"],
        primary_domain=row["primary_domain"],
        created_at=datetime.fromisoformat(row["created_at"]),
        status=AssessmentStatus(row["status"]),
        authorization_method=AuthMethod(row["authorization_method"]),
        verification_token=row["verification_token"],
        public_ips=row["public_ips"] or "",
        assessment_name=row["assessment_name"] or "",
        business_owner=row["business_owner"] or "",
        assessment_date=row["assessment_date"] or "",
    )


def insert_asset(asset: Asset) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO assets (
                asset_id, assessment_id, hostname, ip_address, source, asset_type, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                asset.asset_id,
                asset.assessment_id,
                asset.hostname,
                asset.ip_address,
                asset.source,
                asset.asset_type,
                asset.confidence,
            ),
        )


def list_assets(assessment_id: str) -> List[Asset]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM assets WHERE assessment_id = ? ORDER BY hostname",
            (assessment_id,),
        ).fetchall()
    return [
        Asset(
            asset_id=r["asset_id"],
            assessment_id=r["assessment_id"],
            hostname=r["hostname"],
            ip_address=r["ip_address"] or "",
            source=r["source"] or "",
            asset_type=r["asset_type"] or "",
            confidence=r["confidence"] or "",
        )
        for r in rows
    ]


def insert_observation(obs: Observation) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO observations (
                observation_id, asset_id, observation_type, raw_value, normalized_value, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                obs.observation_id,
                obs.asset_id,
                obs.observation_type,
                obs.raw_value,
                obs.normalized_value,
                obs.created_at.isoformat(),
            ),
        )


def insert_finding(f: Finding) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO findings (
                finding_id, asset_id, title, severity, confidence, risk_score,
                business_impact, technical_evidence, recommended_action, status, category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f.finding_id,
                f.asset_id,
                f.title,
                f.severity,
                f.confidence,
                f.risk_score,
                f.business_impact,
                f.technical_evidence,
                f.recommended_action,
                f.status,
                f.category,
            ),
        )


def list_findings(assessment_id: str) -> List[Dict[str, Any]]:
    """Findings joined with hostname for display."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT f.*, a.hostname
            FROM findings f
            JOIN assets a ON a.asset_id = f.asset_id
            WHERE a.assessment_id = ?
            ORDER BY f.risk_score DESC, f.severity
            """,
            (assessment_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def clear_assessment_results(assessment_id: str) -> None:
    """Remove assets, observations, findings for an assessment (keep assessment row)."""
    with get_connection() as conn:
        asset_ids = [
            r[0]
            for r in conn.execute(
                "SELECT asset_id FROM assets WHERE assessment_id = ?",
                (assessment_id,),
            ).fetchall()
        ]
        for aid in asset_ids:
            conn.execute("DELETE FROM observations WHERE asset_id = ?", (aid,))
            conn.execute("DELETE FROM findings WHERE asset_id = ?", (aid,))
        conn.execute("DELETE FROM assets WHERE assessment_id = ?", (assessment_id,))


def update_asset_classification(asset_id: str, asset_type: str, confidence: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE assets SET asset_type = ?, confidence = ? WHERE asset_id = ?",
            (asset_type, confidence, asset_id),
        )


def delete_assessment_cascade(assessment_id: str) -> None:
    with get_connection() as conn:
        asset_ids = [
            r[0]
            for r in conn.execute(
                "SELECT asset_id FROM assets WHERE assessment_id = ?",
                (assessment_id,),
            ).fetchall()
        ]
        for aid in asset_ids:
            conn.execute("DELETE FROM observations WHERE asset_id = ?", (aid,))
            conn.execute("DELETE FROM findings WHERE asset_id = ?", (aid,))
        conn.execute("DELETE FROM assets WHERE assessment_id = ?", (assessment_id,))
        conn.execute("DELETE FROM assessments WHERE assessment_id = ?", (assessment_id,))


def assessment_summary_metrics(assessment_id: str) -> Dict[str, Any]:
    findings = list_findings(assessment_id)
    assets = list_assets(assessment_id)
    high = sum(1 for f in findings if f["severity"] in ("high", "critical"))
    medium = sum(1 for f in findings if f["severity"] == "medium")
    low = sum(1 for f in findings if f["severity"] == "low")
    total_score = sum(int(f["risk_score"]) for f in findings)
    capped_score = min(100, total_score)
    return {
        "asset_count": len(assets),
        "finding_count": len(findings),
        "high_risk_findings": high,
        "medium_risk_findings": medium,
        "low_risk_findings": low,
        "aggregate_risk_score": capped_score,
        "findings_json": json.dumps(findings),
    }
