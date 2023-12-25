# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 
# @Version: 1.0
# @Comment: 
# -------------------------------
# cron "10 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('什么值得买')
import hashlib
import time

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书验证警告
urllib3.disable_warnings(InsecureRequestWarning)

CHECKIN_URL = "https://user-api.smzdm.com/checkin"


def smzdm_checkin():
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "cookie": "z_me=;partner_name=wandoujia;sess=BB-gj9qDX582iA1PiXhwVv3%2FgGCy24BuouqEQDRAeKj%2FGBMtmp"
                  "%2BfKuJHN0gwDiJ4cLgNOc3CkwKJzgHA%2FUNsDWpB4hupNs%3D;pid=O%2F2di%2BfCagp%2ByBOkjsm0Y5hOCZhBvzf4H6Vv"
                  "%2BVIbt%2FtzbfQDpoHn1A%3D%3D;device_type=Xiaomi2203121C;z_dr=d83f0a81240818b0cbae5cb8cfbc3213"
                  ";sessionID=d0771c8a19a6c3dc641fb8ce4ea06f27.1703386412512;basic_v=0;login=1;client_id"
                  "=d0771c8a19a6c3dc641fb8ce4ea06f27.1703386412340;register_time=1689744461;network=1"
                  ";device_system_version=9;partner_id=0;device_s=d83f0a81240818b0cbae5cb8cfbc3213;smzdm_version=10.6"
                  ".10;ab_test=f;device_smzdm=android;apk_partner_name=wandoujia;smzdm_id=6597502422;device_id"
                  "=d83f0a81240818b0cbae5cb8cfbc3213;device_push=1;apk_partner_id=0;session_id"
                  "=d0771c8a19a6c3dc641fb8ce4ea06f27.1703386412512;device_smzdm_version=10.6.10;device_rid"
                  "=d0771c8a19a6c3dc641fb8ce4ea06f27;active_time=1703386414;z_ai=;new_device_id"
                  "=d83f0a81240818b0cbae5cb8cfbc3213;is_new_user=1;last_article_info=;device_recfeed_setting=%7B"
                  "%22haojia_recfeed_switch%22%3A%221%22%2C%22homepage_sort_switch%22%3A%221%22%2C"
                  "%22other_recfeed_switch%22%3A%221%22%2C%22shequ_recfeed_switch%22%3A%221%22%7D"
                  ";device_smzdm_version_code=930;"
    }

    data_time = int(round(time.time() * 1000))
    data_sign = hashlib.md5(bytes(f'f=android&time={data_time}&v=10.4.1&weixin=1&key=apr1$AwP!wRRT$gJ/q.X24poeBInlUJC',
                                  encoding='utf-8')).hexdigest().upper()
    data = {
        "f": "android",
        "v": "10.4.1",
        "weixin": 1,
        "time": data_time,
        "sign": data_sign
    }

    checkin_response = requests.post(CHECKIN_URL, headers=header, data=data, verify=False).json()
    print(checkin_response)
    print(checkin_response['error_msg'])
    # 连续签到天数
    daily_num = checkin_response['data']['daily_num']
    # 补签卡
    cards = checkin_response['data']['cards']
    # 碎银子
    pre_re_silver = checkin_response['data']['pre_re_silver']
    # 金币
    cgold = checkin_response['data']['cgold']
    notify_content = "签到状态:[True]"


if __name__ == '__main__':
    smzdm_checkin()
