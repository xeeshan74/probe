"""Domain authorization: DNS TXT token verification."""

from __future__ import annotations

import secrets
from typing import Tuple

from dns_utils import get_txt_records, normalize_domain


def generate_verification_token() -> str:
    return secrets.token_hex(8)


def verification_record_value(token: str) -> str:
    return f"probe-verification={token}"


def verify_dns_txt(domain: str, expected_token: str) -> Tuple[bool, str]:
    """
    Returns (authorized, message).
    Looks for probe-verification=<token> in any TXT at the apex domain.
    """
    domain = normalize_domain(domain)
    full = verification_record_value(expected_token)
    txts = get_txt_records(domain)
    for txt in txts:
        if full in txt.replace(" ", ""):
            return True, "TXT verification succeeded."
    if not txts:
        return False, "No TXT records found at apex. Add the TXT record and try again."
    return False, "Verification token not found in TXT records at apex."
