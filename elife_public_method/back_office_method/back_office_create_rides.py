import time

import requests

from elife_public_method.back_office_method.driver_app_rides import DriverAppRides
from elife_public_method.login_encryption.elife_login import ElifeLogin
from elife_public_method.module_encapsulation.pymysql_method import MYSQL_starter_test
from elife_public_method.module_encapsulation.requests_method import requests_type, requests_Parameters
from elife_public_method.module_encapsulation.strfloatditeall_method import BasicsOperation
from elife_public_method.module_encapsulation.times_method import TimeMethod

head = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "Content-Length": "12"}

class CreateNewRide:
    # 获取位置信息
    def placesid(self, name, ses):
        # 查询地址名称加密
        nametext = BasicsOperation().urllib_encryption(name)

        # 调用查询地址接口
        url = "https://e3s6es4ybc.execute-api.us-east-2.amazonaws.com/dev/maps/places/auto-comp?" \
              f"input_text={nametext}&location=37.6213129,-122.3789554&radius=200000"
        heads = {"content-type": "charset=UTF-8"}
        data = requests_type("get", heads, url, "")
        print("模糊查询地址信息结果：", data)
        id = data["predictions"]["predictions"][0]["place_id"]

        # 查询是否有航班信息
        flights = self.flightsInfo(id)
        print("获取航班信息：", flights)
        if len(flights["flights"]) > 0:
            flightindex = TimeMethod().randoms(0, len(flights["flights"])-1)
            print(flightindex)
            flightid = flights["flights"][flightindex]["id"]
        else:
            flightid = ""

        # 获取位置详细信息
        url = f"https://e3s6es4ybc.execute-api.us-east-2.amazonaws.com/dev/maps/places/id?google_place_id={id}"
        placesinfo = requests_type("get", heads, url, "")
        print("获取位置详细信息：", placesinfo)

        # 获取查询到的地址名称
        name = placesinfo["place_detail"]["result"]["name"]

        # 获取经纬度
        lat = placesinfo["place_detail"]["result"]["geometry"]["location"]["lat"]
        lng = placesinfo["place_detail"]["result"]["geometry"]["location"]["lng"]

        # 上传地址
        url = f"https://d46umqzje5.execute-api.us-east-2.amazonaws.com/dev/places?ses={ses}"
        adddata = {"name": name,
                "google_place_id": id,
                "lat": lat,
                "lng": lng,
                "address[formatted_address]": placesinfo["place_detail"]["result"]["formatted_address"]
                }

        # 循环提取查询的地址详情
        address = placesinfo["place_detail"]["result"]["address_components"]
        for i in range(len(address)):
            adddata[f"address[address_components][{i}][long_name]"] = address[i]["long_name"]
            adddata[f"address[address_components][{i}][short_name]"] = address[i]["short_name"]
            adddata[f"address[address_components][{i}][types][]"] = address[i]["types"]

        # 提交选择的地址信息返回id
        res = requests_Parameters(head, url, adddata)
        print("提交地址信息结果：", res)

        datas = {"lat": lat, "lng": lng, "id": res["id"], "flightid": flightid}
        return datas

    # 获取距离，时间
    def distance(self, from_lat, from_lng, to_lat, to_lng):
        url = "https://e3s6es4ybc.execute-api.us-east-2.amazonaws.com/dev/maps/routes/distance-time?" \
              "from_lat=31.1538374&from_lng=121.4307971&to_lat=31.192209&to_lng=121.334297"
        head = {"content-type": "charset=UTF-8"}
        datas = requests_type("get", head, url, "")
        return datas

    # 获取时差
    def timeutc(self, loc, dt, timeinfo):
        url = "https://e3s6es4ybc.execute-api.us-east-2.amazonaws.com/dev/maps/timezones/location/date-time?" \
              f"loc={loc}&dt={dt} {timeinfo}"
        print(url)
        head = {"content-type": "charset=UTF-8"}
        datas = requests_type("get", head, url, "")
        print(datas)
        return datas

    # 获取顾客id
    def customer(self, ses):
        url = "https://sdvjt4r4yl.execute-api.us-east-2.amazonaws.com/dev/customers?" \
              f"ses={ses}"
        data = {"person[salutation]": "Mr.",
                "person[first_name]": "rio",
                "person[middle_name]": "",
                "person[last_name]": "",
                "cell_phones[0][id]": "",
                "cell_phones[0][number]": "+861777777",
                "email": "rio@qq.com"}
        ret = requests.request("post", url=url, data=data, headers=head)
        res = ret.json()
        return res

    # 获取航班信息
    def flightsInfo(self, placeid):
        url = f"https://7tazk1dro3.execute-api.us-east-2.amazonaws.com/dev/flights?to_google_place_id={placeid}"
        head = {"content-type": "charset=UTF-8"}
        ret = requests_type("get", head, url, "")
        return ret

    # 创建订单
    def createRide(self, ses, fname, tname, fleetid, timesum, timeinfo, fleetids, ridetype, ctType, servicetype):
        # 当前日前转数字
        referenceid = TimeMethod().intnowtimedaydatetime()
        # 随机金额
        amount = TimeMethod().randoms(10, 100)
        # 起点
        frominfo = self.placesid(fname, ses)
        # 终点
        time.sleep(2)
        toinfo = self.placesid(tname, ses)

        # 获取距离时间
        distance = self.distance(frominfo["lat"], frominfo["lng"], toinfo["lat"], toinfo["lng"])

        loc = f"""{frominfo["lat"]},{frominfo["lng"]}"""
        print(loc)
        # 获取明天日期
        dtime = TimeMethod().timeyearmonthday(-timesum)
        # 获取时差
        utc = int(self.timeutc(loc, dtime, timeinfo)["utc"])
        time_str = f"""{dtime} {timeinfo}"""

        # 增加顾客信息
        # customer_id = self.customer(ses)
        customer_id = {"customer_id": "53584"}

        url = f"https://7poy9okvyg.execute-api.us-east-2.amazonaws.com/dev/rides?ses={ses}"
        data = {"partner[id]": "11",
                "partner[reference]": referenceid,
                "partner[currency]": "USD",
                "partner[amount]": amount,
                "service_area_id": "3247",
                "from[place_id]": frominfo["id"],
                "from[utc]": utc,
                "from[time_str]": time_str,
                "from[timezone_str]": "China Standard Time",
                "from[daylight]": False,
                "to[place_id]": toinfo["id"],
                "from_flight_sch_id": frominfo["flightid"],
                "from_flight_str": "",
                "to_flight_sch_id": toinfo["flightid"],
                "to_flight_str": "",
                "distance": distance["distance"],
                "duration": distance["time"],
                "vehicle_class_id": "1",
                "trip_count": "1",
                "passenger_count": "2",
                "luggage_count": "2",
                "children_count": "0",
                "infant_count": "0",
                "meet_and_greet": False,
                "customer_id": customer_id["customer_id"],
                "driver_sign": "welcome Mr.rio!",
                "driver_instruction": "Keep the vehicle clean and tidy"}
        if frominfo["flightid"] or toinfo["flightid"]:
            data["meet_and_greet"] = 'true'
        print(data)
        if servicetype == 1:
            data["service_area_id"] = '272'
            # data["service_area_id"] = '11343'
        ret = requests.request("post", url=url, data=data, headers=head)
        res = ret.json()
        print(res)
        id = res["ride_id"]
        statid = res["ride_stat"]
        # 获取订单信息
        # self.ridesinfo(ses, id, statid)
        # 分配车队（抢单）
        if ctType == 0:  # 调用接口指派订单
            if ridetype == 1:
                self.findFleet(ses, res["ride_id"], fleetid)
                if fleetids:  # 分配第二个车队
                    self.findFleet(ses, res["ride_id"], fleetids)
            else:
                # 指派车队
                self.newRidesFleet(ses, id, fleetid, amount)
        else:  # 数据库插入抢单记录(服务区内车队)
            self.addAuction(amount, id, fleetid, ctType)
        return res

    # 添加车队,抢单流程
    def findFleet(self, ses, id, fleetid):
        # self.ridesinfo(ses, id, 134610945)
        # self.fleetlist(ses, id)
        url = f"https://b48pd87r0e.execute-api.us-east-2.amazonaws.com/dev/auctions/ride?ses={ses}"
        # 随机金额
        amount = TimeMethod().randoms(10, 100)
        data = {"ride_id": id,
                "trip_no": 0,
                "environment": "Dev",
                "fleets[0][id]": fleetid,
                "fleets[0][currency]": "USD",
                "fleets[0][amount]": amount}
        print(data)
        ret = requests.request("post", url=url, data=data, headers=head)
        res = ret.json()
        print(res)
        return res

    # 指派车队
    def newRidesFleet(self, ses, id, fleetid, amount):
        url = f"https://i3ik0u41zi.execute-api.us-east-2.amazonaws.com/dev/dispatches?ses={ses}"
        data = {
            "ride_id": id,
            "from_fleet_id": 40,
            "to_fleet_id": fleetid,
            "currency": "USD",
            "amount": amount
        }
        ret = requests_Parameters(head, url, data)
        print(ret)
        return ret

    # 获取车队列表
    def fleetlist(self, ses, id):
        url = f"https://mqpd2xstgc.execute-api.us-east-2.amazonaws.com/dev/sql-templates/run?ses={ses}"
        data = {"ride_id": id,
                "id": "0",
                "sql": "134677701",
                "rows_to_fetch": "3001"}
        ret = requests.request("post", url=url, data=data, headers=head)
        res = ret.json()
        print(res)
        return res

    # 获取订单数据
    def ridesinfo(self, ses, id, typeid):
        url = f"https://rif8m0lk5l.execute-api.us-east-2.amazonaws.com/dev/access-tokens?ses={ses}"
        data = {"resource_type": typeid,
                "resource_id": id}
        ret = requests.request("post", url=url, data=data, headers=head)
        res = ret.json()
        print(res)
        return res

    # 订单写表(服务区内订单)
    def addAuction(self, amount, rideId, fleetid, rideType):
        sql = "SELECT date_format(DATE_ADD(NOW(), INTERVAL 0 MINUTE), '%Y-%m-%d %H:%i:%s') FROM DUAL"
        time = MYSQL_starter_test().ExecQuery(sql)[0][0]
        # 创建 Auction 记录
        addAuctionSql = "INSERT INTO `ride`.`auction` (`currency`, `amount`, `price_version`, `active`, `start_utc`, " \
                        "`start_time_str`, `inserted_at`, `last_updated_at`) VALUES " \
                        f"(%s, %s, %s, %s, %s, %s, %s, %s);"
        if rideType == 1:
            addAuctionVal = [('USD', amount, '0', '1', '1676232000', '2023-02-13 04:00', time, time)]
        else:
            addAuctionVal = [(None, 0, '0', '1', '1676232000', '2023-02-13 04:00', time, time)]
        ret = MYSQL_starter_test().ExecInstallQuery(addAuctionSql, addAuctionVal)
        print(ret)

        # 查询创建的记录id
        selectIdSql = f"select id from ride.auction where elife_price is null and " \
                      "start_utc = '1676232000' order by id desc limit 1;"
        id = MYSQL_starter_test().ExecQuery(selectIdSql)[0][0]
        print("auction id = ", str(id))

        # 创建 auction_ride表记录
        addRideSql = "INSERT INTO `ride`.`auction_ride` (`auction_id`, `ride_id`, `trip_no`, `trip_no_x`, " \
                     "`inserted_at`, `last_updated_at`) VALUES " \
                     "(%s, %s, %s, %s, %s, %s);"
        addRideVal = [(id, rideId, '0', '0', time, time)]
        MYSQL_starter_test().ExecInstallQuery(addRideSql, addRideVal)

        # 创建 auction_fleet表记录(指派车队)
        if rideType > 1:
            addRideSql = "INSERT INTO `ride`.`auction_fleet` (`amount`, `currency`, `fleet_id`, `auction_id`, " \
                         "`inserted_at`, `last_updated_at`) VALUES " \
                         "(%s, %s, %s, %s, %s, %s);"
            addRideVal = [(amount, "USD", fleetid, id, time, time)]
            MYSQL_starter_test().ExecInstallQuery(addRideSql, addRideVal)


    # 随机地址
    def placesRandom(self, placeslist):
        latname = placeslist[TimeMethod().randoms(0, len(placeslist)-1)]
        placeslist.remove(latname)
        lngname = placeslist[TimeMethod().randoms(0, len(placeslist)-1)]
        placeslist.append(latname)
        data = [latname, lngname]
        print(data)
        return data

