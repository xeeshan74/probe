"""Subdomain and hostname discovery (DNS + wordlist)."""

from __future__ import annotations

from typing import List

from config import CONFIG
from dns_utils import normalize_domain, resolve_a_aaaa
from models import AssetConfidence, DiscoveryResult


def discover_hostnames(primary_domain: str) -> List[DiscoveryResult]:
    primary_domain = normalize_domain(primary_domain)
    results: List[DiscoveryResult] = []

    apex_ips = resolve_a_aaaa(primary_domain)
    results.append(
        DiscoveryResult(
            hostname=primary_domain,
            source="dns_apex",
            ip_addresses=apex_ips,
            confidence=AssetConfidence.HIGH.value if apex_ips else AssetConfidence.MEDIUM.value,
        )
    )

    count = 0
    max_sub = CONFIG.assessment.max_subdomains
    for sub in CONFIG.default_subdomain_wordlist:
        if count >= max_sub:
            break
        fqdn = f"{sub}.{primary_domain}"
        ips = resolve_a_aaaa(fqdn)
        if not ips:
            continue
        results.append(
            DiscoveryResult(
                hostname=fqdn,
                source="wordlist_dns",
                ip_addresses=ips,
                confidence=AssetConfidence.MEDIUM.value,
            )
        )
        count += 1

    return results
