# from eth_abi.packed import encode_single_packed, encode_abi_packed
from web3 import Web3
from brownie import accounts, TestHash
import pytest

index = 0
account = "0x1b324A4Ea3545d774b4c40A77ddf5F22370DE0a1"
amount = 0x1ECA955E9B65E00000


def test_hash_packed_vs_unpacked():
    """check a hash of a direct sum of hashes matches hash of packed hashes"""
    hash1 = Web3.solidityKeccak(
        ["uint256", "address", "uint256"], (index, account, amount)
    )
    hash2 = Web3.solidityKeccak(
        ["uint256", "address", "uint256"], (index + 1, account, amount)
    )
    sum1 = Web3.solidityKeccak(["bytes32", "bytes32"], (hash1, hash2))
    sum2 = Web3.keccak(hash1 + hash2)

    assert sum1 == sum2


def test_hash_vs_solidity():
    """check if python hash matches solidity hash"""
    account_deploy = accounts[0]

    test_hash = TestHash.deploy({"from": account_deploy})
    contract_hash = test_hash.p_hash()

    hash1 = Web3.solidityKeccak(
        ["uint256", "address", "uint256"], (index, account, amount)
    )
    hash2 = Web3.solidityKeccak(
        ["uint256", "address", "uint256"], (index + 1, account, amount)
    )
    sum1 = Web3.solidityKeccak(["bytes32", "bytes32"], (hash1, hash2))

    assert str(contract_hash) == str(sum1.hex())


def test_check_encode_pack_unpack():
    """checks if solidity gives different results for encode and encodePacked function"""

    account_deploy = accounts[0]
    if not TestHash:
        test_hash = TestHash.deploy({"from": account_deploy})
    else:
        test_hash = TestHash[-1]

    hash1 = test_hash.p_hash()
    hash2 = test_hash.p_hash2()

    assert not (hash1 == hash2)