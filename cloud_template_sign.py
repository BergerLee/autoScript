import notify
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import os

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 只需要 wordpress_logged_in
cloud_template_cookie = os.getenv('cloud_template_cookie')
sign_url = "https://www.22vd.com/wp-admin/admin-ajax.php"
continue_sign_day_url = "https://www.22vd.com/sign"

headers = {
    "Cookie": cloud_template_cookie
}

fromData = {
    "action": "sign_ajax",
    "ajax_date": "sign"
}

sign_response = requests.post(sign_url, headers=headers, data=fromData).json()
sign_message = ""
continue_days = 0

if sign_response == 1 or sign_response == 3:
    continue_days_response = requests.get(continue_sign_day_url, headers=headers)
    if continue_days_response.status_code == 200:
        sign_html = BeautifulSoup(continue_days_response.text, 'html.parser')
        div_element = sign_html.find('div', class_='title', text='连续签到：')
        if div_element:
            continue_days = div_element.find_next('b').text.strip()
        else:
            print('未找到连续签到信息')
    sign_message = "[True]模板云今日签到成功！以连续签到{}天".format(continue_days == 0 if continue_days else "null")
elif sign_response == 2:
    sign_message = "[Exist]模板云今日已签到，无需重复签到！"
elif sign_response == 5:
    sign_message = "[False]模板云签到失败，原因是登录过期！"
elif sign_response == 4:
    sign_message = "[True]模板云今日已签到，连续签到已被重置!"

print(sign_message)
notifyTitle = "云模板签到提醒"
# 消息推送
notify.pushplus_bot(notifyTitle, sign_message)
