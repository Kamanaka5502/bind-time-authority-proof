def assert_bind_time_invariants(
    fx,
    phi,
    authority_valid,
    token_epoch,
    authority_epoch,
    decision
):
    if decision == "EXECUTE":
        assert fx < 0, "Invariant violation: EXECUTE outside manifold"
        assert phi > 0, "Invariant violation: EXECUTE with negative capacity"
        assert authority_valid, "Invariant violation: EXECUTE without authority"
        assert token_epoch == authority_epoch, "Invariant violation: Token epoch mismatch"

    if not authority_valid:
        assert decision == "REFUSE", "Invariant violation: Invalid authority allowed EXECUTE"
