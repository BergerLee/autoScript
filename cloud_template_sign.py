# -------------------------------
# @Author: BergerLee https://github.com/BergerLee
# @Time: 2023/12/15
# @Version: 2.0
# @Comment: 需要在环境变量中配置cloud_template_data信息，例如：admin-123456
# -------------------------------
# cron "1 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('模板云每日签到')

import time
import notify
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlencode
import os
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书验证警告
InsecureRequestWarning.disabled = True

login_page_url = "https://www.22vd.com/login"

login_url = ("https://www.22vd.com/wp-admin/admin-ajax.php?action=xh_social_add_ons_login&tab=login"
             "&xh_social_add_ons_login={}&notice_str={}&hash={}")

sign_url = "https://www.22vd.com/wp-admin/admin-ajax.php"

continue_sign_day_url = "https://www.22vd.com/sign"

notify_title = "模板云签到提醒"


# 获取用户cookie
def get_user_cookie():
    try:
        # 访问登陆页面
        login_page_response = requests.get(login_page_url, verify=False)
        login_page_soup = BeautifulSoup(login_page_response.text, 'html.parser')
        # 提取登录部分的脚本
        login_page_script = login_page_soup.find_all('script', type='text/javascript')[4].text
        # 使用正则表达式提取 xh_social_add_ons_login，notice_str，hash 的值
        xh_social_add_ons_login = re.search(r'xh_social_add_ons_login=(.*?)&', login_page_script).group(1)
        notice_str = re.search(r'notice_str=(.*?)&', login_page_script).group(1)
        hash_value = re.search(r'hash=(.*?)\'', login_page_script).group(1)
        # 构造登录请求url
        login_url_handle = login_url.format(xh_social_add_ons_login, notice_str, hash_value)
        # 构造请求体
        login_data = os.getenv('cloud_template_data').split('-')
        data = {
            'login_name': login_data[0].strip(),
            'login_password': login_data[1].strip()
        }
        # 构造请求头
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # 登录
        login_response = requests.post(login_url_handle, data=urlencode(data), headers=headers, verify=False)
        # 返回cookie
        user_cookie = login_response.headers.get('Set-Cookie').split(';')[10].split(',')[1].strip()
        if user_cookie:
            return user_cookie
        else:
            notify.pushplus_bot(notify_title, "[Error]未获取到您的Cookie信息，请检查！")
            exit(1)
    except requests.exceptions.RequestException as e:
        notify.pushplus_bot(notify_title, "[Error]登录请求发送失败，请检查")
        raise print(e)


# 执行签到操作
def daily_sign(user_cookie):
    headers = {
        "Cookie": user_cookie,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    from_data = {
        "action": "sign_ajax",
        "ajax_date": "sign"
    }
    try:
        sign_response = requests.post(sign_url, headers=headers, data=urlencode(from_data), verify=False).json()
        if sign_response == 1 or sign_response == 3:
            time.sleep(2)
            continue_day = get_user_continue_sign_day(user_cookie)
            if continue_day:
                return '[Success]签到成功！连续签到：{}天！'.format(continue_day)
            else:
                return '[Success]签到成功！连续签到：undefined'
        elif sign_response == 2:
            return '[Info]今日已经签到过了！'
        elif sign_response == 4:
            return '[Info]签到成功，您的连续签到已经被重置了！'
        elif sign_response == 5:
            return '[Error]请先登录！'
    except requests.exceptions.RequestException as e:
        notify.pushplus_bot(notify_title, "[Error]签到请求发送失败，请检查")
        raise print(e)


# 获取用户连续签到的天数
def get_user_continue_sign_day(user_cookie):
    headers = {
        "Cookie": user_cookie
    }
    try:
        continue_days_response = requests.get(continue_sign_day_url, headers=headers, verify=False)
        sign_html = BeautifulSoup(continue_days_response.text, 'html.parser')
        div_element = sign_html.find('div', class_='mission-always-settings')
        if div_element:
            continue_days = div_element.find_next('b').text.strip()
            return continue_days
        else:
            return
    except requests.exceptions.RequestException as e:
        notify.pushplus_bot(notify_title, "[Error]获取连续签到天数请求发送失败，请检查")
        raise print(e)


if __name__ == '__main__':
    cookie = get_user_cookie()
    sign_message = daily_sign(cookie)
    notify.pushplus_bot(notify_title, sign_message)
