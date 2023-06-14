1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
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


# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/estimateprice/3.0/{timeStamp}/{signStr}'

# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/createorder/3.0/{timeStamp}/{signStr}'

# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/cancelorder/3.0/{timeStamp}/{signStr}'

# url = f'https://60pfokvaff.execute-api.us-east-2.amazonaws.com/dev/day/updateorder/3.0/{timeStamp}/{signStr}'
if __name__ == '__main__':
    data = {"ctripPurchaseOrderId": 4298304485603463, "categoryCode": "airport-dropoff", "totalPrice": 27.16, "priceMark": "ff4eece9366a4fb58ec6170bcc913a08", "fixedLocation": {"fixedCode": "SHA", "cityId": "2", "cityName": "上海"}, "vehicleType": 119, "useTime": "2023-06-15 10:06", "duseLocation": {"address": "上海市市场监督管理局", "detailAddress": "徐汇区 大木桥路1号工商大厦", "longitude": 121.461368, "latitude": 31.202388, "geoType": "GCJ02", "cityId": 2, "cityName": "上海"}, "auseLocation": {"address": "虹桥国际机场", "detailAddress": "虹桥国际机场", "longitude": 121.339785, "latitude": 31.196056, "geoType": "GCJ02", "cityId": 2, "cityName": "上海"}, "flightInfo": {}, "passenger": {"name": "送机julytest", "localPhoneAreaCode": "+86", "localPhone": "13932375023", "maskRealPhone": "153***36263", "email": "abctest@123.com", "intlPhoneAreaCode":66,"intlPhone": "19123423222"}, "masterOrderId": 4298304485603459,  "adults": 0, "children": 0, "luggage": 0, "fromType": 1}
    urlstr = 'https://93praqg7h9.execute-api.ap-east-1.amazonaws.com/dev/JNT/ordercreate/2.0/{}/{}'
    print(ctrip_request(data,urlstr))

