"""Application configuration (MVP). YAML can be added later."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class AssessmentConfig:
    max_subdomains: int = 100
    request_timeout_seconds: float = 5.0
    max_redirects: int = 5
    rate_limit_delay_seconds: float = 0.5


@dataclass
class PortsConfig:
    web_ports: List[int] = field(default_factory=lambda: [80, 443, 8080, 8443])


@dataclass
class SafetyConfig:
    require_authorization: bool = True
    allow_demo_mode: bool = True
    block_private_ip_ranges: bool = True


@dataclass
class RiskThresholds:
    low: int = 20
    medium: int = 50
    high: int = 75
    critical: int = 100


@dataclass
class AppConfig:
    assessment: AssessmentConfig = field(default_factory=AssessmentConfig)
    ports: PortsConfig = field(default_factory=PortsConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    risk: RiskThresholds = field(default_factory=RiskThresholds)
    database_path: str = "probe_data.db"
    default_subdomain_wordlist: List[str] = field(
        default_factory=lambda: [
            "www",
            "mail",
            "vpn",
            "remote",
            "portal",
            "login",
            "admin",
            "api",
            "dev",
            "staging",
            "test",
            "app",
            "support",
            "secure",
            "sso",
        ]
    )


CONFIG = AppConfig()
