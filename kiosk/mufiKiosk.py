from flask import request, make_response
from flask_restx import Resource, Api, Namespace
from db import MufiData
from aws import MufiS3
from werkzeug.utils import secure_filename
import os
import shutil
import json
import threading

def savePicture(picture, orderid, date, count):
    md = MufiData()
    s3 = MufiS3()
    pid = date+"_"+orderid+"_"+str(count)
    try:
        s3.uploadImage(picture, pid)
        sql ="""insert into photo(pictureid, picturetitle, orderid) values('%s','%s','%s')"""%(pid,count,orderid)
        md.insertdb(sql)
    except:
        return 'Not Save'
        
    return 'success'

kiosk = Namespace('kiosk')

@kiosk.route('/pictures/upload/<string:orderid>/<string:date>/<string:count>/<string:kiosk_id>')
class uploadPicture(Resource):
    def post(self, orderid, date, count, kiosk_id):
        threadList = []
        md = MufiData()
        
        sql ="""select * from photo where orderid = '%s';"""%orderid
        res = md.selectdb(sql)
        

        if(len(res)!=0):
            return make_response(json.dumps({'isSuccess':"이미 사용된번호 입니다."}, ensure_ascii=False))
        
        for i in range(int(count)):
            f = request.files['image'+str(i)]
            t = threading.Thread(target =savePicture, args = (f, orderid, date, i))
            t.start()
            threadList.append(t)
        for t in threadList:
            a = t.join()

        sql = "update orders set enroll_kiosk_id = '%s' where orderid = '%s';"%(kiosk_id, orderid)

        res = md.insertdb(sql)
            
        return make_response(json.dumps({"message": "success Upload"}))

@kiosk.route('/pin/<string:pin>')
class getKiosk(Resource):
    def get(self, pin):
        md = MufiData()
        sql ="""select * from orders where pinnumber = '%s';"""%pin
        res = md.selectdb(sql)

        ordersCount =len(res)
        if(ordersCount==0):
            return make_response(json.dumps({'isSuccess' :  "False"}))

        if(res[0]['state'] == 0):
            return make_response(json.dumps({'isSuccess':"취소된 번호 입니다."}, ensure_ascii=False))

        ordername = res[0]['ordername']
        orderid = res[0]['orderid']
        userid = res[0]['userid']
            

        sql ="""select * from photo where orderid = '%s'"""%orderid
        res = md.selectdb(sql)

        if(len(res)!=0):
            return make_response(json.dumps({'isSuccess':"이미 사용된번호 입니다."}, ensure_ascii=False))

        if(ordersCount==0):
            return make_response(json.dumps({'isSuccess' :"False"}))
        else:
            ordername = ordername[:-1]
            return make_response(json.dumps({'isSuccess' : "True", 'orderName':ordername,'userId':userid,'orderId':orderid}, ensure_ascii=False))
        return make_response(json.dumps({"error":"server error"}))
