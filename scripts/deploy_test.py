from brownie import (
    accounts,
    config,
    network,
    SimpleRewardDistributor as Distributor,
    TestTokenWithNameAndSymbol as Token,
    TestHash,
)
from web3 import Web3
from scripts.merkle_tree import MerkleTree
from scripts.misc import (
    LOCAL_ENVIROMENTS,
    get_account,
    read_json,
)

publish = config["networks"][network.show_active()].get("verify")


def deploy_hashtest():
    # account = accounts[0]
    account = get_account()
    # print(account)
    token = TestHash.deploy({"from": account}, publish_source=publish)
    return token


def get_hashtest_value(token=None):
    if not network.show_active() in LOCAL_ENVIROMENTS:
        hash = TestHash[-1].p_hash()
        print(hash)
    else:
        print(token.p_hash())


def deploy_token(total_supply):
    account = get_account()
    print(f"Token deploying token...")
    token = Token.deploy(
        total_supply, "TestToken", "TT", {"from": account}, publish_source=publish
    )
    print(f"Token deployed at {token.address}")
    print(f"Token supply: {token.totalSupply()}\n")
    # ts = token.somename(000, {"from": account})
    # ts.wait(1)
    return token


def deploy_distributor(token_address, root):
    account = get_account()
    print(f"Token deploying distributor...")
    distributor = Distributor.deploy(
        token_address, root, {"from": account}, publish_source=publish
    )
    print(f"Distributor deployed at {distributor.address}\n")
    return distributor


def transfer_to_distributor(token, distributor, amount):
    account = get_account()
    print(f"Transfering {amount} tokens to distributor...")
    tx = token.transfer(distributor.address, amount, {"from": account})
    tx.wait(1)
    balance = token.balanceOf(distributor.address)
    print(f"Balance of the distributor: {balance}\n")
    return tx


def claim_from_distributor(distributor, index, account, amount, proof):
    account_sender = get_account()
    print(f"Claiming {amount} tokens from: {account} (index: {index})...")
    tx = distributor.claim(index, account, amount, proof, {"from": account_sender})
    tx.wait(1)
    is_claimed = distributor.isClaimed(index)
    print(f"Claim successful: {is_claimed}\n")


def main():

    data_to_hash, private_keys_data = read_json("rewardDistribution2")

    merkle_tree = MerkleTree(data_to_hash, ["uint256", "address", "uint256"], 2)
    merkle_root = merkle_tree.merkle_root

    token_supply = Web3.toWei(1000000000, "ether")
    token = deploy_token(token_supply)
    distributor = deploy_distributor(token.address, merkle_root)
    transfer_to_distributor(token, distributor, token_supply)

    index = 0
    index, account, amount = data_to_hash[index]
    target_node = merkle_tree.initial_nodes[data_to_hash[index]]
    merkle_proof = merkle_tree.get_proof_hashes(target_node)
    is_in_a_tree = merkle_tree.verify(merkle_proof, merkle_root, target_node.value)

    claim = claim_from_distributor(distributor, index, account, amount, merkle_proof)
