import hashlib


def hash_leaf(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def hash_node(left: str, right: str) -> str:
    return hashlib.sha256((left + right).encode()).hexdigest()


class MerkleLedger:
    def __init__(self):
        self.leaves = []

    def append(self, receipt: str):
        self.leaves.append(hash_leaf(receipt))

    def root(self) -> str:
        nodes = self.leaves[:]
        if not nodes:
            return ""
        while len(nodes) > 1:
            if len(nodes) % 2 == 1:
                nodes.append(nodes[-1])
            nodes = [hash_node(nodes[i], nodes[i+1]) for i in range(0, len(nodes), 2)]
        return nodes[0]
