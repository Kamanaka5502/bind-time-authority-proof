# Invariant Specification

Let x ∈ ℝⁿ represent the system state vector.
Let F(x) be the admissibility constraint function.

Admissible region:
F(x) ≤ 0

Boundary:
F(x) = 0

Violation:
F(x) > 0

Between T0 and Tcommit, state may mutate continuously.

Resolution rule at Tcommit:

If F(x_commit) ≤ 0 → EXECUTE
If F(x_commit) > 0 → REFUSE

Continuity does not imply standing.
Binding is discrete.

Determinism requirement:
Given identical initial state, mutation sequence, and constraint parameters,
commit resolution and commit hash must be identical under replay.