# 执行脚本
class RunScript:
    # 获取一个账号的抢单列表订单，把这些订单分配给其他账号
    def ridesAssign(self, backses):
        # 登录账号driver app
        appses = ElifeLogin().driverAppLogin("riotestbb@qq.com")
        # 获取rides列表订单
        data = DriverAppRides().ridesAvailableList(appses)
        for i in range(len(data["results"])):
            # 获取id
            rideId = data["results"][i]["ride_id"]
            # 指派订单
            CreateNewRide().findFleet(ses, rideId, 11266)

    # 修改订单为按时间的订单
    def updateRideTime(self, rideid):
        sql = f"UPDATE `ride`.`ride` SET `distance` = '1', `duration` = '18000' WHERE (`id` = '{rideid}');"
        MYSQL_starter_test().ExecNonQuery(sql)

    # 修改进行中的订单为accepted
    def updateRideStatUnderway(self, fleetid):
        sql = f"update ride.dispatch set stat = '134217730' where to_fleet_id = '{fleetid}' " \
              f"and stat in ('134217732', '134217733', '134217734');"


    # 生成随机订单时间
    def randomTime(self, sum, timesum, namelist, fleetid, fleetids, ses, ridetype, ctType, servicetype):
        ctsum = 0
        for i in range(sum):
            timesum += 1
            hour = TimeMethod().randoms(0, 23)
            for time in range(1):
                if hour >23:
                    break
                minute = TimeMethod().randoms(0, 59)
                hours = f"{hour}"
                minutes = f"{minute}"
                if hour < 10:
                    hours = f"0{hour}"
                if minute < 10:
                    minutes = f"0{minute}"
                timedata = f"{hours}:{minutes}"
                addsum = TimeMethod().randoms(5, 12)
                hour += addsum
                ctsum += 1
                namelistinfo = CreateNewRide().placesRandom(namelist)
                # namelistinfo = namelist
                CreateNewRide().createRide(ses, namelistinfo[0], namelistinfo[1], fleetid, timesum, timedata, fleetids, ridetype, ctType, servicetype)
        print(ctsum)



