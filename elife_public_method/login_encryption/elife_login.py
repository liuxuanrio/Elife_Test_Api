import requests, json

from elife_public_method.module_encapsulation.requests_method import requests_Parameters


class ElifeLogin:
    def backOfficeLogin(self):
        url = "https://t3bln7u6xa.execute-api.us-east-2.amazonaws.com/dev/login-seses-employee"
        head = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Content-Length": "12"}
        data = {"email": "gangye@elifetransfer.com", "password": "qweasdzxc"}
        loginret = requests.request("post", url=url, data=data, headers=head)
        ses = loginret.json()["ses"]
        return ses

    def driverAppLogin(self, email):
        url = "https://dd06r2adb9.execute-api.us-east-2.amazonaws.com/dev/login-seses-fleet-emp"
        head = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Content-Length": "12"}
        data = {"email": email, "password": "riotest"}
        ret = requests_Parameters(head, url, data)
        return ret["ses"]


if __name__ == "__main__":
    print(ElifeLogin().driverAppLogin(""))