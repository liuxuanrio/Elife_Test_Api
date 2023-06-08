import binascii
import json
import hashlib
import requests
from pyDes import des, PAD_PKCS5
from pyDes import ECB

def des_encrypt(s, key='12345678'):
    """
    DES 加密
    :param s: 原始字符串
    :param key: 加密密钥8位
    :return: 加密后字符串，16进制
    """
    secret_key = key
    k = des(secret_key, ECB, None, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)

# 参考:https://pages.c-ctrip.com/commerce/Car_Open_API_Platform/cn/accessApi/CreateOrder.html
# 地址格式:  {Domain}/{Channel}/ordercreate/2.0/{timeStamp}/{sign}
# vendor_id = '1000009' (这个是我临时填的,后面可能会修改)
# version = '2.0'
# channel = 'JNT'
# time_stamp = ''  这个是时间戳,格式 yyyyMMddHHmmss
# secrect_key = '12345678'
# bodyJson请求参数:是dict类型
def get_sign(vendor_id,version,channel,time_stamp,secrect_key,bodyJson):
    encry_s = des_encrypt(json.dumps(bodyJson,ensure_ascii=False,separators=(',', ':')).encode("utf-8"))
    verify = hashlib.md5((f'{vendor_id}{version}{channel.upper()}{time_stamp}{secrect_key}{len(encry_s)}').encode('utf-8')).hexdigest()
    return encry_s, verify

def ctrip_request(body,urlstr):
    vendor_id = '1000777'
    version = '2.0'
    channel = 'JNT'
    time_stamp = '23842834'
    secrect_key = '12345678'
    encry_s, sign = get_sign(vendor_id,version,channel,time_stamp,secrect_key,bodyJson=body)
    url = urlstr.format(channel, version, time_stamp, sign)
    ret = requests.post(url=url, data=encry_s.upper())
    print(ret.json())
    return ret.json()


if __name__ == '__main__':

    body={'categoryCode': 'airport-dropoff', 'duseLocation': {'address': 'Shanghai Pudong International Airport 4RV5+P8J, Ying Bin Gao Su Gong Lu, Pu Dong Xin Qu, Shang Hai Shi, China', 'detailAddress': 'Shanghai Pudong International Airport 4RV5+P8J, Ying Bin Gao Su Gong Lu, Pu Dong Xin Qu, Shang Hai Shi, China', 'latitude': 31.1433969, 'longitude': 121.6578713, 'geoType': 'GCJ02', 'cityId': '2', 'cityName': '上海'}, 'auseLocation': {'address': 'Shanghai Pudong International Airport 4RV5+P8J, Ying Bin Gao Su Gong Lu, Pu Dong Xin Qu, Shang Hai Shi, China', 'detailAddress': 'Shanghai Pudong International Airport 4RV5+P8J, Ying Bin Gao Su Gong Lu, Pu Dong Xin Qu, Shang Hai Shi, China', 'latitude': 31.192209, 'longitude': 121.334297, 'geoType': 'GCJ02', 'cityId': '2', 'cityName': '上海'}, 'useTime': '2024-10-29 18:26', 'fromType': 1, 'language': 'zh-CN'}
    urlstr = "https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/{}/productquery/{}/{}/{}"
    # encry_s, sign = get_sign(vendor_id,version,channel,time_stamp,secrect_key,bodyJson=body)
    print(ctrip_request(body,urlstr))
    #
    # # "https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/{}/ordercreate/{}/{}/{}"
    # url = urlstr.format(channel, version, time_stamp, sign)
    # # ret1 = requests.post(url=url,  data=json.dumps(encry_s.upper()))
    # ret = requests.post(url=url, data=encry_s.upper())
    # # print(url)
    # ret2=ret.json()
    # ret3 = json.dumps(ret2, ensure_ascii=False)
    #
    # # ret4 = ret.replace("'", "", -1)
    # print(json.loads(ret3))




