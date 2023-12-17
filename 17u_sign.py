# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2023-12-17
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


def sign(token):
    sign_url = "https://wx.17u.cn/wxmpsign/sign/saveSignInfo"
    headers = {
        "TC-MALL-USER-TOKEN": token
    }
    response = requests.post(sign_url, headers=headers, json={}, verify=False).json()
    print(response)
    if response['code'] == 200:
        return '[True]{}'.format(response.get('msg'))
    else:
        return '[False]{}'.format(response.get('msg'))


if __name__ == '__main__':
    user_token = os.getenv('user_token')
    notify.pushplus_bot("同程旅行签到提醒", sign(user_token))
