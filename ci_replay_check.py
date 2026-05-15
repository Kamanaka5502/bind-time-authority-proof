import sys
import time

from advanced_execution_field import simulate


def run_replay_check():
    start = time.time()
    chain1 = simulate()
    chain2 = simulate()

    if chain1 != chain2:
        print("Replay mismatch detected.")
        sys.exit(1)

    duration_ms = (time.time() - start) * 1000

    # Latency ceiling (example threshold: 100ms)
    if duration_ms > 100:
        print(f"Latency ceiling exceeded: {duration_ms:.2f}ms")
        sys.exit(1)

    print("Replay deterministic: PASS")
    print(f"Latency: {duration_ms:.2f}ms")


if __name__ == "__main__":
    run_replay_check()
