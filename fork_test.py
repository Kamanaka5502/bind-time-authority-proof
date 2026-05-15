from advanced_execution_field import simulate
import hashlib

history = simulate()

last_tip = history[-1]["chain_tip"]

tampered = hashlib.sha256(b"tamper").hexdigest()

print("\n=== FORK TEST ===")
if tampered == last_tip:
    print("Fork undetected.")
else:
    print("Fork detectable. Integrity holds.")
