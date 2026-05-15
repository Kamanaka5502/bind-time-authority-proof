from receipt_schema import Receipt, SCHEMA_VERSION
from hashlib import sha256


def simulate_node(state_hash, intent_hash, epoch, corridor, decision):
    r = Receipt(
        schema_version=SCHEMA_VERSION,
        state_hash=state_hash,
        intent_hash=intent_hash,
        authority_epoch=epoch,
        corridor_id=corridor,
        decision=decision
    )
    return r.digest()


def majority_agreement(nodes):
    counts = {}
    for n in nodes:
        counts[n] = counts.get(n, 0) + 1
    winner = max(counts.values())
    return winner > len(nodes) // 2
