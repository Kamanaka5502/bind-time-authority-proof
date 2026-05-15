import hashlib
import json
import numpy as np
from standing_token import StandingToken, verify
from authority_epoch import AuthorityState

np.set_printoptions(suppress=True)

# -----------------------------
# Constraint Manifold F(x)=0
# -----------------------------
def F(x):
    return np.sum(x**2) - 1.0

# -----------------------------
# Capacity Field Phi
# -----------------------------
def capacity(x):
    return 1.2 - np.linalg.norm(x)

# -----------------------------
# Projection Solver (Gradient)
# -----------------------------
def project_to_boundary(x, lr=0.05, steps=100):
    x_proj = x.copy()
    for _ in range(steps):
        grad = 2 * x_proj
        x_proj -= lr * grad
        if F(x_proj) <= 0:
            break
    return x_proj

# -----------------------------
# Commit Hash
# -----------------------------
def commit_hash(state, decision, epoch, parent=None):
    payload = {
        "state": state.tolist(),
        "decision": decision,
        "epoch": epoch,
        "parent": parent
    }
    encoded = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()

# -----------------------------
# Runtime Simulation
# -----------------------------
def simulate(adversarial_step=6):
    np.random.seed(42)

    x = np.array([0.2, 0.1, 0.15])
    authority = AuthorityState(epoch=1, valid=True)
    parent = None
    chain = []

    print("=== BIND-TIME AUTHORITY ENFORCEMENT ===\n")

    for step in range(12):
        drift = np.random.normal(0, 0.15, size=3)

        if step == adversarial_step:
            drift += np.array([1.5, 0.0, 0.0])

        x = x + drift

        # Mid-state authority mutation
        if step == 4:
            authority.revoke()

        fx = F(x)
        phi = capacity(x)

        # Create bind-time standing token
        state_hash = hashlib.sha256(json.dumps(x.tolist()).encode()).hexdigest()
        token = StandingToken(authority.epoch, "global_scope", state_hash).sign()

        token_valid = verify(token)

        decision = "EXECUTE"

        # Bind-time collapse rule
        if (
            not authority.valid
            or fx > 0
            or phi < 0
            or not token_valid
            or token["payload"]["authority_epoch"] != authority.epoch
        ):
            decision = "REFUSE"

        if decision == "REFUSE":
            x = project_to_boundary(x)

        h = commit_hash(x, decision, authority.epoch, parent)
        chain.append(h)
        parent = h

        print(f"Step: {step}")
        print(f"F(x): {fx:.6f}")
        print(f"Phi: {phi:.6f}")
        print(f"Authority Epoch: {authority.epoch}")
        print(f"Authority Valid: {authority.valid}")
        print(f"Token Valid: {token_valid}")
        print(f"Decision: {decision}")
        print(f"Chain Tip: {h[:12]}")
        print("-" * 60)

    # Deterministic Replay Check
    np.random.seed(42)
    x_replay = np.array([0.2, 0.1, 0.15])
    authority_replay = AuthorityState(epoch=1, valid=True)
    parent_replay = None

    for step in range(12):
        drift = np.random.normal(0, 0.15, size=3)
        if step == adversarial_step:
            drift += np.array([1.5, 0.0, 0.0])
        x_replay = x_replay + drift
        if step == 4:
            authority_replay.revoke()
        fx = F(x_replay)
        phi = capacity(x_replay)
        state_hash = hashlib.sha256(json.dumps(x_replay.tolist()).encode()).hexdigest()
        token = StandingToken(authority_replay.epoch, "global_scope", state_hash).sign()
        token_valid = verify(token)
        decision = "EXECUTE"
        if (
            not authority_replay.valid
            or fx > 0
            or phi < 0
            or not token_valid
            or token["payload"]["authority_epoch"] != authority_replay.epoch
        ):
            decision = "REFUSE"
        if decision == "REFUSE":
            x_replay = project_to_boundary(x_replay)
        h = commit_hash(x_replay, decision, authority_replay.epoch, parent_replay)
        if h != chain[step]:
            print("Replay mismatch at step", step)
            return
        parent_replay = h

    print("Replay deterministic: True")


if __name__ == "__main__":
    simulate()
