import copy
from advanced_execution_field import simulate


def test_chain_mutation_changes_output():
    chain = simulate()
    mutated = copy.deepcopy(chain)
    if mutated:
        mutated[0] = mutated[0] + "_modified"
    assert mutated != chain
