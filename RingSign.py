import notify
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 光环公园微信小程序签到领积分
# 禁用SSL证书验证警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://ring.hklcn.com/wxmall/wxsite/mbr/signin.do"
headers = {
    "Cookie": ""
}

response = requests.get(url, headers=headers, verify=False).json()

print(response)

notifyTitle = "光环公园小程序签到提醒"
notifyContent = response.get('message')
# 消息推送
notify.pushplus_bot(notifyTitle, notifyContent)
