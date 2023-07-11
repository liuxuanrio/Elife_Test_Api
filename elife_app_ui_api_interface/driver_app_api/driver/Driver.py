from elife_app_ui_api_interface.driver_app_api.driver.vehicleClass import vehicleClass
from elife_public_method.module_encapsulation.pymysql_method import MYSQL_starter_test


class Drivers:
    def vehicleXlsx(self):
        from openpyxl.reader.excel import load_workbook
        excelDir = fr'./vehicle_map.xlsx'  # 打开xlsx文件
        workBook = load_workbook(excelDir)
        workSheet = workBook.worksheets[0]
        vehicleClass = []
        idList = []
        nameList = []
        rowsum = 1
        vehicle = {}
        id = 0
        for row in workSheet.rows:
            colsum = 1
            lst = []
            for col in row:
                if rowsum == 1:
                    rowstr = col.value
                    vehicleClass.append(self.strJson(rowstr))
                else:
                    rowstr = col.value
                    if colsum == 1:
                        rowList = rowstr.split("（")
                        id = int(rowList[1][:-1])
                        name = rowList[0]
                        idList.append(id)
                        nameList.append(name)
                    else:
                        if rowstr == "T":
                            lst.append(vehicleClass[colsum-1])
                colsum += 1
            vehicle[id] = {"results": lst}
            rowsum += 1
        workBook.close()
        return vehicle

    def strJson(self, rowstr):
        if rowstr != None:
            rowList = rowstr.split("（")
            return {"id": int(rowList[1][:-1]), "name": rowList[0]}
        else:
            return {"id": rowstr, "name": rowstr}

    def vehicleClassSum(self):
        sql = "select from_vehicle_id from ride.fleet_to_ride_vehicle_mapping group by from_vehicle_id;"
        vehicle = MYSQL_starter_test().ExecQuery(sql)
        vehicle2 = vehicleClass()
        vehicleList2 = list(vehicle2.keys())
        vehicleList1 = []
        for id in vehicle:
            vehicleList1.append(id[0])
        print(list(set(vehicleList1) ^ set(vehicleList2)))

    def retVehicle(self, vehicleId):
        vehicleJson = vehicleClass()
        if len(vehicleId) > 1:
            resultsList = vehicleJson[int(vehicleId[0])]
            for id in vehicleId[1:]:
                for results in vehicleJson[int(id)]["results"]:
                    if results in resultsList["results"]:
                        pass
                    else:
                        resultsList["results"].append(results)
            return resultsList
        else:
            return vehicleJson[int(vehicleId[0])]










if __name__ == "__main__":
    print(Drivers().vehicleClassSum())
    # for i in bb["results"]:
    #     if i in aa["results"]:
    #         pass
    #     else:
    #         aa["results"].append(i)
    # print(aa)