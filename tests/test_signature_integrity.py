from bind_time_authority_fabric.standing_token import StandingToken, verify


def test_signature_roundtrip():
    token = StandingToken(1, "scope-hash", "state-hash").sign()
    assert verify(token), "Signature verification failed"


def test_signature_rejects_payload_tampering():
    token = StandingToken(1, "scope-hash", "state-hash").sign()
    token["payload"]["authority_epoch"] = 2
    assert not verify(token), "Tampered token payload must fail verification"
