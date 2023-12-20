# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2023-12-18
# @Version: 2.0
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

SIGN_MINIAPP_URL = "https://wx.17u.cn/wxmpsign/sign/saveSignInfo"
LOTTERY_MINIAPP_URL = "https://wx.17u.cn/wcrewardshopapiv2/roulette/lottery"


# 微信小程序签到
def sign_miniapp(token):
    headers = {
        "TC-MALL-USER-TOKEN": token
    }
    try:
        response = requests.post(SIGN_MINIAPP_URL, headers=headers, json={}, verify=False).json()
        print(response)
        response_code = response.get('code', None)
        if response_code == 200:
            return f'[True]签到成功！获得里程x{response.get("data").get("signMileage")}'
        else:
            return f'[False]{response.get("msg", "Unknown error")}'
    except requests.RequestException as e:
        return f'[Error]Error making the request: {e}'


# 微信小程序每日抽奖
def lottery_miniapp(token):
    headers = {
        "userToken": token,
        "Content-Type": "application/json",
        "userKey": "ohmdTtzdJJ081-Cx6UA4_u7aU79w",
        "openId": "oOCyauCfN-bEDZEmKfUHcOi3U2Po"
    }
    body = {
        "osType": 0,
        "onceFlag": True
    }
    try:
        response = requests.post(LOTTERY_MINIAPP_URL, headers=headers, json=body, verify=False).json()
        print(response)
        response_code = response.get('hasSuccess', None)
        if response_code:
            return f'[True]今日抽奖获得{response.get("data")[0].get("prizeName")}'
        else:
            return f'[False]{response.get("resultInfo", "Unknown error")}'
    except requests.RequestException as e:
        return f'[Error]Error making the request: {e}'


if __name__ == '__main__':
    user_token = os.getenv('user_token')
    miniapp_lottery_result_message = lottery_miniapp(user_token)
    miniapp_sign_result_message = sign_miniapp(user_token)
    notify_content = f"今日签到状态：{miniapp_sign_result_message}\n今日抽奖状态：{miniapp_lottery_result_message}"
    notify.pushplus_bot("同程旅行提醒", notify_content)
