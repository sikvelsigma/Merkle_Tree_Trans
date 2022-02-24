# Merkle tree in Python for working with Solidity

Currently work-in-progress

Using:
> - ganache-cli (Node.js)
> 
> - brownie (Python)

Problems to solve:
- root hash doesn't match one in the contract
- ~~deploy and test transactions with Merkle tree on local testnet~~
- ~~deploy and test on Rinkeby~~
- ~~test on already deployed contracts~~

## About root hash not matching
I've tried several tree generation techniques that differ in an odd node handling:
 - promote an odd node to the next layer in the last position
 - pair an odd node with itself
 - insert an odd node into the back/front of the next layer
 - insert a new node from the first and an odd one into the back/front of the next layer

 None of these methods yielded the required root hash. I can only conclude that to replicate the same Merkle root I would need the original tree so I could match it with mine and find the exact method used to handle an odd node. I've also verified that my hash function gives the same result as Solidity for the sum of 2 hashes (use `brownie test` to check). 

 Aside from that, I've tested the deploy script on local net and Rinkbey (`deploy.py`), it works as intended. I've also tested the claim function on already deployed contracts (`claim_from_deployed.py`) and it also works.
 To deploy one needs to fill `.env` file with appropriate keys and use 
 `brownie run scripts/deploy.py --network rinkeby`
 to deploy to Rinkeby and claim from the account with 0 index.

 Use `brownie run scripts/claim_from_deployed.py --network rinkeby` with appropriate addresses from token and distributor contracts and desired account index to claim from an already deployed contracts.