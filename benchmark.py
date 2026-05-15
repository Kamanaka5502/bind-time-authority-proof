import time
from advanced_execution_field import simulate


def benchmark(runs=100):
    start = time.time()
    for _ in range(runs):
        simulate()
    end = time.time()
    print(f"Runs: {runs}")
    print(f"Total time: {end - start:.6f}s")
    print(f"Avg per run: {(end - start)/runs:.6f}s")


if __name__ == "__main__":
    benchmark()
