import requests, json

from elife_public_method.login_encryption.elife_login import ElifeLogin
from elife_public_method.module_encapsulation.pymysql_method import MYSQL_starter_test
from elife_public_method.module_encapsulation.requests_method import requests_Parameters
from elife_public_method.module_encapsulation.times_method import TimeMethod

head = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "Content-Length": "12"}

# driver app rides页面api
class DriverAppRides:
    # rides Available 列表订单接口
    def ridesAvailableList(self, ses):
        url = f"https://mqpd2xstgc.execute-api.us-east-2.amazonaws.com/dev/sql-templates/run?ses={ses}"
        data = {"dispatch_id": 0,
                "from_utc": 0,
                "fleet_id": 11236,
                "vehicle_classes[]": [1, 3, 6],
                "sql": 134677705,
                "rows_to_fetch": 100
                }
        ret = requests_Parameters(head, url, data)
        return ret

    # new rides list
    def newRidesList(self, ses):
        url = f"https://mqpd2xstgc.execute-api.us-east-2.amazonaws.com/dev/sql-templates/run?ses={ses}"
        data = {"dispatch_id": 0,
                "from_utc_start": 0,
                "from_utc_end": "1924905600",
                "order": "asc",
                "dispatch_stat[]": "134217729",
                "sql": 134676597,
                "rows_to_fetch": 51
                }
        ret = requests.request("post", url=url, data=data, headers=head)
        print(ret.json())
        return ret.json()

    # rides detail
    def newRidesDetail(self, fromstart, fromend, start, ses):
        url = f"https://mqpd2xstgc.execute-api.us-east-2.amazonaws.com/dev/sql-templates/run?ses={ses}"
        data = {"sql": 134676597,
                "dispatch_id": 0,
                "from_utc_start": fromstart,
                "from_utc_end": fromend,
                "order": "asc",
                "dispatch_stat[]": start,
                "rows_to_fetch": 100}
        ret = requests_Parameters(head, url, data)
        return ret

    # 获取车队信息
    def fleetInfo(self, dispatch_id, ses):
        url = f"https://mqpd2xstgc.execute-api.us-east-2.amazonaws.com/dev/sql-templates/run?ses={ses}"
        data = {"sql": 134676499, "dispatch_id": dispatch_id}
        ret = requests_Parameters(head, url, data)
        print(ret)
        return ret

    # driver list
    def driverList(self, ses):
        url = f"https://mqpd2xstgc.execute-api.us-east-2.amazonaws.com/dev/sql-templates/run?ses={ses}"
        data = {"sql": 135200775,
                "ride_service_area_id": 11325,
                "rows_to_fetch": 10000}
        ret = requests_Parameters(head, url, data)
        print(ret)
        return ret

    # add driver
    def addDriver(self, ses, name, phone):
        url = f"https://mqpd2xstgc.execute-api.us-east-2.amazonaws.com/dev/sql-templates/run?ses={ses}"
        data = {"sql": 134677893,
                "service_area_id": 11256,
                "name": name,
                "person[salutation]": "",
                "person[first_name]": name,
                "person[middle_name]": "",
                "person[last_name]": "",
                "cell_phone": phone,
                "lang_names[0][nat_lang]": "eng",
                "req_id": "4b6d5c9d-06bb-4f71-b0c6-75dfc5ee49af"
                }
        ret = requests_Parameters(head, url, data)
        print(ret)
        return ret

    # new rides Accept
    def newRidesAccept(self, rideid, driverid, ses):
        url = f"https://i3ik0u41zi.execute-api.us-east-2.amazonaws.com/dev/dispatches/{rideid}?ses={ses}"
        print(url)
        data = {"stat": "134217730", "fleet_driver_id": driverid}
        heads = {"content-type": "application/json"}
        ret1 = requests.request("OPTIONS", headers=heads, url=url)
        ret = requests.request("PATCH", headers=head, url=url, data=json.dumps(data))
        print(ret.json())
        return ret

