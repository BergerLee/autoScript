# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2024-09-20
# @Version: 1.0
# @Comment: 配置用户账号密码：key = hutue_account，value为你的账号密码，用|隔开
# -------------------------------
# cron "1 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('糊涂鳄每日签到')
import os
import requests
import notify

CHECKIN_URL = "https://hutue.cn/wp-admin/admin-ajax.php"
notify_title = "糊涂鳄签到提醒"


def sign_daily(user_cookie):
    header = {
        'Cookie': f'{user_cookie}'
    }
    request_data = {
        'action': 'user_qiandao'
    }
    print('开始执行签到...')
    try:
        checkin_response = requests.post(CHECKIN_URL, headers=header, data=request_data).json()
        if checkin_response['status'] == '0':
            return f'[False]签到失败，{checkin_response.get("msg")}!'
        else:
            return f'[True]签到成功，{checkin_response.get("msg")}!'
    except requests.RequestException as e:
        return f'[Error] Error fetching image: {e}'


def user_login(username, password):
    login_url = 'https://hutue.cn/wp-admin/admin-ajax.php'

    request_body = {
        'action': 'user_login',
        'username': username,
        'password': password,
    }

    print('开始登陆账号.....')
    try:
        login_response = requests.post(login_url, data=request_body)
        response_data = login_response.json()

        if response_data.get('status') != '1':
            return notify.pushplus_bot(notify_title, f'[False]登陆失败，{login_response.json().get("msg")}!')

        response_header = login_response.headers.get('Set-Cookie')
        logged_cookie = response_header.split(';')[-3].split(',')[1]

        if logged_cookie:
            print('登录成功，用户cookie获取成功！')
            return logged_cookie.strip()  # 返回 cookie 值
        else:
            return '登录cookie获取失败'
    except requests.RequestException as e:
        return f'[Error] 网络请求错误: {e}'
    except ValueError:
        return '[Error] 响应解析错误'


if __name__ == '__main__':
    user_account = os.getenv('hutue_account')
    username = user_account.split('|')[0]
    password = user_account.split('|')[1]
    if not username or not password:
        print('账号密码读取失败')
    user_cookie = user_login(username, password)
    print(user_cookie)
    if user_cookie:
        notify_content = sign_daily(user_cookie.strip())
        notify.pushplus_bot(notify_title, notify_content)
        print(notify_content)
