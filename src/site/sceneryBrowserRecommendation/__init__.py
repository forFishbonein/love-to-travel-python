# from bottle import route
from flask import Flask, make_response, request
from flask_cors import CORS
from google.protobuf.api_pb2 import Api

import recommmendation as rc
app = Flask(__name__)
# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
# api = Api(app)

# @app.after_request
# def func_res(resp):
#     res = make_response(resp)
#     res.headers['Access-Control-Allow-Origin'] = '*'
#     res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
#     res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#     return res

@app.route('/sce/<scan1>/<scan2>/<scan3>/',methods=["GET","OPTIONS"]) #
def sce(scan1,scan2,scan3):
    # print(scan_str)
    # scan1 = request.args.get('scan1')
    # scan2 = request.args.get('scan2')
    # scan3 = request.args.get('scan3')
    scan_list = [scan1,scan2,scan3]
    print(scan_list)
    # resScenery=rc.getJson(scan_list)
    # print(resScenery)
    # return resScenery

# @app.route('/sd', methods=["GET","OPTIONS"])
# def sce2():
#
#     return "ok"

CORS(app, resources=r'/*')
if __name__ == "__main__":
    app.run('localhost','8086')