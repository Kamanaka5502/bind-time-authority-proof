def assert_bind_time_invariants(fx, phi, authority_valid, token_epoch, authority_epoch, decision):
    if decision == "EXECUTE":
        if not fx < 0:
            raise AssertionError("EXECUTE outside manifold")
        if not phi > 0:
            raise AssertionError("EXECUTE with negative capacity")
        if not authority_valid:
            raise AssertionError("EXECUTE without authority")
        if not token_epoch == authority_epoch:
            raise AssertionError("Token epoch mismatch")

    if not authority_valid and decision != "REFUSE":
        raise AssertionError("Invalid authority allowed EXECUTE")
