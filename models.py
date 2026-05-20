"""Data models aligned with specs §13."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class AssessmentStatus(str, Enum):
    PENDING = "pending"
    PENDING_AUTHORIZATION = "pending_authorization"
    AUTHORIZED = "authorized"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


class AuthMethod(str, Enum):
    DNS_TXT = "dns_txt"
    DEMO_MODE = "demo_mode"
    MANUAL = "manual"


class AssetConfidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FindingSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingConfidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Assessment:
    assessment_id: str
    company_name: str
    primary_domain: str
    created_at: datetime
    status: AssessmentStatus
    authorization_method: AuthMethod
    verification_token: str
    public_ips: str = ""  # comma-separated for SQLite simplicity
    assessment_name: str = ""
    business_owner: str = ""
    assessment_date: str = ""


@dataclass
class Asset:
    asset_id: str
    assessment_id: str
    hostname: str
    ip_address: str
    source: str
    asset_type: str
    confidence: str


@dataclass
class Observation:
    observation_id: str
    asset_id: str
    observation_type: str
    raw_value: str
    normalized_value: str
    created_at: datetime


@dataclass
class Finding:
    finding_id: str
    asset_id: str
    title: str
    severity: str
    confidence: str
    risk_score: int
    business_impact: str
    technical_evidence: str
    recommended_action: str
    status: str = "open"
    category: str = ""  # tls, email, headers, surface, etc.

    def to_row_dict(self) -> Dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "asset_id": self.asset_id,
            "title": self.title,
            "severity": self.severity,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "business_impact": self.business_impact,
            "technical_evidence": self.technical_evidence,
            "recommended_action": self.recommended_action,
            "status": self.status,
            "category": self.category,
        }


@dataclass
class DiscoveryResult:
    hostname: str
    source: str
    ip_addresses: List[str]
    confidence: str
