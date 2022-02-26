from brownie import Contract
from scripts.merkle_tree import MerkleTree
from scripts.misc import (
    LOCAL_ENVIROMENTS,
    read_json,
)
from scripts.deploy import check_claim

token_address = "0x7A8794A201FfCD45d51292471b9c0c5CF9A54485"
distributor_address = "0x4002a62CC0faB1c46c15963703Aa9e5c32c6A2F5"

def main():
    """Check claim for all accounts from the list"""
    token = Contract.from_explorer(token_address)
    distributor = Contract.from_explorer(distributor_address)

    data_to_hash, private_keys_data = read_json("rewardDistribution2")

    merkle_tree = MerkleTree(data_to_hash, ["uint256", "address", "uint256"], 2)

    for item in data_to_hash:
        index, account, amount = item
        target_node = merkle_tree.initial_nodes[item]
        merkle_proof = merkle_tree.get_proof_hashes(target_node)
        
        check_claim(distributor, index, account, amount, merkle_proof)


