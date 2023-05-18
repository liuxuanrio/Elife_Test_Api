import requests, json
from requests.adapters import HTTPAdapter

# request请求参数化

def requests_type(type, head, url, data):
    # post请求
    if type == 'post':
        try:
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            print(json.dumps(dict(data), ensure_ascii=False))
            res = requests.post(url=url, headers=head, data=json.dumps(data))
            return res.json()
        except requests.exceptions.RequestException as e:
            print(e)
    # get请求
    else:
        # 重试机制，接口请求超时获取不到数据时，重新请求3次
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        try:
            ret = requests.request("GET", url, headers=head, timeout=100)
            ret.encoding = ret.apparent_encoding
            res = ret.json()
            return res
        except requests.exceptions.RequestException as e:
            print(e)

# 表单格式请求
def requests_Parameters(head, url, data):
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        print(json.dumps(dict(data), ensure_ascii=False))
        res = requests.request("post", headers=head, url=url, data=data)
        return res.json()
    except requests.exceptions.RequestException as e:
        print(e)