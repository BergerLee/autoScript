# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2024-9-17
# @Version: 1.1
# @Comment:
# -------------------------------
# cron "10 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('PortableAppK自动签到')

import os
import time
import requests
import base64

import notify

portable_cookie = os.getenv('portable_cookie')

notify_title = 'PortableAppK自动签到提醒'
phpsessid = 'PHPSESSID=8c5e262776999dcd217d43c842288ba2'


# 将图片转为base64编码
def get_image_base64(user_cookie=phpsessid):
    capcha_url = "https://portableappk.com/wp-content/plugins/wordpress-hack-bundle/addons/gen-captcha-img.php?Math.random()"

    request_header = {
        "cookie": user_cookie
    }

    try:
        print('正在请求图片验证码....')
        # 请求验证码，返回回来的是图片
        capcha_response = requests.get(capcha_url, headers=request_header, stream=True)
        # 检查请求是否成功
        capcha_response.raise_for_status()
        print('图片验证码请求成功！')

        with open('captcha_image.png', 'wb') as f:
            f.write(capcha_response.content)
        print('图片验证码已保存为 captcha_image.png')

        # 转换为 Base64
        base64_data = base64.b64encode(capcha_response.content).decode('utf-8')
        print('图片验证码格式转换成功！')
        return base64_data
    except requests.RequestException as e:
        print(e)
        # return notify_message(f'[Error] Error fetching image: {e}')
    except IOError as e:
        print(e)
        # return notify_message(f'[Error] Error processing image: {e}')


# 识别验证码
def identify_pic_code(img_base64):
    identify_url = "http://captcha.zwhyzzz.top:8092/identify_GeneralCAPTCHA"
    img_json = {
        "ImageBase64": img_base64
    }
    try:
        response = requests.post(identify_url, json=img_json, verify=False)
        response.raise_for_status()  # 检查请求是否成功
        return response.json().get('result', '[Error] No result in response')
    except requests.RequestException as e:
        return notify_message(f'[Error] Error making the request: {e}')


# 执行签到
def check_in(user_cookie):
    print('-----------正在执行签到操作------------')
    check_in_url = "https://portableappk.com/wp-content/plugins/wordpress-hack-bundle/addons/verify-checkin.php"

    max_attempts = 7
    attempt = 0

    while attempt < max_attempts:
        # 获取验证码的base64编码
        img_base64 = get_image_base64(user_cookie)
        if img_base64.startswith('[Error]'):
            print(img_base64)
            return

        # 识别验证码
        pic_code = identify_pic_code(img_base64)
        if pic_code.startswith('[Error]'):
            return notify_message(pic_code)

        if len(pic_code) != 5:
            print('验证码识别错误，等待重新执行...')
            attempt += 1
            # 验证码识别接口有3秒钟的检测
            time.sleep(5)
            continue

        # 构造签到请求体
        request_data = {
            "phrase": pic_code
        }

        request_header = {
            "cookie": user_cookie
        }

        try:
            response = requests.post(check_in_url, headers=request_header, data=request_data)
            response.raise_for_status()  # 检查请求是否成功
            response_data = response.json()
            print(response_data)

            if response_data.get('success') == 0:
                print(f'Attempt {attempt + 1} failed. Retrying...')
                attempt += 1
                time.sleep(5)
            else:
                return notify_message(f'[Success]签到成功，已连续签到{response_data.get("days")}天！')
        except requests.RequestException as e:
            return notify_message(f'[Error] Error making the request: {e}')

    notify_message(f'[Error] Check-in failed after {max_attempts} attempts.')


def user_login(username, password):
    print('--------------正在执行登陆操作--------------')
    login_url = 'https://portableappk.com/wp-login.php'

    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        # 获取验证码的base64编码
        img_base64 = get_image_base64()
        if img_base64.startswith('[Error]'):
            print(img_base64)
            return

        # 识别验证码
        pic_code = identify_pic_code(img_base64)
        if pic_code.startswith('[Error]'):
            return notify_message(pic_code)

        if len(pic_code) != 5:
            print('验证码识别错误，等待重新执行...')
            attempt += 1
            # 验证码识别接口有3秒钟的检测
            time.sleep(4)
            continue

        print(f'验证码为{pic_code}')
        # 构造登录请求体
        request_data = {
            "log": username,
            "pwd": password,
            "phrase": pic_code,
            "wp-submit": "登录",
            "testcookie": "1"
        }

        login_header = {
            "cookie": f'wordpress_test_cookie=WP%20Cookie%20check; {phpsessid}'
        }

        try:
            login_response = requests.post(login_url, headers=login_header, data=request_data, allow_redirects=False)
            login_response.raise_for_status()  # 检查请求是否成功
            set_cookie = login_response.headers.get('set-cookie')
            if set_cookie:
                try:
                    # 尝试提取 user_cookie
                    user_cookie = set_cookie.split(';')[2].split(',')[1]
                    print('--------------登陆成功--------------')
                    return user_cookie
                except IndexError:
                    print(f'Attempt {attempt + 1} failed. Retrying...')
                    attempt += 1
        except requests.RequestException as e:
            print(e)
            return notify_message(f'[Error] Error making the request: {e}')
    notify_message(f'[Error] Check-in failed after {max_attempts} attempts.')


def notify_message(message):
    print(message)
    notify.pushplus_bot(notify_title, message)


if __name__ == '__main__':
    user_account = os.getenv('portable_account')
    username = user_account.split('|')[0]
    password = user_account.split('|')[1]
    if not username or not password:
        print('账号密码读取失败')
    user_cookie = user_login(username, password)
    print(user_cookie)
    if user_cookie:
        handle_cookie = user_cookie + ';' + phpsessid
        check_in(handle_cookie.strip())
