from scripts.helpful_scripts import get_account, encode_function_data
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def main():
    account = get_account()
    print(f"deploying to ${network.show_active()}")
    box = Box.deploy({"from": account})
    print(box.retrieve())

    proxy_admin = ProxyAdmin.deploy({"from": account})

    # initializer = box.store, 1 <-- leave blank for now VV
    box_encoded_intializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_intializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade to V2!")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())
