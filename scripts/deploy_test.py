from brownie import (
    accounts,
    config,
    SimpleRewardDistributorFlat as Distributor,
    TestTokenWithNameAndSymbolFlat as Token,
)


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
    deploy_token()
