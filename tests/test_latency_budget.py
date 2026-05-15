import time
from advanced_execution_field import simulate


def test_latency_under_25ms():
    start = time.time()
    simulate()
    duration_ms = (time.time() - start) * 1000
    assert duration_ms < 25, f"Latency exceeded: {duration_ms:.2f}ms"
