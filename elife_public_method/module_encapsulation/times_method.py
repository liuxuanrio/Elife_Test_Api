import datetime
import random

from elife_public_method.module_encapsulation.strfloatditeall_method import BasicsOperation


class TimeMethod:
    # 获取昨天年月日
    def timeyearmonthday(self, count):
        # count   0 当天  1 昨天  依次类推
        today = datetime.date.today()
        oneday = datetime.timedelta(days=count)
        yesterday = today - oneday
        return str(yesterday)

    # 获取年月日，去除字符保留数字
    def inttimeyearmonthday(self):
        dayname = datetime.datetime.now().strftime("%Y%m%d")
        return dayname

    # 获取年月日时分秒，去除字符保留数字
    def intnowtimedaydatetime(self):
        strnow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return strnow

    # 获取当前日期年月日时分秒
    def nowtimedaydatetime(self):
        strnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return strnow

    # 获取当前日期年月日时分
    def newTimeDate(self):
        strnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        return strnow

    # 获取当前日期年月日时分秒毫秒（3位）
    def utcnowtimedaydatetime(self):
        strnow = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return strnow

    #  年月日时分秒转换至年月日
    def dateformatdata(self, time):
        data = datetime.datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        return data

    # 数据库日期转字符串
    def dayStrftime(self, time):
        data = time.strftime('%Y-%m-%d %H:%M:%S')
        return data


    # 判断日期是否大于昨天
    def timestrordatatime(self, time):
        timeyearmonthdays = self.timeyearmonthday(1)
        strtime = f"{timeyearmonthdays} 23:59:59"
        t1 = datetime.datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        data = {}
        if t2 > t1:
            data["msg"]="success"
        else:
            data["msg"] = "False"
        return data

    # 打印当前日期加日志
    def logstimeinfo(self, info):
        times = self.nowtimedaydatetime()
        logsinfo = f"[{times}][INFO] {str(info)}"
        print(logsinfo)

    # 打印接口请求信息
    def requestslogs(self, type, url, data, run):
        urllog = f"[{type}]  {url}"
        self.logstimeinfo(urllog)
        if type == 'POST':
            self.logstimeinfo(data)
        else:
            pass
        self.logstimeinfo(run)

    # 打印请求参数
    def requestsurllog(self, info, type, url, data):
        self.logstimeinfo(info)
        urllog = f"[{type}]  {url}"
        self.logstimeinfo(urllog)
        if type == 'POST':
            self.logstimeinfo(data)
        else:
            pass

    # 打印调用接口参数
    def requestsinfo(self, type, head, url, data, run):
        urllog = f"[{type}]  {url}"
        self.logstimeinfo(urllog)
        if type == 'POST':
            self.logstimeinfo(head)
            self.logstimeinfo(data)
        else:
            pass
        self.logstimeinfo(run)

    # 随机数(输入随机数位数，返回对应的值)
    def randommethod(self, sum):
        if int(sum)>0:
            a = '1'
            b = '9'
            for i in range(sum):
                if i > 0:
                    a += '0'
                    b += '9'
            data = random.randint(int(a), int(b))
        else:
            data = 0
        return data

    # 随机数
    def randoms(self, a, b):
        data = random.randint(int(a), int(b))
        return data


    # 订单组成规则
    def bizuseridinforule(self):
        time = self.utcnowtimedaydatetime()
        userid = BasicsOperation().regularstrint(time)[2:]
        return userid

    # 时间加*小时
    def dayTimeUpate(self, eta_temp, sum):
        import datetime
        fd = datetime.datetime.strptime(eta_temp, "%Y-%m-%d %H:%M:%S")
        # 加8后的时间
        eta = (fd + datetime.timedelta(hours=sum)).strftime("%Y-%m-%d %H:%M:%S")
        return eta




if __name__ == "__main__":
    logs = TimeMethod().timeyearmonthday(1)
    print(logs)