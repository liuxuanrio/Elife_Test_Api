from elife_app_ui_api_interface.driver_app_api.available.rides_sql import RidesSql
from elife_public_method.module_encapsulation.requests_method import requests_type


class Rides:
    def available_Accept(self, uptype):
        """
        available driver_app_Ride_Accept 抢单脚本数据处理接口  执行sql
        uptype: 0 初始化订单数据（修改订单状态到available list）
                1 修改抢单时间
                2 抢单时间等待
                3 修改订单价格
                4 抢单时间等待
                5 driver 接口接单
        """
        datalist = ["初始化订单数据", "修改抢单时间", "抢单时间等待", "修改订单价格", "抢单时间等待", "driver 接口接单"]
        data = datalist[uptype]
        if uptype == 0:
            RidesSql().initialize_ride()
        elif uptype == 1:
            RidesSql().updateAcceptTime()
        elif uptype == 2:
            RidesSql().updateCountTime(0)
        elif uptype == 3:
            RidesSql().updateAmount()
        elif uptype == 4:
            RidesSql().updateCountTime(1)
        elif uptype == 5:
            data = self.fleetAccept()
        else:
            data = "False"
        return data

    def fleetAccept(self):
        url = "https://b48pd87r0e.execute-api.us-east-2.amazonaws.com/dev/auctions/id/bids-ride?auction_id=3811&" \
              "ses=LcfppqurqpIxHeTNIXnvZjbsh8lSNePK8loVRm86ePLYkrHYMXJDsPzVTmCL72yz4vyvFN6VhfOzxaqtasZrx1BmRt5X" \
              "KyqQCWc4Ace3Zp4k8P5H23gKwKRIT1MZSYHi"
        head = {"Content-Type": "application/json"}
        data = {"currency": "USD",
                "amount": "33.44",
                "price_version": "0",
                "auction_time_str": "2022-12-22 10:23",
                "auction_utc": "1671675821",
                "req_id": "31e0835e-f8e6-4fe6-a291-bd308e9e07e7"}
        ret = requests_type("post", head, url, data)
        return ret


if __name__ == "__main__":
    print(Rides().fleetAccept())