import hmac
import hashlib
import json
import time

SECRET_KEY = b"bind-time-authority-secret"

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
        payload_bytes = json.dumps(self.payload(), sort_keys=True).encode()
        signature = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()
        return {
            "payload": self.payload(),
            "signature": signature,
        }


def verify(token: dict) -> bool:
    payload_bytes = json.dumps(token["payload"], sort_keys=True).encode()
    expected_signature = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, token["signature"])
