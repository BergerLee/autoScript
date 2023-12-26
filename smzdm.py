# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 
# @Version: 1.0
# @Comment: 
# -------------------------------
# cron "0 1 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('什么值得买')

import hashlib
import json
import os
import requests
import time
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书验证警告
urllib3.disable_warnings(InsecureRequestWarning)

# 青龙变量 zdm_cookie
zdm_cookie = os.getenv("zdm_cookie").split('&')

for i in range(len(zdm_cookie)):
    print(f'开始第{i + 1}个帐号签到')
    ts = int(round(time.time() * 1000))
    url = 'https://user-api.smzdm.com/robot/token'
    headers = {
        'Host': 'user-api.smzdm.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'{zdm_cookie[i]}',
        'User-Agent': 'smzdm_android_V10.4.1 rv:841 (22021211RC;Android12;zh)smzdmapp',
    }
    data = {
        "f": "android",
        "v": "10.4.1",
        "weixin": 1,
        "time": ts,
        "sign": hashlib.md5(bytes(f'f=android&time={ts}&v=10.4.1&weixin=1&key=apr1$AwP!wRRT$gJ/q.X24poeBInlUJC',
                                  encoding='utf-8')).hexdigest().upper()
    }
    html = requests.post(url=url, headers=headers, data=data)
    result = html.json()
    token = result['data']['token']

    Timestamp = int(round(time.time() * 1000))
    data = {
        "f": "android",
        "v": "10.4.1",
        "sk": "ierkM0OZZbsuBKLoAgQ6OJneLMXBQXmzX+LXkNTuKch8Ui2jGlahuFyWIzBiDq/L",
        "weixin": 1,
        "time": Timestamp,
        "token": token,
        "sign": hashlib.md5(bytes(
            f'f=android&sk=ierkM0OZZbsuBKLoAgQ6OJneLMXBQXmzX+LXkNTuKch8Ui2jGlahuFyWIzBiDq/L&time={Timestamp}&token={token}&v=10.4.1&weixin=1&key=apr1$AwP!wRRT$gJ/q.X24poeBInlUJC',
            encoding='utf-8')).hexdigest().upper()
    }
    url = 'https://user-api.smzdm.com/checkin'
    url2 = 'https://user-api.smzdm.com/checkin/all_reward'
    headers = {
        'Host': 'user-api.smzdm.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'{zdm_cookie[i]}',
        'User-Agent': 'smzdm_android_V10.4.1 rv:841 (22021211RC;Android12;zh)smzdmapp',
    }
    html = requests.post(url=url, headers=headers, data=data)
    html2 = requests.post(url=url2, headers=headers, data=data)
    result = json.loads(html.text)
    result2 = json.loads(html2.text)
    print(result)
    print('------------------------------------------------------------------------------------------------')
    print(result2)

# CHECKIN_URL = "https://user-api.smzdm.com/checkin"
# CHECKIN_REWARD_URL = "https://user-api.smzdm.com/checkin/all_reward"


# def smzdm_checkin():
#     header = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "cookie": "z_me=;partner_name=wandoujia;sess=BB-gj9qDX582iA1PiXhwVv3%2FgGCy24BuouqEQDRAeKj%2FGBMtmp"
#                   "%2BfKuJHN0gwDiJ4cLgNOc3CkwKJzgHA%2FUNsDWpB4hupNs%3D;pid=O%2F2di%2BfCagp%2ByBOkjsm0Y5hOCZhBvzf4H6Vv"
#                   "%2BVIbt%2FtzbfQDpoHn1A%3D%3D;device_type=Xiaomi2203121C;z_dr=d83f0a81240818b0cbae5cb8cfbc3213"
#                   ";sessionID=d0771c8a19a6c3dc641fb8ce4ea06f27.1703386412512;basic_v=0;login=1;client_id"
#                   "=d0771c8a19a6c3dc641fb8ce4ea06f27.1703386412340;register_time=1689744461;network=1"
#                   ";device_system_version=9;partner_id=0;device_s=d83f0a81240818b0cbae5cb8cfbc3213;smzdm_version=10.6"
#                   ".10;ab_test=f;device_smzdm=android;apk_partner_name=wandoujia;smzdm_id=6597502422;device_id"
#                   "=d83f0a81240818b0cbae5cb8cfbc3213;device_push=1;apk_partner_id=0;session_id"
#                   "=d0771c8a19a6c3dc641fb8ce4ea06f27.1703386412512;device_smzdm_version=10.6.10;device_rid"
#                   "=d0771c8a19a6c3dc641fb8ce4ea06f27;active_time=1703386414;z_ai=;new_device_id"
#                   "=d83f0a81240818b0cbae5cb8cfbc3213;is_new_user=1;last_article_info=;device_recfeed_setting=%7B"
#                   "%22haojia_recfeed_switch%22%3A%221%22%2C%22homepage_sort_switch%22%3A%221%22%2C"
#                   "%22other_recfeed_switch%22%3A%221%22%2C%22shequ_recfeed_switch%22%3A%221%22%7D"
#                   ";device_smzdm_version_code=930;"
#     }
#
#     data_time = int(round(time.time() * 1000))
#     data_sign = hashlib.md5(bytes(f'f=android&time={data_time}&v=10.4.1&weixin=1&key=apr1$AwP!wRRT$gJ/q.X24poeBInlUJC',
#                                   encoding='utf-8')).hexdigest().upper()
#     data = {
#         "f": "android",
#         "v": "10.4.1",
#         "weixin": 1,
#         "time": data_time,
#         "sign": data_sign
#     }
#
#     checkin_response = requests.post(CHECKIN_URL, headers=header, data=data, verify=False).json()
#     print(checkin_response)
#     # 补签卡
#     cards = checkin_response['data']['cards']
#     # 碎银子
#     pre_re_silver = checkin_response['data']['pre_re_silver']
#     # 金币
#     cgold = checkin_response['data']['cgold']
#
#     bag_data = "钱包数据：\n金币x{}\n碎银子x{}\n补签卡x{}".format(cgold, pre_re_silver, cards)
#     return bag_data
#
# def checkin_all_reward(cookie):
#
# if __name__ == '__main__':
#     smzdm_checkin()
