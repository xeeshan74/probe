"""Heuristic page / hostname classification."""

from __future__ import annotations

from typing import Tuple

# Hostname and text signals (spec §10.11)
_KEYWORDS = [
    "login",
    "admin",
    "portal",
    "vpn",
    "remote",
    "sso",
    "dashboard",
    "console",
    "api",
    "dev",
    "staging",
    "test",
]


def classify_asset(hostname: str, title: str, final_url: str) -> Tuple[str, str]:
    """
    Returns (asset_type, confidence) where confidence is low|medium|high.
    """
    blob = f"{hostname} {title} {final_url}".lower()
    hits = [k for k in _KEYWORDS if k in blob]
    if not hits:
        return "unknown", "low"

    # Strong combos
    if any(k in hostname.lower() for k in ("vpn", "remote", "sslvpn")):
        return "vpn", "high"
    if "admin" in hostname.lower() or "admin" in title.lower():
        return "admin", "high" if ("admin" in hostname.lower() and title) else "medium"
    if "login" in hostname.lower() or "sso" in hostname.lower():
        return "login", "medium"
    if "api" in hostname.lower() or "/api" in final_url.lower():
        return "api", "medium"
    if any(x in hostname.lower() for x in ("dev", "staging", "test")):
        return "dev_staging", "high"

    if len(hits) >= 2:
        return "sensitive_web", "medium"
    return "sensitive_web", "low"
