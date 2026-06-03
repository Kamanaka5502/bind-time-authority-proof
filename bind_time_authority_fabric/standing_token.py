import hashlib
import hmac
import json
import os
import time

DEMO_KEY_ENV = "BIND_TIME_AUTHORITY_DEMO_KEY"


def _demo_key() -> bytes:
    """
    Public demonstrator key source.

    This is not production key management. Production authority signing must use
    protected key custody outside the public proof surface.
    """
    value = os.getenv(DEMO_KEY_ENV)
    if not value:
        value = "public-demo-key-not-for-production"
    return value.encode("utf-8")


class StandingToken:
    def __init__(self, authority_epoch: int, scope_hash: str, state_hash: str):
        self.authority_epoch = authority_epoch
        self.scope_hash = scope_hash
        self.state_hash = state_hash
        self.timestamp = int(time.time())

    def payload(self):
        return {
            "authority_epoch": self.authority_epoch,
            "scope_hash": self.scope_hash,
            "state_hash": self.state_hash,
            "timestamp": self.timestamp,
        }

    def sign(self):
        payload_bytes = json.dumps(self.payload(), sort_keys=True).encode("utf-8")
        signature = hmac.new(_demo_key(), payload_bytes, hashlib.sha256).hexdigest()
        return {
            "payload": self.payload(),
            "signature": signature,
        }


def verify(token: dict) -> bool:
    payload_bytes = json.dumps(token["payload"], sort_keys=True).encode("utf-8")
    expected_signature = hmac.new(_demo_key(), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, token["signature"])
