from elife_public_method.module_encapsulation.pymysql_method import MYSQL_starter_test
from elife_public_method.module_encapsulation.times_method import TimeMethod


class RidesSql:
    def initialize_ride(self):
        """
        初始化available driver_app_Ride_Accept 抢单脚本数据
        1、修改订单时间
        2、修改订单状态
        """
        rideList = [116214, 116216, 116215, 116216]
        strList = [960, 1080, 1920, 2040]
        utcList = [480, 600, 1440, 1560]
        for i in range(len(rideList)):
            if i == 3:
                sql = "update ride.ride set to_utc = (select unix_timestamp(" \
                      f"(SELECT date_format(DATE_ADD(NOW(), INTERVAL '{utcList[i]}' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL))), " \
                      f"to_time_str = (SELECT date_format(DATE_ADD(NOW(), INTERVAL '{strList[i]}' MINUTE), '%Y-%m-%d %H:%i')" \
                      f" FROM DUAL)  where id = {rideList[i]};"

                sql1 = "update ride.dispatch set to_utc = (select unix_timestamp" \
                       f"((SELECT date_format(DATE_ADD(NOW(), INTERVAL '{utcList[i]}' MINUTE), '%Y-%m-%d %H:%i')" \
                       f" FROM DUAL))) where ride_id ='{rideList[i]}' and id = '45011';"
            else:
                sql = "update ride.ride set from_utc = (select unix_timestamp(" \
                      f"(SELECT date_format(DATE_ADD(NOW(), INTERVAL '{utcList[i]}' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL))), " \
                      f"from_time_str = (SELECT date_format(DATE_ADD(NOW(), INTERVAL '{strList[i]}' MINUTE), '%Y-%m-%d %H:%i')" \
                      f" FROM DUAL)  where id = {rideList[i]};"

                sql1 = "update ride.dispatch set from_utc = (select unix_timestamp" \
                       f"((SELECT date_format(DATE_ADD(NOW(), INTERVAL '{utcList[i]}' MINUTE), '%Y-%m-%d %H:%i')" \
                       f" FROM DUAL))) where ride_id ='{rideList[i]}'"
            MYSQL_starter_test().ExecNonQuery(sql)
            MYSQL_starter_test().ExecNonQuery(sql1)

        sqlList = [["update ride.dispatch set stat = '134217736', fleet_driver_id = null, meeting_place_id=null, "
                    "reversal=null,trip_no_x=null where to_fleet_id in ('11466','11468') and ride_id in (116214,116216,116215,116216);"],
                   ["update ride.ride set dispatch_fleet_id = null where dispatch_fleet_id in ('11466','11468');"],
                   ["delete from ride.auction_bid where auction_id in (select auction_id from "
                    "ride.auction_fleet where fleet_id in ('11466','11468'));"],
                   ["update ride.auction set fleet_id = null where id in (select auction_id from "
                    "ride.auction_fleet where fleet_id in ('11466','11468'));"],
                   ["delete from ride.dispatch_prepayment where dispatch_id in "
                    "(select id from ride.dispatch where to_fleet_id in ('11466','11468'));"],
                   ["delete from ride.note_dispatch where dispatch_id in (select id from "
                    "ride.dispatch where to_fleet_id in ('11466','11468'));"],
                   ["update ride.auction_ride set trip_no_x = 1 where auction_id in (select auction_id from "
                    "ride.auction_fleet where fleet_id = '11466' and auction_id = '3814');"],
                   ["update ride.auction_fleet set amount = '66.66' where auction_id = '3813' and id = '155';"]]
        for sql in sqlList:
            MYSQL_starter_test().ExecNonQuery(sql[0])

    def updateAcceptTime(self):
        """
        1、修改订单抢单时间为2分钟后和4分钟后
        """
        sql = "update ride.auction set start_utc = (select unix_timestamp((SELECT date_format(DATE_ADD(NOW(), " \
              "INTERVAL '2' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL))),start_time_str = (SELECT date_format" \
              "(DATE_ADD(NOW(), INTERVAL '482' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL) where id = '3812';"
        MYSQL_starter_test().ExecNonQuery(sql)

        sql1 = "update ride.auction set start_utc = (select unix_timestamp((SELECT date_format" \
               "(DATE_ADD(NOW(), INTERVAL '4' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL))),start_time_str = " \
               "(SELECT date_format(DATE_ADD(NOW(), INTERVAL '484' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL) " \
               "where id = '3814';"
        MYSQL_starter_test().ExecNonQuery(sql1)

    def updateCountTime(self, idType):
        """
        获取数据库中抢单时间
        计算当前时间到抢单时间差值，并做等待
        """
        data = ""
        idList = ["3812", "3814"]
        sql = f"select start_time_str from ride.auction where id = {idList[idType]}"
        strTime = MYSQL_starter_test().ExecQuery(sql)[0][0]
        time = TimeMethod().nowtimedaydatetime()
        timeValue = TimeMethod().countTime(f"{strTime}:00", time)
        if timeValue > 0:
            if timeValue > 60 and timeValue < 240:
                sumtime = timeValue
                for i in range(5):
                    if sumtime > 60:
                        time.sleep(60)
                        sumtime -= 60
                    else:
                        time.sleep(sumtime)
                        break
            elif timeValue <= 60:
                time.sleep(timeValue)
            else:
                print(f"等待时间超过4分钟：{str(timeValue)}")
                data = f"等待时间超过4分钟：{str(timeValue)}"
        else:
            print(f"等待时间已过期：{str(timeValue)}")
            data = f"等待时间已过期：{str(timeValue)}"
        return data

    def updateAmount(self):
        """
        1、修改订单价格
        """
        sql = "update ride.auction_fleet set amount = '120' where auction_id = '3813' and id = '155';"
        MYSQL_starter_test().ExecNonQuery(sql)


if __name__ == "__main__":
    pass
    print(RidesSql().initialize_ride())