from advanced_execution_field import simulate

print("=== REHYDRATION TEST ===")

first_run = simulate()
second_run = simulate()

if first_run == second_run:
    print("Rehydration deterministic. Integrity holds.")
else:
    print("State divergence detected.")