class UpdateRide():
    def selectTime(self):
        # 获取一个月后的日期
        time = TimeMethod().timeyearmonthday(-30)
        time = f"{time} 00:00"
        utcsql = f"select unix_timestamp('{time}');"
        utc = MYSQL_starter_test().ExecQuery(utcsql)[0][0]
        print(utc)
        return time, utc

    def updateRideTimeSql(self, rideid, time, utc):
        # 修改ride 表订单时间
        sql = f"update ride.ride set from_utc = '{utc}', from_time_str = '{time}' where id ='{rideid}'"
        MYSQL_starter_test().ExecNonQuery(sql)

        # 修改dispatch表订单时间
        sql = f"update ride.dispatch set from_utc = '{utc}' where ride_id = '{rideid}'"
        MYSQL_starter_test().ExecNonQuery(sql)

class ActionItem:
    def addAction(self, sum, fleetid, title):
        new = TimeMethod().timeyearmonthday(sum)
        hour = TimeMethod().randoms(0, 23)
        minute = TimeMethod().randoms(0, 59)
        second = TimeMethod().randoms(0, 59)
        if len(str(hour)) < 2:
            hour = f"0{hour}"
        if len(str(minute)) < 2:
            minute = f"0{minute}"
        if len(str(second)) < 2:
            second = f"0{second}"
        due_date = f"{new} {hour}:{minute}:{second}"
        print(due_date)
        due_date_str = due_date[0: -3]
        due_date_utc_sql = f"select unix_timestamp('{due_date}');"
        due_date_utc = MYSQL_starter_test().ExecQuery(due_date_utc_sql)[0][0]
        sql = "SELECT date_format(DATE_ADD(NOW(), INTERVAL 0 MINUTE), '%Y-%m-%d %H:%i') FROM DUAL"
        time = MYSQL_starter_test().ExecQuery(sql)[0][0]

        # 新增action_item_fleet记录
        addActionSql = "INSERT INTO `ride`.`action_item_fleet` (`fleet_id`, `title`, `due_date`, `due_date_str`, " \
                       "`due_date_utc`, `inserted_at`, `last_updated_at`) VALUES " \
                       "(%s, %s, %s, %s, %s, %s, %s);"
        addActionVal = [(fleetid, title, due_date, due_date_str, due_date_utc, time, time)]
        ret = MYSQL_starter_test().ExecInstallQuery(addActionSql, addActionVal)
        print(ret)

        # # 新增note_action 记录
        # addNoteSql = "INSERT INTO `ride`.`note_action` (`notes`, `action_id`, `inserted_at`, " \
        #              "`last_updated_at`) VALUES " \
        #              "('driver on show info', '14', '2023-02-21 17:23:00', '2023-02-21 17:23:00');"
        # addNoteVal = [(note)]

    def updateRideTime(self):
        exptime = TimeMethod().timeyearmonthday(-10)
        rideList = DriverAppRides().ridesAvailableList(ses)["results"]
        # 获取修改的时间
        timelist = UpdateRide().selectTime()
        time = timelist[0]
        utc = timelist[1]
        for ride in rideList:
            UpdateRide().updateRideTimeSql(ride["ride_id"], time, utc)
            print(ride["ride_id"], ride["from_time_str"])
            if ride["from_time_str"] > f"{exptime} 00:00":
                break
        print(rideList)


if __name__ == "__main__":
    # ses = ElifeLogin().driverAppLogin("riotestff@qq.com")
    ses = "eZXtaEqJRP7ygGmuwywS6yjwsOaDptUNls9Bz1LaSatAyppKkDE9kg4GqRK4Gcuh9jlX2vCjEFOoJYK2K8dati9boHRnYvaik2U6D" \
          "ThYungNAD6aK4Woi6NwOUTD8t67"
    ActionItem().updateRideTime()
    # UpdateRide().updateRideTimeSql()