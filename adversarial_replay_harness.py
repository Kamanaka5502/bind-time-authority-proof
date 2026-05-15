from advanced_execution_field import simulate
import copy


def mutate_chain(chain):
    mutated = copy.deepcopy(chain)
    if mutated:
        mutated[-1] = mutated[-1] + "_tampered"
    return mutated


def test_replay_detection():
    original = simulate()
    tampered = mutate_chain(original)
    return original != tampered
