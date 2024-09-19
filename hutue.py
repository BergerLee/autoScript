# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2024-09-19
# @Version: 1.0
# @Comment: 配置用户cookie：hutue_cookie
# -------------------------------
# cron "3 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('糊涂鳄每日签到')
import os
import requests
import notify

CHECKIN_URL = "https://hutue.cn/wp-admin/admin-ajax.php"
notify_title = "糊涂鳄签到提醒"


def sign_daily(user_cookie):
    header = {
        'cookie': user_cookie
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


if __name__ == '__main__':
    user_cookie = os.getenv('hutue_cookie')
    notify_content = sign_daily(user_cookie)
    print(notify_content)
    notify.pushplus_bot(notify_title, notify_content)
