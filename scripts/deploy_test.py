from brownie import (
    accounts,
    config,
    network,
    SimpleRewardDistributor as Distributor,
    TestTokenWithNameAndSymbol as Token,
    TestHash
)

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_hashtest():
    # account = accounts[0]
    account = get_account()
    print(account)
    token = TestHash.deploy({"from": account})
    print(token)

def deploy_token():
    # account = accounts[0]
    account = accounts.add(config["wallets"]["from_key"])
    token = Token.deploy({"from": account})
    # ts = token.somename(000, {"from": account})
    # ts.wait(1)
    print(token)

def deploy_distributor():
    pass


def main():
    deploy_hashtest()
