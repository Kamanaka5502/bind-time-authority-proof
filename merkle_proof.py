from merkle_ledger import hash_leaf, hash_node


def build_proof(leaves, index):
    proof = []
    nodes = [hash_leaf(x) for x in leaves]
    idx = index
    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])
        sibling = idx ^ 1
        proof.append(nodes[sibling])
        idx = idx // 2
        nodes = [hash_node(nodes[i], nodes[i+1]) for i in range(0, len(nodes), 2)]
    return proof


def verify_proof(leaf, proof, root, index):
    computed = hash_leaf(leaf)
    idx = index
    for sibling in proof:
        if idx % 2 == 0:
            computed = hash_node(computed, sibling)
        else:
            computed = hash_node(sibling, computed)
        idx = idx // 2
    return computed == root
