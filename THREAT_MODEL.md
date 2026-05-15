# Threat Model — Bind-Time Authority Fabric

This threat model covers:
1. Cryptographic adversaries
2. Distributed state mutation adversaries
3. Autonomous / AI execution adversaries

---

# I. Cryptographic Threats

## 1. Key Forgery
Attempt to fabricate authority signatures.

Mitigation:
- Ed25519 verification
- Deterministic signature validation
- Reject on verification failure

## 2. Key Replay
Reuse of previously valid signatures under new state.

Mitigation:
- Epoch binding
- Standing token time-bound validation
- Receipt hash uniqueness requirement

## 3. Ledger Tampering
Modification of receipt history.

Mitigation:
- Merkle-root sealing
- Deterministic replay verification
- Hash chain integrity enforcement

---

# II. Distributed State Mutation Threats

## 4. Mid-State Drift
Authority valid at T0 but invalid at commit boundary.

Mitigation:
- Bind-time standing verification
- Epoch revalidation at B
- Fail-closed refusal

## 5. Corridor Escalation
Mutation attempts to exceed authorized scope.

Mitigation:
- Explicit corridor boundary checks
- Scope containment verification

## 6. Replay Divergence
Execution result differs from deterministic expectation.

Mitigation:
- Receipt hash recomputation
- Deterministic replay comparison
- Collapse on mismatch

---

# III. Autonomous / AI Execution Threats

## 7. Stale Authority Persistence
Agent acts under previously granted authority after drift.

Mitigation:
- Standing must be recomputed at bind-time
- Prior approval has no persistence

## 8. Recursive Escalation
Autonomous component modifies its own execution surface.

Mitigation:
- Corridor isolation
- Immutable authority roots
- Sovereign execution guard

## 9. Adversarial Mutation Injection
AI proposes mutation outside lawful envelope.

Mitigation:
- Admission gate before execution
- Explicit invariant validation
- Collapse on invariant violation

---

# IV. System Collapse Guarantees

If any invariant breaks:

System state -> REFUSE

No partial bind.
No degraded continuation.
No silent drift.

Fail-closed semantics are mandatory.

---

Core Security Principle:

Standing does not persist.
It must be proven at the moment consequence would bind.

Every threat reduces to failure of standing validation at B.
