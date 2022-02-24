from brownie import (
    accounts,
    config,
    network,
    SimpleRewardDistributor as Distributor,
    TestTokenWithNameAndSymbol as Token,
)
from web3 import Web3
from scripts.merkle_tree import MerkleTree
from scripts.misc import (
    LOCAL_ENVIROMENTS,
    get_account,
    read_json,
)

# key for publishing contracts
publish = config["networks"][network.show_active()].get("verify")


def deploy_token(total_supply):
    """Deploy token contract"""
    account = get_account()
    print(f"Deploying token contract...")

    token = Token.deploy(
        total_supply, "TestToken", "TT", {"from": account}, publish_source=publish
    )

    print(f"Token deployed at {token.address}")
    print(f"Token supply: {token.totalSupply()}\n")

    return token


def deploy_distributor(token_address, root):
    """Deploy distributor contract"""
    account = get_account()

    print(f"Deploying distributor contract...")

    distributor = Distributor.deploy(
        token_address, root, {"from": account}, publish_source=publish
    )

    print(f"Distributor deployed at {distributor.address}\n")
    return distributor


def transfer_to_distributor(token, distributor, amount):
    """Transfer tokens to distributor contract"""
    account = get_account()

    print(f"Transfering {amount} tokens to distributor...")

    tx = token.transfer(distributor.address, amount, {"from": account})
    tx.wait(1)
    balance = token.balanceOf(distributor.address)

    print(f"Balance of the distributor: {balance} {token.symbol()}\n")
    return tx


def claim_from_distributor(distributor, index, account, amount, proof):
    """Claim from distributor to an account"""
    account_sender = get_account()

    print(f"Claiming {amount} tokens from: {account} (index: {index})...")
    tx = None
    try:
        tx = distributor.claim(index, account, amount, proof, {"from": account_sender})
        tx.wait(1)
    except Exception as err:
        print(f"Claiming Failed!")
        print(err)

    is_claimed = distributor.isClaimed(index)

    print(f"Drop claimed: {is_claimed}\n")
    return tx


def main():

    data_to_hash, private_keys_data = read_json("rewardDistribution2")

    merkle_tree = MerkleTree(data_to_hash, ["uint256", "address", "uint256"], 2)
    merkle_root = merkle_tree.merkle_root

    token_supply = Web3.toWei(1000000000, "ether")
    token = deploy_token(token_supply)
    distributor = deploy_distributor(token.address, merkle_root)
    transfer_to_distributor(token, distributor, token_supply)

    # claim from the 1st account
    index = 0
    index, account, amount = data_to_hash[index]
    target_node = merkle_tree.initial_nodes[data_to_hash[index]]
    merkle_proof = merkle_tree.get_proof_hashes(target_node)
    # is_in_a_tree = merkle_tree.verify(merkle_proof, merkle_root, target_node.value)

    claim = claim_from_distributor(distributor, index, account, amount, merkle_proof)

    balance = token.balanceOf(distributor.address)
    print(f"Balance of the distributor: {balance} {token.symbol()}\n")
