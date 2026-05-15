import hashlib
import json
import numpy as np

np.set_printoptions(suppress=True)

# --- Constraint Manifold ---
def F(x):
    return np.sum(x**2) - 1.0

# --- Capacity Field ---
def capacity(x):
    return 1.2 - np.linalg.norm(x)

# --- Authority Token ---
class Authority:
    def __init__(self, scope=1.0):
        self.scope = scope

    def mutate(self, delta):
        self.scope += delta

    def valid(self):
        return self.scope > 0.5

# --- Commit Hash ---
def commit_hash(state, decision, parent=None):
    payload = {
        "state": state.tolist(),
        "decision": decision,
        "parent": parent
    }
    encoded = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()

# --- Projection Solver (Gradient Step) ---
def project_to_boundary(x, lr=0.05, steps=50):
    x_proj = x.copy()
    for _ in range(steps):
        grad = 2 * x_proj
        x_proj -= lr * grad
        if F(x_proj) <= 0:
            break
    return x_proj

# --- Fork Detection ---
def detect_fork(chain):
    return len(chain) != len(set(chain))

# --- Runtime Simulation ---
def simulate():
    np.random.seed(7)
    x = np.array([0.2, 0.1, 0.15])
    authority = Authority(scope=1.0)
    parent = None
    chain = []

    print("=== FULL EXECUTION FIELD PROOF ===\n")

    for step in range(10):
        drift = np.random.normal(0, 0.2, size=3)
        x = x + drift

        # Mid-state authority mutation
        if step == 4:
            authority.mutate(-0.6)

        fx = F(x)
        phi = capacity(x)

        decision = "EXECUTE"
        if not authority.valid() or fx > 0 or phi < 0:
            decision = "REFUSE"

        if decision == "REFUSE":
            x = project_to_boundary(x)

        h = commit_hash(x, decision, parent)
        chain.append(h)
        parent = h

        print(f"Step: {step}")
        print(f"F(x): {fx:.6f}")
        print(f"Phi: {phi:.6f}")
        print(f"Authority Valid: {authority.valid()}")
        print(f"Decision: {decision}")
        print(f"Fork Detected: {detect_fork(chain)}")
        print("-" * 60)

    # Replay Determinism
    np.random.seed(7)
    x_replay = np.array([0.2, 0.1, 0.15])
    authority_replay = Authority(scope=1.0)
    parent_replay = None

    for step in range(10):
        drift = np.random.normal(0, 0.2, size=3)
        x_replay = x_replay + drift
        if step == 4:
            authority_replay.mutate(-0.6)
        fx = F(x_replay)
        phi = capacity(x_replay)
        decision = "EXECUTE"
        if not authority_replay.valid() or fx > 0 or phi < 0:
            decision = "REFUSE"
            x_replay = project_to_boundary(x_replay)
        h = commit_hash(x_replay, decision, parent_replay)
        if h != chain[step]:
            print("Replay mismatch at step", step)
            return
        parent_replay = h

    print("Replay deterministic: True")

if __name__ == "__main__":
    simulate()
