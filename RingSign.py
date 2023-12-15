# -------------------------------
# @Author : github@BergerLee https://github.com/BergerLee
# @Update by BergerLee
# @Time : 2023/12/14
# -------------------------------
# cron "10 0 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('指尖光环小程序每日签到')
import urllib3

import notify
import requests
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书验证警告
urllib3.disable_warnings(InsecureRequestWarning)

url = "https://ring.hklcn.com/wxmall/wxsite/mbr/signin.do"
headers = {
    "Cookie": "JSESSIONID=D726130F69A97817A86F9792CB169647"
}

response = requests.get(url, headers=headers, verify=False).json()

print(response)

notifyTitle = "光环公园小程序签到提醒"
notifyContent = response.get('message')
# 消息推送
notify.pushplus_bot(notifyTitle, notifyContent)
