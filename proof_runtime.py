import hashlib
import json
import numpy as np

# Constraint function F(x) defining admissibility manifold
# Admissible if F(x) <= 0

def F(x):
    return np.sum(x**2) - 1.0  # unit sphere boundary


def commit_hash(state, decision, parent_hash=None):
    payload = {
        "state": state.tolist(),
        "decision": decision,
        "parent": parent_hash
    }
    encoded = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def simulate():
    np.random.seed(42)

    x = np.array([0.2, 0.3, 0.1])
    parent = None
    chain = []

    print("=== BIND-TIME AUTHORITY PROOF ===\n")

    for step in range(6):
        drift = np.random.normal(0, 0.15, size=3)
        x = x + drift

        fx = F(x)
        decision = "EXECUTE" if fx <= 0 else "REFUSE"

        h = commit_hash(x, decision, parent)
        chain.append(h)
        parent = h

        print(f"Step: {step}")
        print(f"F(x): {fx:.6f}")
        print(f"Decision: {decision}")
        print(f"Commit Hash: {h}")
        print("-" * 60)

    print("\n=== REPLAY VALIDATION ===")

    # Replay determinism test
    np.random.seed(42)
    x_replay = np.array([0.2, 0.3, 0.1])
    parent_replay = None

    for step in range(6):
        drift = np.random.normal(0, 0.15, size=3)
        x_replay = x_replay + drift
        fx = F(x_replay)
        decision = "EXECUTE" if fx <= 0 else "REFUSE"
        h = commit_hash(x_replay, decision, parent_replay)

        if h != chain[step]:
            print("Replay mismatch at step", step)
            return

        parent_replay = h

    print("Replay deterministic: True")


if __name__ == "__main__":
    simulate()
