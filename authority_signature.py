import hashlib
import hmac
import json
import secrets
from typing import Dict, Any

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------

# Replace with environment variable in production
_SECRET_KEY = secrets.token_bytes(32)

# ------------------------------------------------------------------
# CANONICALIZATION
# ------------------------------------------------------------------

def canonicalize(data: Dict[str, Any]) -> bytes:
    """
    Deterministic JSON serialization.
    Stable ordering.
    No whitespace variance.
    """
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")

# ------------------------------------------------------------------
# HASHING
# ------------------------------------------------------------------

def compute_hash(data: Dict[str, Any]) -> str:
    """
    Deterministic SHA-256 hash of canonicalized payload.
    """
    return hashlib.sha256(canonicalize(data)).hexdigest()

# ------------------------------------------------------------------
# SIGNING
# ------------------------------------------------------------------

def sign_receipt(receipt: Dict[str, Any]) -> str:
    """
    HMAC-based signature for commit-bound receipt.
    """
    message = canonicalize(receipt)
    return hmac.new(
        _SECRET_KEY,
        message,
        hashlib.sha256
    ).hexdigest()

# ------------------------------------------------------------------
# VERIFICATION
# ------------------------------------------------------------------

def verify_receipt(receipt: Dict[str, Any], signature: str) -> bool:
    """
    Constant-time verification.
    """
    expected = sign_receipt(receipt)
    return hmac.compare_digest(expected, signature)

# ------------------------------------------------------------------
# OPTIONAL: CHAIN HELPER
# ------------------------------------------------------------------

def chain_hash(parent_hash: str, receipt: Dict[str, Any]) -> str:
    """
    Deterministic chain extension.
    """
    payload = {
        "parent": parent_hash,
        "receipt": receipt
    }
    return compute_hash(payload)
