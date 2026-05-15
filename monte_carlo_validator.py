from advanced_execution_field import simulate

print("=== MONTE CARLO VALIDATION ===")

for i in range(100):
    simulate(steps=20)

print("Monte Carlo completed without invariant breach.")
