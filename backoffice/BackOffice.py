from flask import request, make_response, render_template, redirect, session
from flask_restx import Resource, Api, Namespace
from webserver import tosspay
from db import MufiData
import json
import os
import shutil
from keyLoad import KeyLoad

boserver = Namespace('back_office')
key = KeyLoad()
boserver.secret_key = key.getSecretKey()

@boserver.route("/")
class home(Resource):
    def get(self):
        return make_response(render_template('OfficeLogin.html'))
        
@boserver.route("/mainPage")
class mainPage(Resource):
    def get(self):
        return redirect("https://www.muinfilm.shop/back_office/")
    def post(self):
        if 'username' not in request.form or 'password' not in request.form:
            return redirect("https://www.muinfilm.shop/back_office/")
            
        if(request.form['username'].find("#") != -1 or request.form['username'].find(";") != -1 or request.form['username'].find("'") != -1 or request.form['username'].find("!") != -1):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'please don\'t try hacking'}, ensure_ascii=False))
            
        if(request.form['password'].find("#") != -1 or request.form['password'].find(";") != -1 or request.form['password'].find("'") != -1 or request.form['password'].find("!") != -1):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'please don\'t try hacking'}, ensure_ascii=False))
            
        md = MufiData()
        res = md.selectdb("select * from branchOffice where officeid = '"+request.form['username']+"' and officepw = '"+request.form['password']+"';")
        
        if(len(res)==0):
            return redirect("http://www.muinfilm.shop/back_office/")
            
        session['officeId'] = request.form['username']
        
        return make_response(render_template('OfficeMain.html'))


@boserver.route("/pictures/upload/<string:orderid>/<string:date>/<int:count>")
class uploadPicture(Resource):
    def get(self, orderid, date, count):
        md = MufiData()
        
        res = md.selectdb("select * from orders as o join picture as p on o.orderid = p.orderid where o.orderid = '%s'"%(orderid))
        
        if(len(res) != 0):
            return redirect("http://www.muinfilm.shop/back_office/mainPage")
            
        date = session['officeId'][:18] + date 
        
        return make_response(render_template('uploadFile.html', orderid = orderid, date = date, count = count))

@boserver.route("/cancelPage")
class cancelPage(Resource):
    def get(self):
        if 'officeId' not in session:
          return make_response(json.dumps({'isSuccess': 'False', 'message' : 'You\'r not manager try again after Login'}, ensure_ascii=False))
          
        return make_response(render_template('Officecancel.html'))

@boserver.route("/cancel/orderid/<string:orderId>/reason/<string:reason>")
class cancel(Resource):
    def put(self, orderId, reason):
        if 'officeId' not in session:
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'You\'r not manager try again after Login'}, ensure_ascii=False))
        
        md = MufiData()

        if(orderId.find("#") != -1 or orderId.find(";") != -1 or orderId.find("'") != -1 or orderId.find("!") != -1):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'please don\'t try hacking'}, ensure_ascii=False))

        if(reason.find("#") != -1 or reason.find(";") != -1 or reason.find("'") != -1 or reason.find("!") != -1):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'please don\'t try hacking'}, ensure_ascii=False))
        
        res = md.selectdb("select paymentkey from pay where orderid = '"+orderId+"';")
        if (len(res) == 0):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'This is an invalid code.'}, ensure_ascii=False))
            
        tp = tosspay.TossPay()
        
        res = tp.cancelOrder(res[0]['paymentkey'], reason)
        res = json.loads(res)
        
        if 'message' in res:
            return res
            
        md.insertdb("update orders set state = 0  where orderid = '"+orderId+"';")

        md.insertdb("""insert into cancelData( paymentkey, lastTransactionKey, method, orderid, approvedAt, reason, officeid) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""%(res['paymentKey'], res['lastTransactionKey'], res['method'], res['orderId'], res['approvedAt'], reason, session['officeId']))
        
        return make_response(json.dumps({'isSuccess': 'True', 'message': 'delete success'}, ensure_ascii=False))

        
@boserver.route("/search/columnname/<string:columnName>/data/<string:data>")
class search(Resource):
    def get(self, columnName, data):
        if 'officeId' not in session:
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'You\'r not manager try again after Login'}, ensure_ascii=False))
            
        if(columnName.find("#") != -1 or columnName.find(";") != -1 or columnName.find("'") != -1 or columnName.find("!") != -1):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'please don\'t try hacking'}, ensure_ascii=False))
            
        if(data.find("#") != -1 or data.find(";") != -1 or data.find("'") != -1 or data.find("!") != -1):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'please don\'t try hacking'}, ensure_ascii=False))
                    
        md = MufiData()
        res = md.selectdb("select o.ordername, o.orderid, o.pinnumber, u.name, o.state, EXISTS (select * from picture where orderid = o.orderid) as success  from orders as o join user as u on o.userid = u.userid where %s"%(columnName) + " like '%"+ data +"%'")
        return make_response(json.dumps(res, ensure_ascii=False))
