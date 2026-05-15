from advanced_execution_field import manifold_f, capacity_phi
from invariants import assert_bind_time_invariants

fx = manifold_f(0.5)
phi = capacity_phi(0.5)

authority_valid = False
token_epoch = 1
authority_epoch = 2

print("=== RESURRECTION ATTACK TEST ===")

try:
    decision = "EXECUTE"
    assert_bind_time_invariants(
        fx,
        phi,
        authority_valid,
        token_epoch,
        authority_epoch,
        decision
    )
    print("Resurrection succeeded (FAIL).")
except AssertionError as e:
    print("Resurrection blocked:", e)
