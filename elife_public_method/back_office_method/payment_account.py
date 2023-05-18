import requests

from elife_public_method.module_encapsulation.requests_method import requests_Parameters
from elife_public_method.module_encapsulation.times_method import TimeMethod

head = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "Content-Length": "128"}

class Payment:
    def addAccount(self, i):
        url = 'https://wx487icstl.execute-api.us-east-2.amazonaws.com/dev/accounts/id/pymt-instruments?account_id=800&ses=Js0hDtH1eEQG8XIO7CDbeJMotzpUHIchchV6gLpmEzXaNArKTfQZMGWISJvW1zxiD8e8IFHUEgzObxVjfQyboI8exnp7Zn3IHUgSUvGHqGpeSnpoufSye7oQsu936nAD'
        data = {"json": i,
                "instrument_id": '1524'}
        ret = requests_Parameters(head, url, data)
        return ret


if __name__ == "__main__":
    # add = Payment().addAccount()
    # print(add)
    t = TimeMethod().intnowtimedaydatetime()
    for i in range(40):
        jsoninfo = """{"account_name": "rio%s","account_number": "rio%s","method": "Payoneer","alias": "rio%s"}""" %(i,t,i)
        print(jsoninfo)
        add = Payment().addAccount(jsoninfo)
        print(add)