if __name__ == "__main__":
    ses = "PqxDtFhs3reWdAMeQzlK4SNVmSHm7q1ed0s8jatx7jnasOgaFZEWYO0wMkpnjUMFhoRnDrjlXfXOSlcjKCfBalNncF6gDFPa9cUtoO2LcMvfn9ptSWqzdwtKNhVbU2DT"
    fleetid = 11255
    fleeid = ["riotest@qq.com 11236", "riotestaa@qq.com 11255", "riotestbb@qq.com 11257", "riotestcc@qq.com 11266",
              "riotestff@qq.com 11324"]
    placeslist = ["上海浦东国际机场", "上海南站", "上海虹桥国际机场", "上海西站", "上海迪士尼乐园", "上海野生动物园", "上海东方明珠",
                    "上海科技馆", "上海城隍庙"]
    # placeslist = ["Apalachicola Regional Airport 8 Airport Rd, Apalachicola, FL 32320, USA",
                  # "3511 Garrison Ave, Port St Joe, FL 32456, USA"]
    # placeslist = ["Apalachicola Regional Airport", "Box-R Wildlife Management Area", "Apalachicola, FL 32320, USA"]
    # placeslist = ["San Francisco International Airport San Francisco, CA 94128, USA San Francisco, CA 94128, USA",
    #               "Oakland International Airport 1 Airport Dr, Oakland, CA 94621, USA"]
    timesum = 5
    start = time.time()
    ridetype = 1        # 1 available   2 new rides
    ctType = 2          # 0 接口指派订单  1 数据库写入地区内所有车队  2 数据库写入指派车队
    servicetype = 0     # 0 Test Sh 1 AAF
    RunScript().randomTime(10, timesum, placeslist, fleetid, "", ses, ridetype, ctType, servicetype)
    # CreateNewRide().addAuction(171.73, 129288, 11255, 2)
    # CreateNewRide().addAuction("128", '127049')
    end = time.time()
    print('程序运行时间为: %s Seconds' % (end - start))
    # RunScript().updateRideTime("129287")









