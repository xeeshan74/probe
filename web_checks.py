"""Non-invasive HTTP/HTTPS checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import httpx

from config import CONFIG


@dataclass
class WebCheckResult:
    url: str
    final_url: str
    status_code: Optional[int]
    title: str
    headers: Dict[str, str]
    error: Optional[str] = None


def _pick_title(html: str) -> str:
    if not html:
        return ""
    lower = html.lower()
    i = lower.find("<title")
    if i < 0:
        return ""
    j = lower.find(">", i)
    k = lower.find("</title>", j)
    if j < 0 or k < 0:
        return ""
    return html[j + 1 : k].strip()[:500]


def fetch_url(url: str) -> WebCheckResult:
    timeout = CONFIG.assessment.request_timeout_seconds
    max_redirect = CONFIG.assessment.max_redirects
    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            max_redirects=max_redirect,
            headers={"User-Agent": "PROBE-Executive-Scanner/1.0 (authorized assessment)"},
        ) as client:
            r = client.get(url)
            title = ""
            ctype = r.headers.get("content-type", "")
            if "html" in ctype.lower():
                title = _pick_title(r.text[:200_000])
            hdrs = {k.lower(): v for k, v in r.headers.items()}
            return WebCheckResult(
                url=url,
                final_url=str(r.url),
                status_code=r.status_code,
                title=title,
                headers=hdrs,
            )
    except Exception as e:  # noqa: BLE001 — surface as observation
        return WebCheckResult(
            url=url,
            final_url=url,
            status_code=None,
            title="",
            headers={},
            error=str(e)[:500],
        )


def check_https_and_http(hostname: str) -> List[WebCheckResult]:
    """Try https then http on standard ports."""
    out: List[WebCheckResult] = []
    for scheme in ("https", "http"):
        url = f"{scheme}://{hostname}/"
        out.append(fetch_url(url))
    return out
