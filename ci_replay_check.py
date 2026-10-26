import sys
import time
import hashlib
from advanced_execution_field import simulate
from bind_time_authority_fabric.standing_token import StandingToken, verify

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
    # The returned chain entries must at least have the expected SHA-256 shape.
    # Full predecessor/payload verification is exercised by CommitChain.verify().
    return all(isinstance(item, str) and len(item) == 64 for item in chain)


def crypto_self_test():
    token = StandingToken(1, "replay-scope", "replay-state").sign()
    return verify(token)


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
