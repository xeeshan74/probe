"""DNS helpers using dnspython."""

from __future__ import annotations

import ipaddress
from typing import List, Optional, Set

import dns.exception
import dns.resolver
import dns.reversename

from config import CONFIG


def _resolver() -> dns.resolver.Resolver:
    r = dns.resolver.Resolver()
    r.lifetime = CONFIG.assessment.request_timeout_seconds
    return r


def normalize_domain(domain: str) -> str:
    return domain.strip().lower().rstrip(".")


def is_private_ip(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True
    if addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved:
        return True
    return False


def resolve_a_aaaa(hostname: str) -> List[str]:
    hostname = normalize_domain(hostname)
    ips: Set[str] = set()
    r = _resolver()
    for rdtype in ("A", "AAAA"):
        try:
            ans = r.resolve(hostname, rdtype)
            for rr in ans:
                ips.add(str(rr))
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
            continue
        except dns.resolver.NoNameservers:
            continue
    if CONFIG.safety.block_private_ip_ranges:
        return [ip for ip in ips if not is_private_ip(ip)]
    return list(ips)


def get_txt_records(name: str) -> List[str]:
    name = normalize_domain(name)
    r = _resolver()
    try:
        ans = r.resolve(name, "TXT")
        chunks: List[str] = []
        for rr in ans:
            s = b"".join(rr.strings).decode("utf-8", errors="replace")
            chunks.append(s)
        return chunks
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
        return []
    except dns.resolver.NoNameservers:
        return []


def reverse_dns(ip: str) -> Optional[str]:
    if is_private_ip(ip):
        return None
    r = _resolver()
    try:
        rev = dns.reversename.from_address(ip)
        ans = r.resolve(rev, "PTR")
        if ans:
            return str(ans[0]).rstrip(".")
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout, OSError):
        return None
    return None
