# import binascii
# import json
# import hashlib
# import requests
# from pyDes import des, PAD_PKCS5
# from pyDes import ECB
#
# def des_encrypt(s, key='12345678'):
#     """
#     DES 加密
#     :param s: 原始字符串
#     :param key: 加密密钥8位
#     :return: 加密后字符串，16进制
#     """
#     secret_key = key
#     k = des(secret_key, ECB, None, pad=None, padmode=PAD_PKCS5)
#     en = k.encrypt(s, padmode=PAD_PKCS5)
#     return binascii.b2a_hex(en)
#
# # 参考:https://pages.c-ctrip.com/commerce/Car_Open_API_Platform/cn/accessApi/CreateOrder.html
# # 地址格式:  {Domain}/{Channel}/ordercreate/2.0/{timeStamp}/{sign}
# # vendor_id = '1000009' (这个是我临时填的,后面可能会修改)
# # version = '2.0'
# # channel = 'JNT'
# # time_stamp = ''  这个是时间戳,格式 yyyyMMddHHmmss
# # secrect_key = '12345678'
# # bodyJson请求参数:是dict类型
# def get_sign(vendor_id,version,channel,time_stamp,secrect_key,bodyJson):
#     encry_s = des_encrypt(json.dumps(bodyJson,ensure_ascii=False,separators=(',', ':')).encode("utf-8"))
#     verify = hashlib.md5((f'{vendor_id}{version}{channel.upper()}{time_stamp}{secrect_key}{len(encry_s)}').encode('utf-8')).hexdigest()
#     return encry_s, verify
#
# def ctrip_request(body,urlstr):
#     vendor_id = '1000777'
#     version = '2.0'
#     channel = 'JNT'
#     time_stamp = '23842834'
#     secrect_key = '12345678'
#     encry_s, sign = get_sign(vendor_id,version,channel,time_stamp,secrect_key,bodyJson=body)
#     url = urlstr.format(channel, version, time_stamp, sign)
#     ret = requests.post(url=url, data=encry_s.upper())
#     print(ret.json())
#     return ret.json()
#
import json
import hashlib
import binascii

try:
    from pyDes import des, PAD_PKCS5, ECB
except ImportError:
    pass

from datetime import datetime
import pytz
import requests

def get_ctrip_secrect_key():
    return '12345678'

def get_ctrip_vendor_id():
    return '1000777'

def get_ctrip_url_info():
    return {
        'url': 'http://gateway.fat.ctripqa.com/chvendormessagebus',
        'VendorID': '1000777'
    }


def get_shanghai_time(time_format='%Y%m%d%H%M%S'):
    now = datetime.utcnow()
    print(now)
    now = now.replace(tzinfo=pytz.utc)
    s = now.astimezone(pytz.timezone('Asia/Shanghai')).strftime(time_format)
    return s

class CDes:
    """
    ctrip消息体加密
    DES加密规格:ECB;
               PKCS5Padding;
    字节编码方式:16进制大写
    """
    def __init__(self, key) -> None:
        self.key = key
        self.cipher = des(key.encode(), mode=ECB, padmode=PAD_PKCS5)

    def encrypt(self, data):
        jsonString = json.dumps(data, ensure_ascii=False, separators=(',',':'))
        encryptedData = self.cipher.encrypt(jsonString.encode('utf-8'))
        return binascii.hexlify(encryptedData).decode('utf-8').upper()

    def decrypt(self, string):
        decryptData = self.cipher.decrypt(binascii.a2b_hex(string), padmode=PAD_PKCS5)
        return decryptData.decode()


def day_ctripMd5Str(timestamp, bodyLenth):
    """
    请求ctrip签名
    """
    print(timestamp, bodyLenth)
    string = get_ctrip_vendor_id() + '3.0' + str(timestamp) + get_ctrip_secrect_key() + str(bodyLenth)
    string = string.lower()
    res = hashlib.md5(string.encode('utf-8')).hexdigest()
    return res

# '/JNT/ordercreate/2.0/20230614142110/a1b87c83f78fea02f6f0a90ac5f08063'

def ctripMd5Str(timestamp, bodyLenth):
    """
    请求ctrip签名
    """
    print(timestamp, bodyLenth)
    string = get_ctrip_vendor_id() + '2.0' + 'JNT' + str(timestamp) + get_ctrip_secrect_key() + str(bodyLenth)
    res = hashlib.md5(string.encode('utf-8')).hexdigest()
    return res

