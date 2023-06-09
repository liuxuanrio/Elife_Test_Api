# coding=UTF-8
import traceback
import flask, json
from gevent import pywsgi
from flask import request, Flask, render_template, send_from_directory, make_response

from elife_api_interface.auto_test_api.gmail import Gmail
from elife_api_interface.ctrip_test_api.getsign import ctrip_request
from elife_app_ui_api_interface.driver_app_api.account.account import LoginFleet
from elife_app_ui_api_interface.driver_app_api.available.rides import Rides
from elife_app_ui_api_interface.driver_app_api.driver.Driver import Drivers
from elife_public_method.module_encapsulation.parameter_method import returndata
from elife_api_interface.ctrip_test_api.ctripday import ctrip_day_request
from elife_public_method.module_encapsulation.times_method import TimeMethod

# 实例化api，把当前这个python文件当作一个服务，__name__代表当前这个python文件
api = Flask(__name__)

# userid,token公用方法
def tokenpublic(keylist):
    ren = {'msg': "成功"}
    for i in range(len(keylist)):
        data = flask.request.json.get(keylist[i])
        ren[keylist[i]] = data
    ren["reqMsg"] = json.loads(request.get_data())
    ren["post"] = request.url
    return ren

@api.route('/auto/AppUI/vehicle/class', methods=['post'])
def vehicle_Class():
    keylist = ["vehicleId"]
    msginfo = tokenpublic(keylist)
    try:
        ret = Drivers().retVehicle(msginfo["vehicleId"])
        ret = returndata(1, ret)
    except:
        ret = returndata(2, "")  # 打印报错信息
        TimeMethod().logstimeinfo(str(traceback.print_exc()))
    TimeMethod().logstimeinfo(ret)
    return json.dumps(ret, ensure_ascii=False)

@api.route('/auto/AppUI/login/fleet', methods=['post'])
def login_Fleet():
    keylist = ["state"]
    msginfo = tokenpublic(keylist)
    try:
        ret = LoginFleet().fleetScript(msginfo["state"])
        ret = returndata(1, ret)
    except:
        ret = returndata(2, "")  # 打印报错信息
        TimeMethod().logstimeinfo(str(traceback.print_exc()))
    TimeMethod().logstimeinfo(ret)
    return json.dumps(ret, ensure_ascii=False)


@api.route('/auto/AppUI/Available/Accept', methods=['post'])
def available_Accept():
    keylist = ["upType"]
    msginfo = tokenpublic(keylist)
    try:
        ret = Rides().available_Accept(msginfo["upType"])
        ret = returndata(1, ret)
    except:
        ret = returndata(2, "")  # 打印报错信息
        TimeMethod().logstimeinfo(str(traceback.print_exc()))
    TimeMethod().logstimeinfo(ret)
    return json.dumps(ret, ensure_ascii=False)

@api.route('/auto/AppUI/Booked/Ride', methods=['post'])
def booked_Ride():
    keylist = ["upType", "ride"]
    msginfo = tokenpublic(keylist)
    try:
        ret = Rides().booked_Ride(msginfo["upType"], msginfo["ride"])
        ret = returndata(1, ret)
    except:
        ret = returndata(2, "")  # 打印报错信息
        TimeMethod().logstimeinfo(str(traceback.print_exc()))
    TimeMethod().logstimeinfo(ret)
    return json.dumps(ret, ensure_ascii=False)


@api.route('/auto/gmail', methods=['GET', 'POST'])  # 获取gmail邮箱
def gmailroute():
    if (request.method == 'GET'):
        try:
            ret = Gmail().selectGmail(1)
            ret = returndata(1, ret)
        except:
            ret = returndata(2, "")  # 打印报错信息
    else:
        keylist = ["gmailType"]
        msginfo = tokenpublic(keylist)
        try:
            ret = Gmail().selectGmail(msginfo["gmailType"])
            ret = returndata(1, ret)
        except:
            ret = returndata(2, "")  # 打印报错信息
            TimeMethod().logstimeinfo(str(traceback.print_exc()))
    TimeMethod().logstimeinfo(ret)
    return json.dumps(ret, ensure_ascii=False)


@api.route('/auto/ctriproute', methods=['post'])
def ctriproute():
    keylist = ["body", "urlstr","env"]
    msginfo = tokenpublic(keylist)
    try:
        ret = ctrip_request(msginfo["body"], msginfo["urlstr"],msginfo["env"])
        ret = returndata(1, ret)
    except:
        ret = returndata(2, "")  # 打印报错信息
        TimeMethod().logstimeinfo(str(traceback.print_exc()))
    TimeMethod().logstimeinfo(ret)
    return json.dumps(ret, ensure_ascii=False)

#  ctrip多日程
@api.route('/auto/ctripday', methods=['post'])
def ctripday():
    keylist = ["body", "urlstr","env"]
    msginfo = tokenpublic(keylist)
    try:
        ret = ctrip_day_request(msginfo["body"], msginfo["urlstr"],msginfo["env"])
        ret = returndata(1, ret)
    except:
        ret = returndata(2, "")  # 打印报错信息
        TimeMethod().logstimeinfo(str(traceback.print_exc()))
    TimeMethod().logstimeinfo(ret)
    return json.dumps(ret, ensure_ascii=False)


if __name__ == '__main__':
    api.run(port=8090, debug=True, host='127.0.0.1')  # 启动服务
    server = pywsgi.WSGIServer(('127.0.0.1', 8090), api)
    server.serve_forever()