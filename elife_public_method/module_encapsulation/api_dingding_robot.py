import requests, json

class apidingding:
    def dingTalk(self, news):
        headers = {
            "Content-Type": "application/json"
        }
        data = {"msgtype": "text",
                "text": {
                    "content": str(news)},
                "at": {"isAtAll": 'true'}
                }
        url='https://oapi.dingtalk.com/robot/send?access_token='

        res = requests.post(url=url, headers=headers, data=json.dumps(data))
        return res.json()

    def dingTalkSes(self, webhook, secret, text):
        import json
        import time
        import hmac
        import hashlib
        import base64
        import urllib.parse
        import requests
        # 钉钉推送
        headers = {'Content-Type': 'application/json', "Charset": "UTF-8"}
        # 这里替换为复制的完整 webhook 地址
        prefix = f'https://oapi.dingtalk.com/robot/send?access_token={webhook}'
        # 时间戳
        timestamp = str(round(time.time() * 1000))
        # 编码转换
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        # 使用HmacSHA256算法计算签名，然后进行Base64 encode
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        # 将一些特殊的字符串转换为固定的一些符号字母数字组合，比如/转为%2
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # 拼接url
        url = f'{prefix}&timestamp={timestamp}&sign={sign}'
        # 钉钉消息格式，其中 content 就是我们要发送的具体内容
        con = {"msgtype": "text",
               "text": {
                   "content": text
                   }
               }
        jd = json.dumps(con)
        requests.request('POST', url, data=jd, headers=headers)