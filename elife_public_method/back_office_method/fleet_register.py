from elife_public_method.module_encapsulation.requests_method import requests_Parameters
from elife_public_method.module_encapsulation.times_method import TimeMethod

head = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "Content-Length": "72"}


class RegisterFleet:
    def flt_up_unverified(self, name, email, phone, airports):
        url = "https://tkduvoscb4.execute-api.us-east-2.amazonaws.com/dev/fleets-unverified"
        data = {"name": name,
                "role": "personal",
                "fleet_name": name,
                "email": email,
                "vehicle_classes[]": [1, 3],
                "password": "riotest",
                "cellNumber": phone,
                "airports[]": airports,
                "languages[]": ["zho", "eng"],
                "req_id": "68e00d64-02e7-46ba-afd7-ff3800bdfd7c"
                }
        ret = requests_Parameters(head, url, data)
        return ret

class RegisterScript:
    def fleetScript(self, state):
        template = {
            "China": ["86", "PVG"],
            "USA": ["1", "AAF"],
            "JPN": ["81", "CTS"],
            "Mexico": ["52", "CEN"],
            "MYS": ["60", "IPH"],
            "BSH": ["1242", "NAS"],
            "MTQ": ["596", "FDF"]
        }
        # 获取当前日期
        day = TimeMethod().intnowtimedaydatetime()
        if state == "BSH":
            day = day[3:]
        phone = f"+{template[state][0]}{day}"
        name = f"rio{day}"
        email = f"rio{day}@qq.com"
        print(email)
        airports = template[state][1]
        data = RegisterFleet().flt_up_unverified(name, email, phone, airports)
        print(data)


if __name__ == "__main__":
    data = RegisterScript().fleetScript("China")
