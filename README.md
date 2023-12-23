# Readme

**Author: Berger**

## 青龙面板拉库：

`ql repo https://github.com/Berger10086/autoScript.git "" "backup" "" ""`

## 环境变量配置说明

- 查看文件说明的注释
- 如果是配置token：
  - **仅支持单个token：**直接填写
  - **支持多个token：**`token` 与 `token` 之间用 `&` 隔开
- 如果是配置账号密码：
  - 支持配置**单个账号密码**：则账号密码之间用 `#` 隔开，例如 `test#123456`
  - 支持配置**多个账号密码**：则多个账号之间用 `&` 隔开，例如 `test1#123456&test2#123456`

## 文件说明

| Title                  | Description                    | Comment                                                      |
| ---------------------- | ------------------------------ | ------------------------------------------------------------ |
| RingSign.py            | 重庆光环公园微信小程序每日签到 | Cookie                                                       |
| everyApiSign.py        | EveryApi每日签到               | userName,password                                            |
| cloud_template_sign.py | 模板云每日签到                 | 环境变量名：`cloud_template_data`<br/>变量类型：单个账号密码 |
| 17u_sign.py            | 同程旅行每日签到领里程         | 环境变量名：`user_token`<br/>变量类型：单个Token             |
| cha_gee.py             | 霸王茶姬每日签到               | 环境变量名：`qm_user_token` <br>变量类型：单个Token          |
| ikuuu_vpn              | ikuuu机场签到领流量            | 环境变量名：`ikuuu`<br/>变量类型：多个账号密码               |
| notify.py              | 消息推送                       |                                                              |



