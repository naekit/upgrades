from scripts.helpful_scripts import get_account
from brownie import network, Box


def main():
    account = get_account()
    print(f"deploying to ${network.show_active()}")
    box = Box.deploy({"from": account})
    print(box.retrieve())
