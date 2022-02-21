from eth_abi.packed import encode_single_packed, encode_abi_packed
from web3 import Web3
index = 0
account = "0x1b324A4Ea3545d774b4c40A77ddf5F22370DE0a1"
amount = 0x1eca955e9b65e00000

hash = Web3.solidityKeccak(['uint256', 'address', 'uint256'], (index, account, amount))

packed = encode_abi_packed(['uint256', 'address', 'uint256'], (index, account, amount))
hash2 = Web3.keccak(packed)
hash3 = Web3.solidityKeccak(['uint256', 'address', 'uint256'], (index+1, account, amount))
# print(hash2.hex())
# print(hash3.hex())

# print(Web3.solidityKeccak(["bytes32", "bytes32"], (hash2, hash3)).hex())
# print(Web3.keccak(hash2 + hash3).hex())
# print(hash == hash2)

test1 = Web3.toBytes(0x5bdfe7b6d1c643ab3a2c651d2b868c7c7dc685db87db7f928e7488cdac82a292)
test2 = Web3.toBytes(0xe31b06a13cc4a4bc5f1b22ddfcaacf2910f5f6beb1d2191cd53297a4433ce1be)
print(Web3.keccak(test1 + test2).hex())