# coding=UTF-8
import traceback
import flask, json
from gevent import pywsgi
from flask import request, Flask, render_template, send_from_directory, make_response

from elife_api_interface.auto_test_api.gmail import Gmail
from elife_public_method.module_encapsulation.parameter_method import returndata

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


@api.route('/auto/gmail', methods=['post'])  # 创建测试套
def gmailroute():
    keylist = ["gmailType"]
    msginfo = tokenpublic(keylist)
    try:
        ret = Gmail().selectGmail(msginfo["gmailType"])
        ret = returndata(1, ret)
    except:
        ret = returndata(2, "")  # 打印报错信息
    return json.dumps(ret, ensure_ascii=False)


if __name__ == '__main__':
    api.run(port=8989, debug=True, host='18.222.127.214')  # 启动服务
    server = pywsgi.WSGIServer(('18.222.127.214', 8989), api)
    server.serve_forever()