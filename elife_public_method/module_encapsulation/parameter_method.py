# 接口返回通用模板
def returndata(flag, datas):
    if int(flag) == 1:
        data = {
            "code": "200",
            "msg": "成功",
            "data": datas
        }
    else:
        data = {
            "code": "500",
            "msg": "失败",
            "data": ""
        }
    return data

# 定义接口返回信息
def returninfo(code, msg, data):
    data = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return data
