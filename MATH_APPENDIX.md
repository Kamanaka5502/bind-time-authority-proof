# Mathematical Appendix — Bind-Time Authority Fabric

## 1. State Manifold

Let S ⊂ R^n be the admissible state manifold.

Constraint function:

F : R^n → R

Admissible region:

S = { x ∈ R^n | F(x) ≤ 0 }

---

## 2. Capacity Field

Define Φ(x) as capacity surplus:

Φ(x) = C(x) − B(x)

Execution requires:

Φ(x) > 0

---

## 3. Standing Predicate

Standing is a time-local predicate:

Standing(x, A_e, C_scope) :=

F(x) ≤ 0 ∧ Φ(x) > 0 ∧ A_e.valid ∧ Scope(x) ⊂ C_scope

---

## 4. Collapse Rule

If Standing(x) = False

⇒ Decision = REFUSE

---

## 5. Deterministic Replay

Let T be transition operator.

Replay property:

T(x, intent) = x'

hash(x, intent, epoch) = receipt

Replay(x, intent) must reproduce receipt.

---

## 6. Non-Persistence Theorem

Standing(T0) ≠ Standing(C)

Therefore standing must be evaluated at bind-time C.
