'''
ctripday对应的sign获取以及body加密
'''
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
    # print(now)
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


def ctripMd5Str(timestamp, bodyLenth):
    """
    请求ctrip签名
    """
    # print(timestamp, bodyLenth)
    string = get_ctrip_vendor_id() + '3.0' + str(timestamp) + get_ctrip_secrect_key() + str(bodyLenth)
    string = string.lower()
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

# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/estimateprice/3.0/{timeStamp}/{signStr}'
# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/createorder/3.0/{timeStamp}/{signStr}'
# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/cancelorder/3.0/{timeStamp}/{signStr}'
# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/updateorder/3.0/{timeStamp}/{signStr}'
def ctrip_day_request(data,urlstr):
    try:
        dec = CDes(get_ctrip_secrect_key())
        enData = dec.encrypt(data)
        timeStamp = get_shanghai_time()
        url_info = get_ctrip_url_info()
        signStr = ctripMd5Str(timeStamp, len(enData))
        url = urlstr.format(timeStamp, signStr)
        # url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/createorder/3.0/{}/{}'
        response = requests.post(url, data=enData)
        dataJson = response.json()
    except:
        import traceback
        dataJson = str(traceback.print_exc())
        print(dataJson)
    return dataJson


    # print(response.status_code)
    # print(response.json())
if __name__ == '__main__':
    data={"ctripOrderId":"20230612164804","vehicleTypeId":121,"duration":5,"packageCode":"6-100","orderPrice":3101,"priceMark":"a8c0d389657841a98496a2612b08f4d6-v21","auditQuantity":3,"bagQuantity":4,"passenger":{"contactName":"julytest","contactPhone":"18123425634","email":"july@ttesst.dev","contactWeChat":"weixin123432"},"routeList":[{"useTime":"2025-04-30 11:30:00","departureLocation":{"name":"虹桥国际机场","latitude":31.166056,"longitude":121.319785,"cityId":2,"cityName":"上海","detailAddress":"虹桥国际机场"},"arriveLocationList":[{"name":"上海博物馆","latitude":31.128291,"longitude":121.43558,"cityId":2,"cityName":"上海","detailAddress":"黄浦区 人民大道201号"}]},{"useTime":"2025-05-01 04:10:00","departureLocation":{"name":"上海和平飯店","latitude":31.2390388,"longitude":121.4869678,"cityId":2,"cityName":"上海","detailAddress":"中國上海市黄浦区外滩南京东路20号 邮政编码: 200002"},"arriveLocationList":[{"name":"豫園","latitude":31.2253491,"longitude":121.4774603,"cityId":2,"cityName":"上海","detailAddress":"中國上海市黃浦區豫园"}]},{"useTime":"2024-05-02 15:10:00","departureLocation":{"name":"上海和平飯店","latitude":31.2390388,"longitude":121.4869678,"cityId":2,"cityName":"上海","detailAddress":"中國上海市黄浦区外滩南京东路20号 邮政编码: 200002"},"arriveLocationList":[{"name":"上海中山公園","latitude":31.2257219,"longitude":121.4239659,"cityId":2,"cityName":"上海","detailAddress":"中國上海市长宁区长宁路780号 邮政编码: 200050"}]},{"useTime":"2025-05-04 14:10:00","departureLocation":{"name":"上海和平飯店","latitude":31.2390388,"longitude":121.4869678,"cityId":2,"cityName":"上海","detailAddress":"中國上海市黄浦区外滩南京东路20号 邮政编码: 200002"},"arriveLocationList":[{"name":"上海站","latitude":31.24967045,"longitude":121.45561058,"cityId":2,"cityName":"上海","detailAddress":"静安区 秣陵路303号"}]}],"addServiceList":[],"extJson":"{\"remark\":\"推荐游玩行程 \\u003cbr/\\u003e北京周边包车两日游 (方案1)\\u003cbr/\\u003e1: 北京出发 司机按照预约时间到达约定地点，接您出发\\u003cbr/\\u003e2: 前往古北水镇 行驶约150公里2.5小时，到达古北水镇\\u003cbr/\\u003e3: 入住古北水镇 游览古北水镇，欣赏水镇夜景，入住酒店以便第二天行程\\u003cbr/\\u003e玩法二 (方案2)\\u003cbr/\\u003e1: 宽窄箱子 行驶约14公里2小时，建议游玩3小时\\u003cbr/\\u003e推荐美食 \\u003cbr/\\u003e (方案1)\\u003cbr/\\u003e1: 一品火锅 最好的火锅，没有之一\\u003cbr/\\u003e\"}"}
    urlstr = 'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/createorder/3.0/{}/{}'
    print(ctrip_day_request(data,urlstr))