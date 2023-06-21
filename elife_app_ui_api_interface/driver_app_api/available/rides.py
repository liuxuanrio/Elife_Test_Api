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
                pass
            elif uptype == 1:
                pass
            elif uptype == 2:
                pass
            elif uptype == 3:
                pass
            elif uptype == 4:
                pass
            else:
                data = "False"
        except:
            import traceback
            data = str(traceback.print_exc())
            print(data)
        return data
