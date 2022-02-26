from web3 import Web3
from scripts.misc import read_json

# from eth_abi.packed import encode_abi_packed
class MerkleTree:
    class Node:
        """
        Class for nodes of Merkle tree
        Nodes comparison is done by value
        """

        def __init__(self, value, left=None, right=None, id=None, parent=None):
            self.left = left
            self.right = right
            self.value = value
            self.parent = parent
            self.id = id

        def __gt__(self, other):
            return self.value > other.value

        def __lt__(self, other):
            return self.value < other.value

        def __ge__(self, other):
            return self.value >= other.value

        def __le__(self, other):
            return self.value <= other.value

        def __eq__(self, other):
            vc = self.value == other.value
            return vc

        def __str__(self):
            return self.value.hex()

    def pre_order(self, node, layer=0):
        """
        Pre-order binary tree search (from root to children)
        """
        if node:
            print_value = f"{node.id}:{node.value.hex()}"
            graphic = " " * 4 * layer
            print(f"{graphic}{print_value}")
            self.pre_order(node.left, layer + 1)
            self.pre_order(node.right, layer + 1)
        return ""

    def __str__(self):
        return self.pre_order(self.__root_node)

    def __init__(self, data, format, single_nodes_mode=0):
        """
        data is a list of values to hash together
        format is a list with Solidity types
        single_nodes_mode:
            0: single nodes are promoted
            1: single nodes are self-paired
            2: single nodes are added to the 1st in the next level
        """
        # hash initial nodes and store
        hash_data = self.list_to_keccak(data, format)
        self.initial_nodes = {}
        nodes = []
        for i, (elem, hash) in enumerate(zip(data, hash_data)):
            node = self.Node(hash, id=i)
            self.initial_nodes[elem] = node
            nodes.append(node)

        self.nodes_by_layer = []
        self.nodes_by_layer.append(nodes)

        # tree generation
        current_id = len(nodes) - 1
        while len(nodes) > 1:
            parents = []
            for i in range(0, len(nodes), 2):
                node1 = nodes[i]

                if i + 1 < len(nodes):
                    node2 = nodes[i + 1]
                else:
                    if single_nodes_mode == 0:
                        node2 = None
                    elif single_nodes_mode == 1:
                        node2 = nodes[i]
                    elif single_nodes_mode == 2:
                        parents.insert(0, node1)
                        nodes.pop(i)
                        continue

                if node2 is not None:
                    # smallest hash is always on the left leaf
                    if node1 > node2:
                        left = node2
                        right = node1
                    else:
                        left = node1
                        right = node2
                    p_hash = self.keccak(left.value + right.value)
                else:
                    # promote current hash to the next node for odd nodes
                    left = node1
                    right = None
                    p_hash = node1.value
                current_id += 1

                parents.append(self.Node(p_hash, left, right, current_id))
                node1.parent = parents[-1]
                if node2:
                    node2.parent = parents[-1]

            if parents:
                self.nodes_by_layer.append(parents)
            nodes = parents

        self.__root_node = nodes[0]

    @staticmethod
    def get_proof(node):
        """
        Get proof for a node by climbing up the tree and
        searching for neighbor nodes, returns Node objects
        """
        res = []
        current_node = node
        while current_node.parent:
            parent = current_node.parent
            if current_node is parent.left:
                neighbor = parent.right
            else:
                neighbor = parent.left
            if neighbor:
                res.append(neighbor)
            current_node = parent
        return res

    def get_proof_hashes(self, node):
        proof = self.get_proof(node)
        return [n.value for n in proof]

    def verify(self, proof, root, leaf):
        result_hash = leaf
        for hash in proof:
            if result_hash <= hash:
                result_hash = self.keccak(result_hash + hash)
            else:
                result_hash = self.keccak(hash + result_hash)
        return result_hash == root

    def print_ids_by_layer(self):
        for i, elem in enumerate(self.nodes_by_layer):
            st = ""
            for n in elem:
                c1 = n.left.id if n.left else ""
                c2 = n.right.id if n.right else ""
                st = st + f"   {n.id}({c1},{c2})"
            print(f"layer {i}: {st}")

    @property
    def root_node(self):
        return self.__root_node

    @property
    def merkle_root(self):
        return self.__root_node.value

    @staticmethod
    def keccak(inp):
        return Web3.keccak(inp)

    @staticmethod
    def list_to_keccak(inp, format):
        res = []
        for elem in inp:
            hash = Web3.solidityKeccak(format, elem)
            res.append(hash)
        return res


def main():
    data_to_hash, _ = read_json("rewardDistribution2")

    # for i in data_to_hash:
    #     print(f'{i[0]}  {i[1]}  {Web3.toHex(i[2])}')

    hash_tree = MerkleTree(
        data_to_hash, ["uint256", "address", "uint256"], single_nodes_mode=2
    )
    print(hash_tree)

    target_number = 14
    check_number = 14

    target = hash_tree.initial_nodes[data_to_hash[target_number]]
    # print(target)
    print(f"root: {hash_tree.merkle_root.hex()}")
    proof = hash_tree.get_proof_hashes(target)

    hash_tree.print_ids_by_layer()

    target_hash = hash_tree.initial_nodes[data_to_hash[check_number]].value
    is_in_a_tree = hash_tree.verify(proof, hash_tree.merkle_root, target_hash)
    print(
        f"verify item #{check_number} with proof from item #{target_number}: {is_in_a_tree}"
    )

    contract_root = Web3.toBytes(
        0x70b2f9fa327eddf705fca65be0b43300dee9c8f1ea76d32203695c863aa4d76b
    )
    
    # 0xAC1910A665AEB8BD47D75573DFCFE10582A33738B3FE8B12EEBA6A884AA86886
    print(f"check against contract root: {hash_tree.merkle_root == contract_root}")

# if __name__ == "__main__":
#     pass
    