def ctripMd5(version, channel, timestamp, bodyLenth, signStr):
    """
    ctrip 签名验证
    """
    string = get_ctrip_vendor_id() + str(version) + str(channel) + str(timestamp) + get_ctrip_secrect_key() + str(bodyLenth)
    res = hashlib.md5(string.encode('utf-8')).hexdigest()
    print("需签名串：%s, 签名后：%s, 签名串：%s" % (string, res, signStr))
    return res == signStr

# data = {
#     "ctripPurchaseOrderId": '202306141613',
#     "categoryCode": "airport-dropoff",
#     "totalPrice": 27.16,
#     "priceMark": "13ac68e107bb4f07a86d7c10431ad0c3",
#     "fixedLocation": {
#         "fixedCode": "SHA",
#         "cityId": "2",
#         "cityName": "上海"
#     },
#     "vehicleType": 119,
#     "useTime": "2023-07-15 10:06",
#     "duseLocation": {
#         "address": "上海市市场监督管理局",
#         "detailAddress": "徐汇区 大木桥路1号工商大厦",
#         "longitude": 121.461368,
#         "latitude": 31.202388,
#         "geoType": "GCJ02",
#         "cityId": 2,
#         "cityName": "上海"
#     },
#     "auseLocation": {
#         "address": "虹桥国际机场",
#         "detailAddress": "虹桥国际机场",
#         "longitude": 121.339785,
#         "latitude": 31.196056,
#         "geoType": "GCJ02",
#         "cityId": 2,
#         "cityName": "上海"
#     },
#     "flightInfo": {},
#     "passenger": {
#         "name": "送机julytest",
#         "localPhoneAreaCode": "+86",
#         "localPhone": "13964440327",
#         "maskRealPhone": "153***36263",
#         "email": "abctest@123.com",
#         "intlPhone": "19123423222"
#     },
#     "masterOrderId": '2023061416131',
#     "needLandingVisa": False,
#     "permission": {
#         "record": True,
#         "video": False
#     },
#     "supportExternalDriver": True,
#     "adults": 1,
#     "children": 0,
#     "luggage": 1,
#     "fromType": 1
# }

def ctrip_request(data,urlstr):
    try:
        dec = CDes(get_ctrip_secrect_key())
        enData = dec.encrypt(data)
        timeStamp = get_shanghai_time()
        url_info = get_ctrip_url_info()
        signStr = ctripMd5Str(timeStamp, len(enData))
        url = urlstr.format(timeStamp, signStr)
        print(signStr)
        print(enData)
        print(timeStamp)
        response = requests.post(url, data=enData)
        print(response.status_code)
        print(response.json())
        dataJson = response.json()
    except:
        import traceback
        dataJson = str(traceback.print_exc())
        print(dataJson)
    return dataJson


# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/estimateprice/3.0/{timeStamp}/{signStr}'

# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/createorder/3.0/{timeStamp}/{signStr}'

# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/cancelorder/3.0/{timeStamp}/{signStr}'

# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/updateorder/3.0/{timeStamp}/{signStr}'
if __name__ == '__main__':
    data = {"ctripPurchaseOrderId": 4298304485603463, "categoryCode": "airport-dropoff", "totalPrice": 27.16, "priceMark": "ff4eece9366a4fb58ec6170bcc913a08", "fixedLocation": {"fixedCode": "SHA", "cityId": "2", "cityName": "上海"}, "vehicleType": 119, "useTime": "2023-06-15 10:06", "duseLocation": {"address": "上海市市场监督管理局", "detailAddress": "徐汇区 大木桥路1号工商大厦", "longitude": 121.461368, "latitude": 31.202388, "geoType": "GCJ02", "cityId": 2, "cityName": "上海"}, "auseLocation": {"address": "虹桥国际机场", "detailAddress": "虹桥国际机场", "longitude": 121.339785, "latitude": 31.196056, "geoType": "GCJ02", "cityId": 2, "cityName": "上海"}, "flightInfo": {}, "passenger": {"name": "送机julytest", "localPhoneAreaCode": "+86", "localPhone": "13932375023", "maskRealPhone": "153***36263", "email": "abctest@123.com", "intlPhoneAreaCode":66,"intlPhone": "19123423222"}, "masterOrderId": 4298304485603459,  "adults": 0, "children": 0, "luggage": 0, "fromType": 1}
    urlstr = 'https://93praqg7h9.execute-api.ap-east-1.amazonaws.com/dev/JNT/ordercreate/2.0/{}/{}'
    print(ctrip_request(data,urlstr))

