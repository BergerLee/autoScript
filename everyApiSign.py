# -------------------------------
# @Author : github@BergerLee https://github.com/BergerLee
# @Update by BergerLee
# @Time : 2023/12/14
# -------------------------------
# cron "10 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('EveryApi每日签到')

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书验证警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

login_url = 'https://q.icodef.com/api/v1/auth/login'

login_headers = {
    'Content-Type': 'application/json',
}

login_data = {
    'mobile': '14723555129',
    'password': 'XzHKLHyL4D8KyVr',
    'auto_login': True,
    'type': 'account',
}

login_response = requests.post(login_url, headers=login_headers, json=login_data)

cookie1, cookie2 = "", ""

if login_response.status_code == 200:
    cookie1 = login_response.headers.get('Set-Cookie').split(',')[0].split(';')[0]
    cookie2 = login_response.headers.get('Set-Cookie').split(',')[1].split(';')[0]

sign_url = 'https://q.icodef.com/api/v1/user/daily_sign'
sign_headers = {
    'cookie': f"{cookie1};{cookie2}" if cookie1 and cookie2 else ""
}

sign_response = requests.post(sign_url, headers=sign_headers, verify=False)
sign_response = sign_response.json()
print(sign_response)
