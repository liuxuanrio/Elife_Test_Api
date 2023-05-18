import traceback
import pymysql
from elife_public_method.module_encapsulation.times_method import TimeMethod


class MYSQL_starter_test:
    # 连接数据库地址，如需连接其他库时可参数化连接参数
    def __init__(self):
        self.db = pymysql.connect(
        host="rideprod.c9y2b7qgnkr8.us-east-2.rds.amazonaws.com",
        user="dev_user",
        passwd="0TAnwLmMzDbCYMuf",
        db=f"ride",  # 库名
        charset="utf8"
    )
    # 传入sql语句查询所有值
    def ExecQuery(self, sql):
        TimeMethod().logstimeinfo(sql)
        cur=self.db.cursor()
        cur.execute(sql)
        resList = cur.fetchall()
        cur.close()
        TimeMethod().logstimeinfo(resList)
        return resList

    # 修改数据库信息
    def ExecNonQuery(self, sql):
        TimeMethod().logstimeinfo(sql)
        try:
            cur = self.db.cursor()
            cur.execute(sql)
            self.db.commit()
            cur.close()
        except:
            TimeMethod().logstimeinfo(traceback.format_exc())
            try:
                TimeMethod().logstimeinfo(sql)
                cur = self.db.cursor()
                cur.execute(sql)
                self.db.commit()
                cur.close()
            except:
                TimeMethod().logstimeinfo(traceback.format_exc())
                cur = self.db.cursor()
                cur.execute(sql)
                self.db.commit()
                cur.close()

    # 创建数据
    def ExecInstallQuery(self, sql, val):
        print(sql)
        print(val)
        try:
            cur = self.db.cursor()
            cur.executemany(sql, val)
            self.db.commit()
            cur.close()
        except:
            try:
                cur = self.db.cursor()
                cur.executemany(sql, val)
                self.db.commit()
                cur.close()
            except:
                cur = self.db.cursor()
                cur.executemany(sql, val)
                self.db.commit()
                cur.close()

if __name__ == "__main__":
    sql = "select from_unixtime(1684881000);"
    # sql = "select unix_timestamp('2023-02-23 12:00:00');"
    # sql = "SELECT date_format(date_sub(now(),interval -1 day), '%Y-%m-%d ')"
    #sql = "SELECT NOW(), date_format(NOW(), '%Y-%m-%d') FROM DUAL;"
    # time = "2021-10-01 10:00"
    # sql = "select date_format(current_timestamp,'yyyy-MM-dd HH:mm:ss')"
    # sql = "SELECT date_format(DATE_ADD(NOW(), INTERVAL 0 MINUTE), '%Y-%m-%d %H:%i') FROM DUAL"
    # sql = "select unix_timestamp('2022-12-10 03:47')"
    # ql = "SELECT date_format(NOW(), '%Y-%m-%d %H:%i:%s') FROM DUAL"
    # sql = "SELECT TIMESTAMPDIFF(Second,(SELECT date_format(NOW(), '%Y-%m-%d %H:%i:%s') FROM DUAL), '2023-02-08 14:20:00')"
    # sql = "select from_utc,inserted_at from ride.dispatch where ride_id = '127349' and stat = '134217729' and to_fleet_id = '40';"
    ret = MYSQL_starter_test().ExecQuery(sql)
    print(ret)