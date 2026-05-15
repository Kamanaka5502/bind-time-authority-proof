import hashlib
import json
from dataclasses import dataclass, asdict

SCHEMA_VERSION = "1.0"

@dataclass
class Receipt:
    schema_version: str
    state_hash: str
    intent_hash: str
    authority_epoch: int
    corridor_id: str
    decision: str

    def canonical(self) -> bytes:
        return json.dumps(asdict(self), sort_keys=True).encode()

    def digest(self) -> str:
        return hashlib.sha256(self.canonical()).hexdigest()
