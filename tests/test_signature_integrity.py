from authority_signature import generate_keypair, sign_epoch, verify_signature


def test_signature_roundtrip():
    priv, pub = generate_keypair()
    msg = "epoch-test"
    sig = sign_epoch(priv, msg)
    assert verify_signature(pub, msg, sig), "Signature verification failed"
