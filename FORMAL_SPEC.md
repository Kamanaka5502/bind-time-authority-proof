# Formal Specification — Bind-Time Authority Fabric

## 1. System Model

Let:

- S_t be system state at time t
- A_t be authority vector at time t
- M be proposed mutation
- B be the bind-time commit boundary

Execution is admitted iff standing holds at B.

---

## 2. Standing Invariant

Standing(S_t, A_t, M) == TRUE

Where standing requires:

1. Authority is current epoch-valid
2. Authority signature verifies
3. Mutation scope ⊆ authorized corridor
4. Ledger continuity intact
5. Deterministic replay hash matches

Violation of any clause => REFUSE

---

## 3. Bind-Time Condition

Bind(M) is permitted only if:

Standing(S_t, A_t, M) == TRUE

Permission prior to B is non-binding.

---

## 4. Collapse Condition

Authority collapses if:

- Epoch drift detected
- Signature invalid
- Mutation attempts replay divergence
- Corridor boundary exceeded
- Ledger Merkle root mismatch

Collapse forces fail-closed refusal.

---

## 5. Deterministic Replay Requirement

Replay(M, S_t, A_t) must produce identical receipt hash H.

If H' != H => execution invalid.

---

Core Principle:

Execution permission does not persist.
Standing must be proven at the moment consequence would bind.
