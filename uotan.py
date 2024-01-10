# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2024-1-10
# @Version: 1.0
# @Comment: 柚子社区每日签到
# -------------------------------
# cron "10 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('柚子社区')

import requests
import urllib3
import os
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

import notify

# 禁用SSL证书验证警告
urllib3.disable_warnings(InsecureRequestWarning)
login_page_url = "https://www.uotan.cn/login/"
login_url = "https://www.uotan.cn/login/login"
checkin_url = "https://www.uotan.cn/mjc-credits/clock"
home_url = "https://www.uotan.cn/"


def get_xf_user():
    print('-------------------------执行登录操作--------------------------')
    login_page = requests.get(login_page_url, verify=False)
    login_page_response_headers = login_page.headers.get('Set-Cookie').split(';')
    login_page_html = BeautifulSoup(login_page.text, "html.parser")

    xf_token = login_page_html.find('input', {'name': '_xfToken'}).get('value').strip()
    xf_csrf = login_page_response_headers[0].strip()
    xf_session = login_page_response_headers[2].split(',')[1].strip()

    print('xf_token:', xf_token)
    print('xf_csrf:', xf_csrf)
    print('xf_session:', xf_session)

    login_header = {
        'Cookie': f'{xf_csrf};{xf_session}'
    }

    login_data = {
        '_xfToken': xf_token,
        'login': os.getenv('login'),
        'password': os.getenv('password'),
        'remember': '1'
    }

    # # 执行登录操作
    login_response = requests.post(login_url, headers=login_header, data=login_data, verify=False,
                                   allow_redirects=False)
    print(login_response.headers)
    login_response_headers = login_response.headers.get('Set-Cookie')
    if login_response_headers is None:
        notify.pushplus_bot('柚子社区提醒', '未知错误！')
    xf_user = login_response_headers.split(';')[0]
    return xf_user


def checkin(xf_user):
    print('-------------------------执行签到操作--------------------------')
    home_page = requests.get(home_url, verify=False)
    home_page_response_headers = home_page.headers.get('Set-Cookie').split(';')
    home_page_html = BeautifulSoup(home_page.text, "html.parser")

    xf_token = home_page_html.find('input', {'name': '_xfToken'}).get('value').strip()
    xf_csrf = home_page_response_headers[0].strip()

    checkin_header = {
        'Cookie': f'{xf_csrf};{xf_user}'
    }

    chekin_data = {
        '_xfToken': xf_token
    }
    checkin_response = requests.post(checkin_url, headers=checkin_header, data=chekin_data, verify=False)
    if checkin_response.status_code == 200:
        notify.pushplus_bot('柚子社区', '签到成功！')


if __name__ == '__main__':
    login = os.getenv('login')
    password = os.getenv('password')
    if login and password:
        xf_user = get_xf_user()
        checkin(xf_user)
    else:
        print('请配置账号和密码')
