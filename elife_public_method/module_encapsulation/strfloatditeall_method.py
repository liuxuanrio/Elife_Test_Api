import re
from statistics import mean
import math
import json
from urllib import parse


class BasicsOperation:
    # 保留小数点后两位，四舍五入
    def floatround(self, data):
        floatdata = float("%.2f" % float(data))
        return floatdata

    #　保留小数点后两位补零去除字符
    def floatroundstr(self, data):
        data1 = str(("{:.2f}".format(float(data))))
        data2 = data1.replace(".", "")
        return data2

    # 求列表中数字或小数的平均值，保留小数点后两位
    def meanlistavg(self, data):
        meandata = round(mean(data), 2)
        return meandata

    # 取绝对值
    def mathfabs(self, data):
        mathdata=math.fabs(data)
        return mathdata

    # 循环取出元组数据写入列表
    def tupleswitchlist(self, data):
        datalist = []
        for configlistcount in range(len(data)):
            for configlistcounts in range(len(data[configlistcount])):
                datalist.append(data[configlistcount][configlistcounts])
        return datalist

    # 提取字符串中的数字
    def regularstrint(self, data):
        dataint = re.sub("\D", "", data)
        print(type(dataint))
        return dataint

    # 判断字符串或列表数据是否为空
    def strlistnull(self, data):
        datainfo = ''
        if len(data) == 0:
            datainfo = "无"
        return datainfo

    # 字符串转字典
    def strdictinfo(self, data):
        data1 = json.loads(data)
        return data1

    # list列表去重
    def setlist(self, list):
        data = set(list)
        return data

    # url 加密
    def urllib_encryption(self, data):
        urldata = parse.quote(data)
        return urldata

    # 对比两个list返回差值
    def setListDiff(self, list1, list2):
        list3 = list(set(list1) ^ set(list2))
        return list3

if __name__ == "__main__":
    flo = 0.5