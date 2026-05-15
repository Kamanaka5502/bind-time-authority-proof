import numpy as np
import hashlib
import json
import copy
import random

# ============================================================
# SOVEREIGN EXECUTION FIELD
# A) Standing Epoch Model
# B) Hard Invariants
# C) Stress Runner
# D) Deterministic Replay + Fork Detection
# ============================================================


# -----------------------------
# Manifold Constraint F(x) = 0
# -----------------------------
def F(x):
    # implicit constraint surface (quadratic bowl offset)
    return np.dot(x, x) - 1.0


# -----------------------------
# Capacity Field Phi
# -----------------------------
def Phi(x):
    return 1.0 - abs(F(x))


# -----------------------------
# Authority Model with Epoch
# -----------------------------
class AuthorityModel:
    def __init__(self):
        self.valid = True
        self.epoch = 1

    def revoke(self):
        self.valid = False

    def reissue(self):
        self.valid = True
        self.epoch += 1


# -----------------------------
# Commit Chain
# -----------------------------
class CommitChain:
    def __init__(self):
        self.chain = []

    def tip(self):
        return self.chain[-1]["hash"] if self.chain else "GENESIS"

    def add(self, payload):
        parent = self.tip()
        blob = json.dumps(payload, sort_keys=True)
        h = hashlib.sha256((parent + blob).encode()).hexdigest()
        self.chain.append({
            "hash": h,
            "parent": parent,
            "payload": payload
        })
        return h

    def detect_fork(self):
        seen = set()
        for block in self.chain:
            if block["hash"] in seen:
                return True
            seen.add(block["hash"])
        return False


# -----------------------------
# Nearest Admissible Projection
# -----------------------------
def project_to_boundary(x):
    grad = 2 * x
    val = F(x)
    if np.linalg.norm(grad) == 0:
        return x
    return x - (val / np.dot(grad, grad)) * grad


# -----------------------------
# Hard Invariant Assertions
# -----------------------------
def assert_invariants(Fx, phi, authority_valid, decision, previous_decision, standing_epoch_before, standing_epoch_now):

    # EXECUTE only allowed if:
    if decision == "EXECUTE":
        assert Fx < 0, "Invariant violation: EXECUTE outside manifold"
        assert phi > 0, "Invariant violation: EXECUTE with negative capacity"
        assert authority_valid, "Invariant violation: EXECUTE without authority"

        # No resurrection without epoch increase
        if previous_decision == "REFUSE" and standing_epoch_now == standing_epoch_before:
            raise AssertionError("Invariant violation: Authority resurrection without reissue")

    # REFUSE must occur if authority invalid
    if not authority_valid:
        assert decision == "REFUSE", "Invariant violation: Invalid authority allowed EXECUTE"


# -----------------------------
# Simulation Core
# -----------------------------
def run_simulation(adversarial=False, stress=False):

    np.random.seed(42)
    random.seed(42)

    x = np.array([0.3, 0.4])
    authority = AuthorityModel()
    chain = CommitChain()

    history = []
    previous_decision = None
    standing_epoch_before = authority.epoch

    steps = 50 if stress else 12

    for step in range(steps):

        # Drift
        if adversarial and step == 6:
            x += np.array([10.0, 0.0])
        else:
            x += np.array([0.05, -0.02])

        # Optional random noise in stress mode
        if stress:
            x += np.random.normal(0, 0.01, size=2)

        Fx = F(x)
        phi = Phi(x)

        # Revoke authority mid-state
        if step == 4:
            authority.revoke()

        # Decision logic
        if Fx < 0 and phi > 0 and authority.valid:
            decision = "EXECUTE"
        else:
            decision = "REFUSE"

        # Enforce invariants
        assert_invariants(
            Fx, phi, authority.valid,
            decision,
            previous_decision,
            standing_epoch_before,
            authority.epoch
        )

        payload = {
            "step": step,
            "Fx": float(Fx),
            "phi": float(phi),
            "authority": authority.valid,
            "epoch": authority.epoch,
            "decision": decision
        }

        tip = chain.add(payload)

        history.append((step, Fx, phi, authority.valid, decision, tip[:12]))

        # Projection if outside
        if Fx > 0:
            x = project_to_boundary(x)

        previous_decision = decision
        standing_epoch_before = authority.epoch

    # Replay Determinism
    replay_chain = CommitChain()
    for block in chain.chain:
        replay_chain.add(block["payload"])

    replay_valid = (
        replay_chain.chain[-1]["hash"] == chain.chain[-1]["hash"]
    )

    fork_detected = chain.detect_fork()

    return history, replay_valid, fork_detected


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=== BASE EXECUTION FIELD ===")
    history, replay_valid, fork = run_simulation()

    for h in history:
        print("Step:", h[0])
        print("F(x):", round(h[1], 6))
        print("Phi:", round(h[2], 6))
        print("Authority Valid:", h[3])
        print("Decision:", h[4])
        print("Chain Tip:", h[5])
        print("-" * 60)

    print("Replay Deterministic:", replay_valid)
    print("Fork Detected:", fork)

    print("\n=== ADVERSARIAL DRIFT INJECTION ===")
    history, replay_valid, fork = run_simulation(adversarial=True)

    for h in history:
        print("Step:", h[0])
        print("F(x):", round(h[1], 6))
        print("Phi:", round(h[2], 6))
        print("Authority Valid:", h[3])
        print("Decision:", h[4])
        print("Chain Tip:", h[5])
        print("-" * 60)

    print("Replay Deterministic:", replay_valid)
    print("Fork Detected:", fork)

    print("\n=== STRESS RUN (50 steps randomized drift) ===")
    history, replay_valid, fork = run_simulation(stress=True)

    print("Final Step:", history[-1][0])
    print("Replay Deterministic:", replay_valid)
    print("Fork Detected:", fork)

