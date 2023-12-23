# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2023-12-22
# @Version: 1.0
# @Comment: 配置邮箱和密码，例如单个账号：test@example.com#123456
#                           多个账号：test@example.com#123456&test2@example.com#123456
# -------------------------------
# cron "3 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('IKUUU VPN')
import os

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

import notify

# 禁用SSL证书验证警告
urllib3.disable_warnings(InsecureRequestWarning)

LOGIN_URL = "https://ikuuu.me/auth/login"
SIGN_URL = "https://ikuuu.me/user/checkin"
notify_title = "ikuuu机场签到提醒"


# 用户登录，获取cookie
def user_login(email, password):
    data = {
        "email": email,
        "passwd": password
    }
    try:
        login_response = requests.post(LOGIN_URL, data=data, verify=False)
        print(login_response.json())
        if login_response.json()["ret"] == 1:
            set_cookie = login_response.headers.get('Set-Cookie').split(',')
            uid = set_cookie[0].split(';')[0]
            email = set_cookie[2].split(';')[0]
            key = set_cookie[4].split(';')[0]
            ip = set_cookie[6].split(';')[0]
            expire_in = set_cookie[8].split(';')[0]
            user_cookie = "{};{};{};{};{}".format(uid, email, key, ip, expire_in)
            return user_cookie
        else:
            return False
    except requests.exceptions.RequestException as e:
        notify.pushplus_bot(notify_title, "[Error]登录请求发送失败，请检查")
        raise print(e)


def sign_daily(user_cookie):
    header = {
        'cookie': user_cookie
    }
    sign_response = requests.post(SIGN_URL, headers=header, verify=False).json()
    print(sign_response)
    if sign_response['ret'] == 1:
        return '[True]签到成功，{}'.format(sign_response['msg'])
    else:
        return '[False]{}'.format(sign_response['msg'])


if __name__ == '__main__':
    user_test = os.getenv('ikuuu')
    user_list = user_test.split("&")
    print(f"---------获取到了{len(user_list)}条用户信息---------")
    for user in user_list:
        user_info = user.split("#")
        print(f"正在执行{user_info[0]}........")
        cookie = user_login(user_info[0], user_info[1])
        if not cookie:
            notify.pushplus_bot(notify_title, "[Error]登陆失败，请检查账号！")
        else:
            notify_content = sign_daily(cookie)
            notify.pushplus_bot(notify_title, notify_content)
