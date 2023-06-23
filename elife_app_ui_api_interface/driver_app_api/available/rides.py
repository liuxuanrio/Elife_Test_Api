from elife_app_ui_api_interface.driver_app_api.available.rides_sql import RidesSql


class Rides:
    def available_Accept(self, uptype):
        """
        available driver_app_Ride_Accept 抢单脚本数据处理接口  执行sql
        uptype: 0 初始化订单数据（修改订单状态到available list）
                1 修改抢单时间
                2 抢单时间等待
                3 修改价格
                4 抢单时间等待
        """
        data = ""
        try:
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
            else:
                data = "False"
        except:
            import traceback
            data = str(traceback.print_exc())
            print(data)
        return data
