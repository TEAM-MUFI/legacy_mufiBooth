from flask import request, make_response
from flask_restx import Resource, Api, Namespace
from db import MufiData
from werkzeug.utils import secure_filename
import os
import shutil
import json
import threading

def savePicture(picture, orderid, date, count):
    md = MufiData()
    pid = date+"_"+orderid+"_"+str(count)
    try:
        with open("picture/"+pid+".png", 'wb') as fs:
            shutil.copyfileobj(picture,fs)
        sql ="""insert into picture(pictureid, picturetitle, orderid) values('%s','%s','%s')"""%(pid,count,orderid)
        md.insertdb(sql)
    except:
        return 'Not Save'

kiosk = Namespace('kiosk')

@kiosk.route('')
class test(Resource):
    def get(self):
        return{'hi':'hello'}

@kiosk.route('/pictures/upload/<string:orderid>/<string:date>/<string:count>')
class uploadPicture(Resource):
    def post(self,orderid,date,count):
        threadList = []
        for i in range(int(count)):
            f = request.files['image'+str(i)]
            t = threading.Thread(target =savePicture, args = (f, orderid, date, i))
            t.start()
            threadList.append(t)
        for t in threadList:
            t.join()
        return make_response(json.dumps({"message": "success Upload"}))

@kiosk.route('/pin/<string:pin>')
class getKiosk(Resource):
    def get(self, pin):
        md = MufiData()
        sql ="""select * from orders where pinnumber = '%s';"""%pin
        res = md.selectdb(sql)

        if(res[0]['state'] == 0):
            return make_response(json.dumps({'isSuccess':"취소된 번호 입니다."}, ensure_ascii=False))

        ordersCount =len(res)
        if(ordersCount==0):
            return make_response(json.dumps({'isSuccess' :  "False"}))

        ordername = res[0]['ordername']
        orderid = res[0]['orderid']
        userid = res[0]['userid']
            

        sql ="""select * from picture where orderid = '%s'"""%orderid
        res = md.selectdb(sql)

        if(len(res)!=0):
            return make_response(json.dumps({'isSuccess':"이미 사용된번호 입니다."}, ensure_ascii=False))

        if(ordersCount==0):
            return make_response(json.dumps({'isSuccess' :"False"}))
        else:
            return make_response(json.dumps({'isSuccess' : "True", 'orderName':ordername,'userId':userid,'orderId':orderid}, ensure_ascii=False))
        return make_response(json.dumps({"error":"server error"}))


