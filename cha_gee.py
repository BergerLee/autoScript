# -------------------------------
# @Author: BergerLee
# @GitHub: https://github.com/BergerLee
# @Time: 2023-12-22
# @Version: 1.0
# @Comment: 
# -------------------------------
# cron "1 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('霸王茶姬')
import urllib3
import os
import notify
import requests
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书验证警告
urllib3.disable_warnings(InsecureRequestWarning)

# 签到接口
SIGN_MINIAPP_URL = "https://webapi.qmai.cn/web/catering/integral/sign/signIn"
# 查询积分接口
TOTAL_POINT_MINIAPP_URL = "https://webapi.qmai.cn/web/catering/crm/total-points"


# 霸王茶姬微信小程序签到
def sign_miniapp(headers):
    body = {
        "activityId": "100820000000000686",
        "mobilePhone": "14723555129"
    }
    try:
        sign_response = requests.post(SIGN_MINIAPP_URL, headers=headers, json=body, verify=False).json()
        print(sign_response)
        response_code = sign_response.get('status', False)
        if response_code:
            return f'[True]签到成功！'
        else:
            return f'[False]{sign_response.get("message", "Unknown error")}'
    except requests.RequestException as e:
        return f'[Error]Error making the request: {e}'


# 霸王茶姬微信小程序查询当前用户积分
def get_user_point_miniapp(headers):
    try:
        point_response = requests.post(TOTAL_POINT_MINIAPP_URL, headers=headers, verify=False).json()
        print(point_response)
        response_status = point_response.get('status', False)
        if response_status:
            return f'当前积分：{point_response.get("data")}'
        else:
            return f'{point_response.get("message", "Unknown error")}'
    except requests.RequestException as e:
        return f'[Error]Error making the request: {e}'


if __name__ == '__main__':
    user_token = os.getenv('qm_user_token')

    request_headers = {
        "qm-user-token": user_token,
        "Content-Type": "application/json",
        "qm-from": "wechat"
    }

    miniapp_sign_result_message = sign_miniapp(request_headers)
    miniapp_point_result_message = get_user_point_miniapp(request_headers)
    notify_content = f"{miniapp_sign_result_message}\n{miniapp_point_result_message}"
    notify.pushplus_bot("霸王茶姬签到提醒", notify_content)
