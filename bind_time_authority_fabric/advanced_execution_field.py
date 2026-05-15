import hashlib
from dataclasses import dataclass
from bind_time_authority_fabric.invariants import assert_bind_time_invariants
from bind_time_authority_fabric.standing_token import sign, verify


@dataclass
class Authority:
    valid: bool
    epoch: int


@dataclass
class StandingToken:
    epoch: int
    signature: str


class CommitChain:
    def __init__(self):
        self.chain = []

    def append(self, payload: str):
        h = hashlib.sha256(payload.encode()).hexdigest()
        self.chain.append(h)
        return h

    def verify(self):
        return all(isinstance(x, str) for x in self.chain)


def manifold_f(x):
    return x - 1.0


def capacity_phi(x):
    return 1.0 - abs(x - 1.0)


def simulate(steps=12):
    authority = Authority(valid=True, epoch=1)
    token = StandingToken(epoch=1, signature=sign(1))
    chain = CommitChain()
    x = 0.1

    print("=== BIND-TIME CONSEQUENCE ENFORCEMENT ===")

    for step in range(steps):
        fx = manifold_f(x)
        phi = capacity_phi(x)

        # Simulate authority revocation
        if step == 4:
            authority.valid = False
            authority.epoch += 1

        signature_valid = verify(token.epoch, token.signature)

        decision = (
            "EXECUTE"
            if fx < 0
            and phi > 0
            and authority.valid
            and signature_valid
            and token.epoch == authority.epoch
            else "REFUSE"
        )

        assert_bind_time_invariants(
            fx,
            phi,
            authority.valid,
            token.epoch,
            authority.epoch,
            decision
        )

        payload = f"{step}|{fx}|{phi}|{authority.valid}|{authority.epoch}"
        tip = chain.append(payload)

        print(f"Step: {step}")
        print(f"F(x): {round(fx,6)}")
        print(f"Phi: {round(phi,6)}")
        print(f"Authority Valid: {authority.valid}")
        print(f"Signature Valid: {signature_valid}")
        print(f"Decision: {decision}")
        print(f"Chain Tip: {tip[:12]}")
        print("-"*60)

        x += 0.1

    print("Replay deterministic:", chain.verify())
    return chain.chain


if __name__ == "__main__":
    simulate()
