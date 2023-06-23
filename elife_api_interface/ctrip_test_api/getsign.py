
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
    return 'Xa0TTStx'

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
    # string = string.lower()
    res = hashlib.md5(string.encode('utf-8')).hexdigest()
    return res



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



if __name__ == '__main__':
    data = {"ctripPurchaseOrderId": 4298304485603463, "categoryCode": "airport-dropoff", "totalPrice": 27.16, "priceMark": "ff4eece9366a4fb58ec6170bcc913a08", "fixedLocation": {"fixedCode": "SHA", "cityId": "2", "cityName": "上海"}, "vehicleType": 119, "useTime": "2023-06-15 10:06", "duseLocation": {"address": "上海市市场监督管理局", "detailAddress": "徐汇区 大木桥路1号工商大厦", "longitude": 121.461368, "latitude": 31.202388, "geoType": "GCJ02", "cityId": 2, "cityName": "上海"}, "auseLocation": {"address": "虹桥国际机场", "detailAddress": "虹桥国际机场", "longitude": 121.339785, "latitude": 31.196056, "geoType": "GCJ02", "cityId": 2, "cityName": "上海"}, "flightInfo": {}, "passenger": {"name": "送机julytest", "localPhoneAreaCode": "+86", "localPhone": "13932375023", "maskRealPhone": "153***36263", "email": "abctest@123.com", "intlPhoneAreaCode":66,"intlPhone": "19123423222"}, "masterOrderId": 4298304485603459,  "adults": 0, "children": 0, "luggage": 0, "fromType": 1}
    urlstr = 'https://93praqg7h9.execute-api.ap-east-1.amazonaws.com/dev/JNT/ordercreate/2.0/{}/{}'
    print(ctrip_request(data,urlstr))

