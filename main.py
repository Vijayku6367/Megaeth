import json
import random

import cycle
from faucet import megaeth_faucet
from bebop import bebop
from cap import cap
from gte import gte
from onchaingm import onchaingm
from teko import teko
from nacci import nacci_nft


def main():
    # 读取config.json文件
    with open('config.json', 'r') as f:
        config = json.load(f)
    api_key = config['api_key']
    ip_user = config['ip_user']
    ip_password = config['ip_password']
    tasks = config['task']
    is_random = config['is_random']
    # 读取wallets.txt文件
    with open('wallets.txt', 'r') as f:
        wallets = f.readlines()
    for wallet in wallets:
        try:
            random_tasks = tasks.copy()
            address, private_key = wallet.strip().split(":")
            # 判断tasks中是否有faucet，有就从中tasks中删除faucet
            if is_random:
                if 'faucet' in random_tasks:
                    random_tasks.remove('faucet')
                    # 调用faucet
                    cycle.log_message("随机任务优先执行官方领水", "info")
                    megaeth_faucet(address, ip_user, ip_password, api_key)
                random.shuffle(random_tasks)
            for task in random_tasks:
                try:
                    if task == 'bebop_swap_eth_to_weth':
                        my_bebop = bebop.Bebop(address, private_key)
                        my_bebop.swap_eth_to_weth()
                    elif task == 'bebop_swap_weth_to_eth':
                        my_bebop = bebop.Bebop(address, private_key)
                        my_bebop.swap_weth_to_eth()
                    elif task == 'cap_mint_cusd':
                        cap.mint_cusd(address, private_key)
                    elif task == 'gte_swap_token':
                        my_gte = gte.Gte(address, private_key)
                        my_gte.swap_token()
                    elif task == 'gte_swap_all_tokens_to_eth':
                        my_gte = gte.Gte(address, private_key)
                        my_gte.swap_all_tokens_to_eth()
                    elif task == 'onchaingm_send_gm':
                        onchaingm.send_gm(address, private_key)
                    elif task == 'teko_faucet':
                        my_teko = teko.Teko(address, private_key)
                        my_teko.faucet()
                    elif task == 'teko_stake':
                        my_teko = teko.Teko(address, private_key)
                        my_teko.stake()
                    elif task == 'teko_unstake':
                        my_teko = teko.Teko(address, private_key)
                        my_teko.unstake()
                    elif task == 'faucet':
                        megaeth_faucet(address, ip_user, ip_password, api_key)
                    elif task == 'nacci':
                        rarible = nacci_nft.Rarible(address, private_key)
                        rarible.mint_nft()
                    else:
                        cycle.log_message(f"任务{task}不存在", "error")
                except Exception as e:
                    cycle.log_message(f"{wallet}执行任务{task}错误：{e}", "error")
        except Exception as e:
            cycle.log_message(f"{wallet}执行错误：{e}", "error")


if __name__ == '__main__':
    main()
