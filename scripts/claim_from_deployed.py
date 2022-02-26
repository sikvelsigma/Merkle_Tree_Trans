from brownie import Contract
from scripts.merkle_tree import MerkleTree
from scripts.misc import (
    LOCAL_ENVIROMENTS,
    read_json,
)
from scripts.deploy import claim_from_distributor

# unclaimed account (currently claimed 0-2 as of the time of this commit)
claim_index = 3

token_address = "0x7A8794A201FfCD45d51292471b9c0c5CF9A54485"
distributor_address = "0x4002a62CC0faB1c46c15963703Aa9e5c32c6A2F5"

def main():
    """Claim from already deployed contracts"""
    token = Contract.from_explorer(token_address)
    distributor = Contract.from_explorer(distributor_address)

    data_to_hash, private_keys_data = read_json("rewardDistribution2")

    merkle_tree = MerkleTree(data_to_hash, ["uint256", "address", "uint256"], 2)

    # try claim for unclaimed account
    index = claim_index
    index, account, amount = data_to_hash[index]
    target_node = merkle_tree.initial_nodes[data_to_hash[index]]
    merkle_proof = merkle_tree.get_proof_hashes(target_node)
    
    claim = claim_from_distributor(distributor, index, account, amount, merkle_proof)
    balance = token.balanceOf(distributor.address)
    print(f"Balance of the distributor: {balance} {token.symbol()}\n")

    # try claim for claimed account
    index = 0
    index, account, amount = data_to_hash[index]
    target_node = merkle_tree.initial_nodes[data_to_hash[index]]
    merkle_proof = merkle_tree.get_proof_hashes(target_node)

    claim = claim_from_distributor(distributor, index, account, amount, merkle_proof)
    balance = token.balanceOf(distributor.address)
    print(f"Balance of the distributor: {balance} {token.symbol()}\n")
