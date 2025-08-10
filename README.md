# MegaETH Bot

一个用于自动化执行MegaETH链上任务的Python工具。该工具支持多钱包批量操作，包括领水、代币兑换、NFT铸造等功能。

## 代理供应商注册链接

- NSTProxy: https://app.nstproxy.com/register?i=3tOiyf

## 图像识别服务

- yescaptcha：https://yescaptcha.com/i/lwZgQd

## 功能特性

- 多钱包批量操作支持
- 随机任务执行顺序
- 支持的任务类型：
  - Bebop代币兑换（ETH/WETH）
  - CAP协议CUSD铸造
  - GTE代币兑换
  - OnChainGM消息发送
  - Teko质押和领水
  - Nacci NFT铸造
  - MegaETH官方水龙头

## 安装说明

1. 克隆项目到本地：
```bash
git clone https://github.com/claire-cycle/megaeth_bot.git
cd cycle_megaeth
```

2. 创建并配置配置文件：
- 复制`config.json.example`为`config.json`
- 填入以下信息：
  ```json
  {
    "api_key": "你的yescaptcha API密钥",
    "ip_user": "代理用户名",
    "ip_password": "代理密码",
    "task": ["需要执行的任务列表"],
    "is_random": true
  }
  ```

3. 配置钱包文件：
- 在`wallets.txt`中按照以下格式添加钱包信息：
  ```
  钱包地址:私钥
  ```

## 使用方法

1. 运行主程序：
```bash
python main.py
```

2. 支持的任务类型：
- `bebop_swap_eth_to_weth`: Bebop ETH转WETH
- `bebop_swap_weth_to_eth`: Bebop WETH转ETH
- `cap_mint_cusd`: 铸造CUSD
- `gte_swap_token`: GTE代币兑换
- `gte_swap_all_tokens_to_eth`: GTE所有代币兑换为ETH
- `onchaingm_send_gm`: 发送GM消息
- `teko_faucet`: Teko领水
- `teko_stake`: Teko质押
- `teko_unstake`: Teko解除质押
- `faucet`: 官方水龙头领水
- `nacci`: Nacci NFT铸造

## 注意事项

- 使用前请确保已正确配置`config.json`和`wallets.txt`
- 建议使用代理IP以避免请求限制
- 请妥善保管私钥，不要泄露给他人
- 执行任务前请确保钱包中有足够的ETH支付gas费

## 许可证

本项目采用MIT许可证。详情请参见[LICENSE](LICENSE)文件。