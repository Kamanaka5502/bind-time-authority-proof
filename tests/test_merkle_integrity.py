import hashlib
from advanced_execution_field import simulate
from ci_replay_check import merkle_root


def test_merkle_root_stable():
    chain1 = simulate()
    chain2 = simulate()

    root1 = merkle_root(chain1)
    root2 = merkle_root(chain2)

    assert root1 == root2, "Merkle root mismatch under deterministic replay"
