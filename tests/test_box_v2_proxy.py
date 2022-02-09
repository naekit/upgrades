from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import (
    Box,
    BoxV2,
    exceptions,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
)
import pytest


def test_proxy_upgrades():
    # Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )

    # Act deploy boxv2 -- should revert
    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    # Assert - test to make sure function doesnt work w/o upgrade
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    # Arrange
    upgrade(
        account,
        proxy,
        box_v2.address,
        proxy_admin_contract=proxy_admin,
    )
    # Make sure we are still at 0
    assert proxy_box.retrieve() == 0
    # Act
    proxy_box.increment({"from": account})
    # Assert
    assert proxy_box.retrieve() == 1
