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



aa = apidingding().dingTalk("测试：")