from base64 import encode
from brownie import accounts, network, config
import eth_utils


LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "mainnet-fork",
    "mainnet-fork-dev",
    "development",
    "ganache-local",
]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def encode_function_data(initializer=None, *args):
    """
    Encodes the Function call so we can work with an initializer:

    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        the intializer function we want to call e.g.: "box.store".
        defaults to None

        args (Any, optional):
        The arguments to pass to the initializer function

    Returns:
        [bytes]: Return encoded bytes

    """

    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    tx = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            tx = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            tx = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            tx = proxy.upgradeToAndCall(
                new_implementation_address, encoded_function_call, {"from": account}
            )
        else:
            tx = proxy.upgradeTo(new_implementation_address, {"from": account})
    return tx
