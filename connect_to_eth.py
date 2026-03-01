import json
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers.rpc import HTTPProvider


def connect_to_eth():
    """
    Connect to Ethereum mainnet
    """
    url = "https://mainnet.infura.io/v3/147858491d9b4b49828ae53fe87393fb"
    w3 = Web3(HTTPProvider(url))
    assert w3.is_connected(), f"Failed to connect to provider at {url}"
    return w3


def connect_with_middleware(contract_json):
    """
    Connect to BNB testnet and load MerkleValidator contract
    """
    # Load contract info
    with open(contract_json, "r") as f:
        d = json.load(f)["bsc"]
        address = d["address"]
        abi = d["abi"]

    # Connect to BNB testnet (opBNB)
    url = "https://bsc-testnet.infura.io/v3/147858491d9b4b49828ae53fe87393fb"
    w3 = Web3(HTTPProvider(url))
    assert w3.is_connected(), f"Failed to connect to provider at {url}"

    # Inject Proof-of-Authority middleware
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    # Create contract object
    contract = w3.eth.contract(address=address, abi=abi)

    return w3, contract


if __name__ == "__main__":
    connect_to_eth()
