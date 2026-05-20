"""SPF / DMARC analysis from DNS TXT."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from dns_utils import get_txt_records, normalize_domain


@dataclass
class EmailPosture:
    spf_present: bool
    spf_record: str
    dmarc_present: bool
    dmarc_record: str
    dmarc_policy: Optional[str]


def _extract_spf(txts: List[str]) -> str:
    for t in txts:
        if t.startswith("v=spf1"):
            return t
    return ""


def _dmarc_txts(domain: str) -> str:
    name = f"_dmarc.{normalize_domain(domain)}"
    txts = get_txt_records(name)
    for t in txts:
        if "v=DMARC1" in t or "v=dmarc1" in t:
            return t
    return ""


def _parse_dmarc_policy(record: str) -> Optional[str]:
    if not record:
        return None
    m = re.search(r"\bp=([^;\s]+)", record, re.I)
    return m.group(1).lower() if m else None


def analyze_email_security(domain: str) -> EmailPosture:
    domain = normalize_domain(domain)
    root_txts = get_txt_records(domain)
    spf = _extract_spf(root_txts)
    dmarc_raw = _dmarc_txts(domain)
    return EmailPosture(
        spf_present=bool(spf),
        spf_record=spf[:2000],
        dmarc_present=bool(dmarc_raw),
        dmarc_record=dmarc_raw[:2000],
        dmarc_policy=_parse_dmarc_policy(dmarc_raw),
    )
