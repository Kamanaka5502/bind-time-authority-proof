from advanced_execution_field import simulate


class Corridor:
    def __init__(self, name):
        self.name = name
        self.chain = []

    def run(self):
        self.chain = simulate()
        return self.chain


def run_isolated_corridors():
    corridors = [Corridor("A"), Corridor("B"), Corridor("C")]
    results = {}
    for c in corridors:
        results[c.name] = c.run()
    return results
