"""Runnable public demonstrator for bind-time authority checks."""
import hashlib
from dataclasses import dataclass

from bind_time_authority_fabric.invariants import assert_bind_time_invariants
from bind_time_authority_fabric.standing_token import StandingToken, verify


@dataclass
class Authority:
    valid: bool
    epoch: int


class CommitChain:
    """Tamper-evident demonstration hash chain, not a production ledger."""

    def __init__(self):
        self.chain: list[str] = []
        self._payloads: list[str] = []

    @staticmethod
    def _digest(index: int, previous_hash: str, payload: str) -> str:
        material = f"{index}|{previous_hash}|{payload}".encode("utf-8")
        return hashlib.sha256(material).hexdigest()

    def append(self, payload: str) -> str:
        previous_hash = self.chain[-1] if self.chain else "GENESIS"
        digest = self._digest(len(self.chain), previous_hash, payload)
        self._payloads.append(payload)
        self.chain.append(digest)
        return digest

    def verify(self) -> bool:
        if len(self.chain) != len(self._payloads):
            return False
        previous_hash = "GENESIS"
        for index, (payload, observed_hash) in enumerate(zip(self._payloads, self.chain)):
            expected_hash = self._digest(index, previous_hash, payload)
            if not isinstance(observed_hash, str) or observed_hash != expected_hash:
                return False
            previous_hash = observed_hash
        return True


def manifold_f(x):
    return x - 1.0


def capacity_phi(x):
    return 1.0 - abs(x - 1.0)


def simulate(steps=12):
    authority = Authority(valid=True, epoch=1)
    token = StandingToken(
        authority_epoch=1,
        scope_hash="public-demo-scope",
        state_hash="public-demo-state",
    ).sign()
    chain = CommitChain()
    x = 0.1

    print("=== BIND-TIME CONSEQUENCE ENFORCEMENT ===")
    for step in range(steps):
        fx = manifold_f(x)
        phi = capacity_phi(x)

        # Revoke after issuing the token; old standing must not inherit the new epoch.
        if step == 4:
            authority.valid = False
            authority.epoch += 1

        signature_valid = verify(token)
        token_epoch = token["payload"]["authority_epoch"]
        decision = (
            "EXECUTE"
            if fx < 0
            and phi > 0
            and authority.valid
            and signature_valid
            and token_epoch == authority.epoch
            else "REFUSE"
        )

        assert_bind_time_invariants(
            fx, phi, authority.valid, token_epoch, authority.epoch, decision
        )
        payload = f"{step}|{fx}|{phi}|{authority.valid}|{authority.epoch}"
        tip = chain.append(payload)

        print(f"Step: {step}")
        print(f"F(x): {round(fx, 6)}")
        print(f"Phi: {round(phi, 6)}")
        print(f"Authority Valid: {authority.valid}")
        print(f"Signature Valid: {signature_valid}")
        print(f"Decision: {decision}")
        print(f"Chain Tip: {tip[:12]}")
        print("-" * 60)
        x += 0.1

    print("Chain integrity verified:", chain.verify())
    return chain.chain


if __name__ == "__main__":
    simulate()
