import hashlib
import json
import numpy as np

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
# Authority Object
# -----------------------------
class Authority:
    def __init__(self, scope=1.0):
        self.scope = scope

    def mutate(self, delta):
        self.scope += delta

    def valid(self):
        return self.scope > 0.5

# -----------------------------
# Hysteresis Envelope
# -----------------------------
class Hysteresis:
    def __init__(self, epsilon=0.02):
        self.epsilon = epsilon
        self.last_decision = None

    def stabilize(self, fx):
        if abs(fx) < self.epsilon and self.last_decision:
            return self.last_decision
        return None

# -----------------------------
# Projection Solver
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
def commit_hash(state, decision, parent=None):
    payload = {
        "state": state.tolist(),
        "decision": decision,
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
    authority = Authority(scope=1.0)
    hysteresis = Hysteresis(epsilon=0.03)
    parent = None
    chain = []

    print("=== ADVANCED EXECUTION FIELD PROOF ===\n")

    for step in range(12):
        drift = np.random.normal(0, 0.15, size=3)

        # Adversarial spike injection
        if step == adversarial_step:
            drift += np.array([1.5, 0.0, 0.0])

        x = x + drift

        # Mid-state authority mutation
        if step == 4:
            authority.mutate(-0.7)

        fx = F(x)
        phi = capacity(x)

        decision = "EXECUTE"

        stabilized = hysteresis.stabilize(fx)
        if stabilized:
            decision = stabilized
        else:
            if not authority.valid() or fx > 0 or phi < 0:
                decision = "REFUSE"

        hysteresis.last_decision = decision

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
        print(f"Chain Tip: {h[:12]}")
        print("-" * 60)

    # Replay Determinism Check
    np.random.seed(42)
    x_replay = np.array([0.2, 0.1, 0.15])
    authority_replay = Authority(scope=1.0)
    hysteresis_replay = Hysteresis(epsilon=0.03)
    parent_replay = None

    for step in range(12):
        drift = np.random.normal(0, 0.15, size=3)
        if step == adversarial_step:
            drift += np.array([1.5, 0.0, 0.0])
        x_replay = x_replay + drift
        if step == 4:
            authority_replay.mutate(-0.7)
        fx = F(x_replay)
        phi = capacity(x_replay)
        decision = "EXECUTE"
        stabilized = hysteresis_replay.stabilize(fx)
        if stabilized:
            decision = stabilized
        else:
            if not authority_replay.valid() or fx > 0 or phi < 0:
                decision = "REFUSE"
        hysteresis_replay.last_decision = decision
        if decision == "REFUSE":
            x_replay = project_to_boundary(x_replay)
        h = commit_hash(x_replay, decision, parent_replay)
        if h != chain[step]:
            print("Replay mismatch at step", step)
            return
        parent_replay = h

    print("Replay deterministic: True")

if __name__ == "__main__":
    simulate()
