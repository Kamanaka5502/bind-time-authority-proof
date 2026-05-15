import numpy as np
import hashlib
import json

# ============================================================
# SUBSTRATE MANIFOLD + ADVERSARIAL DRIFT + FORK DETECTION
# ============================================================

def F(x):
    # Implicit admissibility manifold F(x) = 0 boundary
    return float(np.sum(x**2) - 1.0)

def phi_capacity(x):
    return float(1.0 - np.linalg.norm(x))

def authority_rule(phi, step):
    # Mid-state authority mutation
    if step >= 4:
        return False
    return bool(phi > 0.2)

class CommitChain:
    def __init__(self):
        self.chain = []

    def tip(self):
        if not self.chain:
            return "GENESIS"
        return self.chain[-1]

    def add(self, payload):
        payload_str = json.dumps(payload, sort_keys=True)
        parent = self.tip()
        combined = parent + payload_str
        h = hashlib.sha256(combined.encode()).hexdigest()
        self.chain.append(h)
        return h

    def verify_no_fork(self):
        # deterministic rebuild
        test_chain = []
        parent = "GENESIS"
        for payload in self.payload_log:
            payload_str = json.dumps(payload, sort_keys=True)
            combined = parent + payload_str
            h = hashlib.sha256(combined.encode()).hexdigest()
            test_chain.append(h)
            parent = h
        return test_chain == self.chain

def project_to_boundary(x):
    norm = np.linalg.norm(x)
    if norm == 0:
        return x
    return x / norm

def run_simulation(adversarial=False):
    x = np.array([0.2, 0.1, 0.3])
    chain = CommitChain()
    chain.payload_log = []
    history = []

    for step in range(12):

        # adversarial drift injection (single dimension spike)
        if adversarial and step == 6:
            x[0] += 3.0

        f_val = F(x)
        phi = phi_capacity(x)
        authority_valid = authority_rule(phi, step)

        decision = "EXECUTE"
        if f_val > 0 or not authority_valid:
            decision = "REFUSE"

        if decision == "REFUSE":
            # gradient projection to nearest admissible surface
            x = project_to_boundary(x)

        payload = {
            "step": int(step),
            "x": [float(v) for v in x.tolist()],
            "F": float(round(float(f_val), 6)),
            "phi": float(round(float(phi), 6)),
            "authority": bool(authority_valid),
            "decision": str(decision)
        }

        chain.payload_log.append(payload)
        tip = chain.add(payload)

        history.append(
            (
                step,
                round(f_val, 6),
                round(phi, 6),
                authority_valid,
                decision,
                tip[:12],
            )
        )

        # deterministic drift
        x = x + np.array([0.05, -0.02, 0.03])

    replay_valid = chain.verify_no_fork()
    return history, replay_valid

# ============================================================
# MAIN
# ============================================================

print("=== BASE EXECUTION FIELD ===")
history, replay_valid = run_simulation(adversarial=False)

for h in history:
    print("Step:", h[0])
    print("F(x):", h[1])
    print("Phi:", h[2])
    print("Authority Valid:", h[3])
    print("Decision:", h[4])
    print("Chain Tip:", h[5])
    print("-" * 60)

print("Replay Deterministic:", replay_valid)

print("\n=== ADVERSARIAL DRIFT INJECTION ===")
history, replay_valid = run_simulation(adversarial=True)

for h in history:
    print("Step:", h[0])
    print("F(x):", h[1])
    print("Phi:", h[2])
    print("Authority Valid:", h[3])
    print("Decision:", h[4])
    print("Chain Tip:", h[5])
    print("-" * 60)

print("Replay Deterministic:", replay_valid)
