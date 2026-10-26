"""Deterministic digest utility for the public demonstrator.

Despite the historical module name, this is NOT a zero-knowledge proof:
it has no prover/verifier protocol, circuit, or private/public-input model.
The digest is a reproducibility checksum, not evidence of authority by itself.
"""
import hashlib


def generate_standing_proof(fx, phi, authority_epoch):
    """Return a deterministic SHA-256 digest; this is not a ZK proof."""
    payload = f"{round(fx, 6)}|{round(phi, 6)}|{authority_epoch}"
    return hashlib.sha256(payload.encode()).hexdigest()


def verify_standing_proof(fx, phi, authority_epoch, proof):
    """Check digest equality for identical inputs; not cryptographic authority."""
    expected = generate_standing_proof(fx, phi, authority_epoch)
    return expected == proof
