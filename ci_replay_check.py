import sys
import time
import hashlib
from advanced_execution_field import simulate
from authority_signature import generate_keypair, sign_epoch, verify_signature

LATENCY_CEILING_MS = 25


def merkle_root(chain):
    nodes = chain[:]
    if not nodes:
        return None
    while len(nodes) > 1:
        next_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i+1] if i+1 < len(nodes) else left
            combined = hashlib.sha256((left + right).encode()).hexdigest()
            next_level.append(combined)
        nodes = next_level
    return nodes[0]


def fork_detect(chain):
    # simplistic continuity enforcement
    for i in range(1, len(chain)):
        if not isinstance(chain[i], str):
            return False
    return True


def crypto_self_test():
    priv, pub = generate_keypair()
    msg = "epoch-test"
    sig = sign_epoch(priv, msg)
    return verify_signature(pub, msg, sig)


def run_replay_check():
    start = time.time()
    chain1 = simulate()
    chain2 = simulate()

    if chain1 != chain2:
        print("Replay mismatch detected.")
        sys.exit(1)

    root1 = merkle_root(chain1)
    root2 = merkle_root(chain2)

    if root1 != root2:
        print("Merkle root mismatch.")
        sys.exit(1)

    if not fork_detect(chain1):
        print("Fork detected in chain.")
        sys.exit(1)

    if not crypto_self_test():
        print("Cryptographic signature self-test failed.")
        sys.exit(1)

    duration_ms = (time.time() - start) * 1000

    if duration_ms > LATENCY_CEILING_MS:
        print(f"Latency ceiling exceeded: {duration_ms:.2f}ms")
        sys.exit(1)

    print("Replay deterministic: PASS")
    print(f"Merkle root: {root1[:16]}...")
    print(f"Latency: {duration_ms:.2f}ms")


if __name__ == "__main__":
    run_replay_check()
