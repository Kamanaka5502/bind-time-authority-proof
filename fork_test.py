from bind_time_authority_fabric import CommitChain


chain = CommitChain()
chain.append("request")
chain.append("decision")
print("=== FORK TEST ===")
assert chain.verify(), "Untampered chain should verify"
chain.chain[1] = "0" * 64
assert not chain.verify(), "Tampered chain should be rejected"
print("Fork mutation detected. Integrity holds.")
