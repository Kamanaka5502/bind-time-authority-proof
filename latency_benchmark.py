import time
from advanced_execution_field import simulate

runs = 100
start = time.perf_counter()

for _ in range(runs):
    simulate(steps=5)

end = time.perf_counter()

avg = (end - start) / runs * 1000
print("Average commit latency (ms):", round(avg, 4))
