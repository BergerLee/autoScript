# Readme

**Author: Berger**

## 青龙面板拉库：

`ql repo https://github.com/Berger10086/autoScript.git "" "backup" "" ""`

## Environment  Instruction

- 查看文件说明的注释
- 如果是配置token：
  - **仅支持单个token：** 直接填写
  - **支持多个token：**`token` 与 `token` 之间用 `&` 隔开
- 如果是配置账号密码：
  - 支持配置**单个账号密码**：则账号密码之间用 `#` 隔开，例如 `test#123456`
  - 支持配置**多个账号密码**：则多个账号之间用 `&` 隔开，例如 `test1#123456&test2#123456`

## 文件说明

| Title                  | Description                    |    Variable Name    |          Variable Value           | Variable Type | Comment |
| :--------------------- | :----------------------------- | :-----------------: | :-------------------------------: | :-----------: | :-----: |
| RingSign.py            | 重庆光环公园微信小程序每日签到 |          /          |              Cookie               |    signal     |    /    |
| everyApiSign.py        | EveryApi每日签到               |          /          |      `mobile` and `password`      |    signal     |    /    |
| cloud_template_sign.py | 模板云每日签到                 | cloud_template_data | `login_name` and `login_password` |    signal     |    /    |
| 17u_sign.py            | 同程旅行每日签到领里程         |     user_token      |                 /                 |    signal     |    /    |
| cha_gee.py             | 霸王茶姬每日签到               |    qm_user_token    |                 /                 |    signal     |    /    |
| ikuuu_vpn              | ikuuu机场签到领流量            |        ikuuu        |       `email` and `passwd`        |   multiple    |    /    |
| uotan.py               | 柚子社区每日签到               |        uotan        |      `login` and `password`       |    signal     |    /    |
| notify.py              | 消息推送                       |          /          |                 /                 |       /       |    /    |



