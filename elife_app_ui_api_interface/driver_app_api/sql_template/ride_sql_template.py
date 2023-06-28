class RideSqlTemplate:
    def upRideTime(self, utc, str, ride):
        """
        修改ride表订单时间
        :param utc: 单位秒 修改为当前时间后多少秒
        :param str: 单位秒 修改为当前时间后多少秒 有8小时时差
        :param ride: 订单id
        :return: sql
        """
        sql = "update ride.ride set from_utc = (select unix_timestamp(" \
              f"(SELECT date_format(DATE_ADD(NOW(), INTERVAL '{utc}' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL))), " \
              f"from_time_str = (SELECT date_format(DATE_ADD(NOW(), INTERVAL '{str}' MINUTE), '%Y-%m-%d %H:%i')" \
              f" FROM DUAL)  where id = {ride};"
        return sql

    def upDispatchTime(self, utc, ride):
        """
        修改Dispatch表订单时间
        :param utc: 单位秒 修改为当前时间后多少秒
        :param ride: 订单id
        :return: sql
        """
        sql = "update ride.dispatch set from_utc = (select unix_timestamp" \
               f"((SELECT date_format(DATE_ADD(NOW(), INTERVAL '{utc}' MINUTE), '%Y-%m-%d %H:%i')" \
               f" FROM DUAL))) where ride_id ='{ride}'"
        return sql

    def upAuctionTime(self, utc, str, id, ride):
        """
        修改Auction表订单时间
        :param utc: 单位秒 修改为当前时间后多少秒
        :param str: 单位秒 修改为当前时间后多少秒 有8小时时差
        :param ride: 订单id
        :return: sql
        """
        if id:
            sql = "update ride.auction set start_utc = (select unix_timestamp((SELECT date_format(DATE_ADD(NOW(), " \
                  f"INTERVAL '{utc}' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL))),start_time_str = (SELECT date_format" \
                  f"(DATE_ADD(NOW(), INTERVAL '{str}' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL) where id = '{id}';"
        else:
            sql = "update ride.auction set start_utc = (select unix_timestamp((SELECT date_format(DATE_ADD(NOW(), " \
                  f"INTERVAL '{utc}' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL))),start_time_str = (SELECT date_format" \
                  f"(DATE_ADD(NOW(), INTERVAL '{str}' MINUTE), '%Y-%m-%d %H:%i') FROM DUAL) where id = " \
                  f"(select auction_id from ride.auction_ride where ride_id = {ride});"
        return sql
