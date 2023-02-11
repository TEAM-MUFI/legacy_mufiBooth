from flask import request, make_response
from flask_restx import Resource, Api, Namespace
from webserver import tosspay
from db import MufiData
import json
import os
import shutil

boserver = Namespace('back_office')

@boserver.route("/cancel/orderid/<string:orderId>/reason/<string:reason>")
class cancel(Resource):
    def get(self, orderId, reason):
        md = MufiData()
        tp = tosspay.TossPay()
        
        res = md.selectdb("select paymentkey from pay where orderid = '"+orderId+"';")
        if (len(res) == 0):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'This is an invalid code.'}, ensure_ascii=False))
        
        res = tp.cancelOrder(res[0]['paymentkey'], reason)
        res = json.loads(res)
        
        if 'message' in res:
            return res
            
        md.insertdb("update orders set state = 0  where orderid = '"+orderId+"';")

        md.insertdb("""insert into cancelData( paymentkey, lastTransactionKey, method, orderid, approvedAt) values('%s', '%s', '%s', '%s', '%s')"""%(res['paymentKey'], res['lastTransactionKey'], res['method'], res['orderId'], res['approvedAt'] ))
        
        return make_response(json.dumps({'isSuccess': 'True', 'message': 'delete success'}, ensure_ascii=False))

        
@boserver.route("/")
class home(Resource):
    def get(self):
        return "Hello"
