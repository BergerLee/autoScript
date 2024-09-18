# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2024-9-17
# @Version: 1.0
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
request_header = {
    "cookie": portable_cookie
}

notify_title = 'PortableAppK自动签到提醒'


# 将图片转为base64编码
def get_image_base64():
    capcha_url = "https://portableappk.com/wp-content/plugins/wordpress-hack-bundle/addons/gen-captcha-img.php?Math.random()"
    try:
        print('正在请求图片验证码....')
        # 请求验证码，返回回来的是图片
        capcha_response = requests.get(capcha_url, headers=request_header, stream=True)
        # 检查请求是否成功
        capcha_response.raise_for_status()
        print('图片验证码请求成功！')
        # 转换为 Base64
        base64_data = base64.b64encode(capcha_response.content).decode('utf-8')
        print('图片验证码格式转换成功！')
        return base64_data
    except requests.RequestException as e:
        return notify_message(f'[Error] Error fetching image: {e}')
    except IOError as e:
        return notify_message(f'[Error] Error processing image: {e}')


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
def check_in():
    check_in_url = "https://portableappk.com/wp-content/plugins/wordpress-hack-bundle/addons/verify-checkin.php"

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

        # 构造签到请求体
        request_data = {
            "phrase": pic_code
        }

        try:
            print('正在执行签到操作....')
            response = requests.post(check_in_url, headers=request_header, data=request_data)
            response.raise_for_status()  # 检查请求是否成功
            response_data = response.json()

            if response_data.get('success') == 0:
                print(f'Attempt {attempt + 1} failed. Retrying...')
                attempt += 1
            else:
                return notify_message(f'[Success]签到成功，已连续签到{response_data.get("days")}天！')
        except requests.RequestException as e:
            return notify_message(f'[Error] Error making the request: {e}')

    notify_message(f'[Error] Check-in failed after {max_attempts} attempts.')


def notify_message(message):
    print(message)
    notify.pushplus_bot(notify_title, message)


if __name__ == '__main__':
    check_in()
