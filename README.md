# Bind-Time Authority Proof

Executable demonstration of bind-time authority enforcement under mid-state mutation.

## Core Principle

Operational continuity is not proof of standing.
Authority must be re-evaluated at commit-time against current state invariants.

Consequence permission collapses discretely at the bind boundary.
Drift is continuous. Binding is not.

## Failure Class

Stable operation under decayed legitimating basis.

Advanced systems can remain:
- coherent
- deterministic
- authenticated
- operationally successful

while the legitimating basis for continuation has decayed beneath the runtime surface.

## Invariants

I1 — Bind-Time Authority Collapse  
If authority epoch at commit differs from authorization epoch, consequence binding must refuse.

I2 — Deterministic Replay  
Given identical state, authority, manifold definition, and history, decision outcomes must be identical.

I3 — No Resurrection Without Reissue  
Authority cannot be restored implicitly by geometric recovery. Standing requires explicit epoch increment.

I4 — Fork Detectability  
Commit chain mutation must be detectable.

## Proof Surfaces

- Manifold constraint F(x)=0
- Capacity field Φ
- Authority epoch semantics
- Gradient projection to nearest admissible surface
- Deterministic commit-chain hashing
- Adversarial drift injection
- Stress-run invariant validation

---

Deterministic. Replayable. Fail-closed.
