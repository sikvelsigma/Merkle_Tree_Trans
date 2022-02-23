from brownie import (
    accounts,
    config,
    network,
)

import json
from collections import defaultdict
import os

LOCAL_ENVIROMENTS = [
    "development",
    "ganache-local",
]


def get_account():
    if network.show_active() in LOCAL_ENVIROMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def read_json(name):
    with open(os.path.join("data", f"{name}.json")) as json_file:
        data = json.load(json_file)
        # Print the type of data variable
        converted_dict = defaultdict(dict)
        for key, item in data.items():
            for item2 in item:
                index = item2["index"]
                if key == "distribution":
                    converted_dict[index]["address"] = item2["address"]
                    converted_dict[index]["amount"] = int(item2["amount"]["hex"], 0)
                elif key == "privateKeys":
                    converted_dict[index]["privateKey"] = item2["privateKey"]

    data_to_hash = [None] * len(converted_dict)
    private_keys = [None] * len(converted_dict)
    for index, item in converted_dict.items():
        account = item["address"]
        amount = item["amount"]
        private_key = item["privateKey"]
        data_to_hash[index] = (index, account, amount)
        private_keys[index] = private_key
    return data_to_hash, private_keys
