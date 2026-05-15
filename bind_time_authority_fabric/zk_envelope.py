import hashlib

def generate_standing_proof(fx, phi, authority_epoch):
    payload = f"{round(fx,6)}|{round(phi,6)}|{authority_epoch}"
    return hashlib.sha256(payload.encode()).hexdigest()

def verify_standing_proof(fx, phi, authority_epoch, proof):
    expected = generate_standing_proof(fx, phi, authority_epoch)
    return expected == proof
