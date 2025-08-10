import random

import primp
from eth_account import Account
from web3 import Web3
import cycle

CHAIN_ID = 6342  # From constants.py comment

# Contract addresses
WETH_CONTRACT = Web3.to_checksum_address("0x4eb2bd7bee16f38b1f4a0a5796fffd028b6040e9")
SPENDER_CONTRACT = Web3.to_checksum_address(
    "0x000000000022D473030F116dDEE9F6B43aC78BA3"
)  # Contract to approve for spending WETH
ROUTER_CONTRACT = Web3.to_checksum_address(
    "0xbeb0b0623f66be8ce162ebdfa2ec543a522f4ea6"
)  # Bebop router
CUSD_CONTRACT = Web3.to_checksum_address(
    "0xe9b6e75c243b6100ffcb1c66e8f78f96feea727f"
)  # cUSD token

# ABIs
WETH_ABI = [
    {
        "constant": False,
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "wad", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "type": "function",
    },
]

# ERC20 ABI for approve function
ERC20_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
]

# Constants
MAX_UINT256 = 2 ** 256 - 1  # Maximum uint256 value for unlimited approval

# Default swap amount in ETH (0.0000006 ETH)
DEFAULT_SWAP_AMOUNT_ETH = 0.0000006
RPC_URL = 'https://carrot.megaeth.com/rpc'
web3 = Web3(Web3.HTTPProvider(RPC_URL))


class Bebop:
    def __init__(self, address, private_key):
        self.address = address
        self.private_key = private_key

    def _eth_to_wei(self, eth_amount):
        """Convert ETH amount to wei"""
        return int(eth_amount * 10 ** 18)

    def swap_eth_to_weth(self):
        eth_balance_wei = web3.eth.get_balance(self.address)
        eth_balance = eth_balance_wei / 10 ** 18
        cycle.log_message(f"{self.address}账户eth余额：{eth_balance}")
        if eth_balance < 0:
            cycle.log_message("eth余额不足","error")
            return False
        percentage = random.uniform(5, 10)
        swap_amount = (eth_balance * percentage) / 100
        swap_amount = round(swap_amount, 8)
        if swap_amount < 0.00000001:
            swap_amount = 0.00000001
        cycle.log_message(f"{self.address}交换{swap_amount}eth到weth", "info")
        amount_wei = self._eth_to_wei(swap_amount)
        weth_contract = web3.eth.contract(address=WETH_CONTRACT, abi=WETH_ABI)
        tx_params = {
            "from": self.address,
            "value": amount_wei,
            "nonce": web3.eth.get_transaction_count(self.address),
            "chainId": CHAIN_ID,
            'gas': 100000,
            'gasPrice': web3.eth.gas_price
        }
        tx = weth_contract.functions.deposit().build_transaction(tx_params)
        signed_txn = web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        cycle.log_message(f"{self.address}|{swap_amount}eth交换至weth成功！交易哈希：{web3.to_hex(tx_hash)}","success")
        return True

    def swap_weth_to_eth(self):
        weth_contract = web3.eth.contract(address=WETH_CONTRACT, abi=WETH_ABI)
        weth_balance_wei = weth_contract.functions.balanceOf(self.address).call()
        weth_balance = weth_balance_wei / 10 ** 18
        cycle.log_message(f"{self.address}|weth余额{weth_balance}")
        if weth_balance < 0:
            cycle.log_message(f"{self.address}|weth余额不足", "error")
            return False
        if self.approve_weth():
            amount_wei = self._eth_to_wei(weth_balance)
            cycle.log_message(f"{self.address}交换{weth_balance}weth到eth", "info")
            function_selector = "0x2e1a7d4d"
            amount_hex = hex(amount_wei)[2:].zfill(
                64
            )
            withdraw_data = function_selector + amount_hex
            tx_params = {
                "from": self.address,
                "to": WETH_CONTRACT,
                "data": withdraw_data,
                "value": 0,
                "nonce": web3.eth.get_transaction_count(self.address),
                "chainId": CHAIN_ID,
                'gas': 100000,
                'gasPrice': web3.eth.gas_price
            }
            signed_tx = web3.eth.account.sign_transaction(tx_params, self.private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hex = tx_hash.hex()
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt["status"] == 1:
                cycle.log_message(f"{self.address}|{weth_balance}weth交换至eth成功！交易哈希：0x{tx_hex}", "success")
                return True
            else:
                cycle.log_message(f"{self.address}|{weth_balance}weth交换至eth失败！", "error")
                return False
        return False

    def approve_weth(self):
        try:
            cycle.log_message(f"{self.address}|执行无限授权weth")
            weth_contract = web3.eth.contract(address=WETH_CONTRACT, abi=WETH_ABI)
            tx_params = {
                "from": self.address,
                "nonce": web3.eth.get_transaction_count(self.address),
                "chainId": CHAIN_ID,
                'gas': 100000,
                'gasPrice': web3.eth.gas_price
            }
            tx = weth_contract.functions.approve(SPENDER_CONTRACT, MAX_UINT256).build_transaction(tx_params)
            signed_txn = web3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            cycle.log_message(f"{self.address}|weth无限授权成功！交易哈希：{web3.to_hex(tx_hash)}", "success")
            return True
        except Exception as e:
            cycle.log_message(f"{self.address}|weth无限授权失败！，错误原因：{e}", "error")
            return False


if __name__ == "__main__":
    bebop = Bebop(address="0x5095868e796279DC8fd677193B57808aC341cE09",
                  private_key="REDACTED_PRIVATE_KEY")
    cycle.log_message(bebop.swap_weth_to_eth())
