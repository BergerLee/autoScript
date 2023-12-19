# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2023-12-18
# @Version: 1.0
# @Comment: 需要user_token
# -------------------------------
# cron "5 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('同程旅行每日签到')
import urllib3
import os
import notify
import requests
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书验证警告
urllib3.disable_warnings(InsecureRequestWarning)

SIGN_URL = "https://wx.17u.cn/wxmpsign/sign/saveSignInfo"


def sign(token):
    headers = {
        "TC-MALL-USER-TOKEN": token
    }
    try:
        response = requests.post(SIGN_URL, headers=headers, json={}, verify=False).json()
        print(response)
        response_code = response.get('code', None)
        if response_code == 200:
            return f'[True]签到成功！获得里程x{response.get("data").get("signMileage")}'
        else:
            return f'[False]{response.get("msg", "Unknown error")}'
    except requests.RequestException as e:
        return f'[False]Error making the request: {e}'


if __name__ == '__main__':
    user_token = os.getenv('user_token')
    result_message = sign(user_token)
    notify.pushplus_bot("同程旅行签到提醒", result_message)
