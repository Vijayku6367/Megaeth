from curl_cffi import requests

import cycle


def megaeth_faucet(address, ip_user, ip_password, api_key):
    try:
        proxy = cycle.get_proxy(ip_user,ip_password)
        cycle.log_message(f"{address}|使用代理{proxy}进行官方领水", "process")
        url = "https://carrot.megaeth.com/claim"
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,zh-TW;q=0.6,zh;q=0.5",
            "content-type": "text/plain;charset=UTF-8",
            "origin": "https://testnet.megaeth.com",
            "priority": "u=1, i",
            "referer": "https://testnet.megaeth.com/",
            "sec-ch-ua": '"Chromium";v="131", "Not:A-Brand";v="24", "Google Chrome";v="131"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }
        # cf_token = cycle.get_captcha(api_key, "https://testnet.megaeth.com/", "0x4AAAAAABA4JXCaw9E2Py-9")
        cf_token = cycle.get_captcha_no_api()
        data = f'{{"addr":"{address}","token":"{cf_token}"}}'
        response = requests.post(url, headers=headers, data=data, proxies=proxy)
        res = response.json()
        response_text = response.text
        if res['success']:
            cycle.log_message(f"{address}|官方领水成功", "success")
            return True
        if "used Cloudflare to restrict access" in response_text:
            cycle.log_message(f"{address}|当前ip已被Cloudflare加入黑名单", "error")
            return True
        if "less than 24 hours have passed" in response_text:
            cycle.log_message(f"{address}|官方领水失败，24小时内只能领一次水，请切换ip", "error")
            return True
        if '"Success"' in response_text:
            cycle.log_message(
                f"[{address}]|领水成功",
                "success"
            )
            return True
        if "Claimed already" in response_text:
            cycle.log_message(
                f"[{address}]|已经领过水了",
            )
            return True

        else:
            cycle.log_message(
                f"[{address}]|领水失败！失败信息: {response_text}"
            )
            return False
    except Exception as e:
        cycle.log_message(f"[{address}]|领水失败！失败信息: {e}", "error")
        return False
