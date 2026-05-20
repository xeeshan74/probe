"""TLS certificate metadata (expiry, SAN)."""

from __future__ import annotations

import socket
import ssl
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import List, Optional


@dataclass
class TLSCheckResult:
    hostname: str
    not_after: Optional[datetime]
    not_before: Optional[datetime]
    subject: str
    san_list: List[str]
    issuer: str
    error: Optional[str] = None


def check_tls(hostname: str, port: int = 443) -> TLSCheckResult:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
        if not cert:
            return TLSCheckResult(
                hostname=hostname,
                not_after=None,
                not_before=None,
                subject="",
                san_list=[],
                issuer="",
                error="No certificate returned",
            )
        na = cert.get("notAfter")
        nb = cert.get("notBefore")
        not_after = _parse_asn1(na) if na else None
        not_before = _parse_asn1(nb) if nb else None
        subject = str(cert.get("subject", ""))
        issuer = str(cert.get("issuer", ""))
        san_list: List[str] = []
        for ext in cert.get("subjectAltName", []) or []:
            if ext[0].lower() == "dns":
                san_list.append(ext[1])
        return TLSCheckResult(
            hostname=hostname,
            not_after=not_after,
            not_before=not_before,
            subject=subject,
            san_list=san_list,
            issuer=issuer,
        )
    except Exception as e:  # noqa: BLE001
        return TLSCheckResult(
            hostname=hostname,
            not_after=None,
            not_before=None,
            subject="",
            san_list=[],
            issuer="",
            error=str(e)[:500],
        )


def _parse_asn1(s: str) -> datetime:
    dt = parsedate_to_datetime(s)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
