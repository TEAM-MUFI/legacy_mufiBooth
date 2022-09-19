from flask import request, make_response, render_template,session,redirect, escape
from flask_restx import Resource, Api, Namespace
from webserver import kakaoLogin
from webserver import tosspay
from db import MufiData
from datetime import timedelta
import time
from datetime import datetime
import json

server = Namespace('webserver')
server.secret_key = 'mufiHome'

@server.route('/oauth/<string:token>/<string:name>/<string:age>/<string:gender>')
class signup(Resource):
    def get(self,token,name,age,gender):
        md = MufiData()
        userid =""
        data = md.selectdb("select * from user where token = '"+ token +"';")
        for i in data:
            userid = i['userid']
            session['id'] = i['userid']
            session['name'] = i['name']
            return redirect("http://54.191.229.56:5000/webserver/menu") 
        userid = datetime.now().strftime('%Y%m%d%H%M%S')
        userid += "MF"+str(int((time.time()%1)*1000))
        age = 20
        if(gender == 'male'):
            gender = 0
        else:
            gender = 1
        try:
            sql ="""insert into user(token, name, age, gender, userid) values('%s', '%s', %d, %d, '%s')"""%(token, name, age, gender, userid)
        except:
            return "error"
        md.insertdb(sql)
        session['id'] = userid
        session['name'] = name
        return redirect("http://54.191.229.56:5000/webserver/menu")

@server.route('/menu')
class menu(Resource):
    def get(self):
        if 'id' in session:
            return make_response(render_template('menu.html'))
        else:
            return redirect("http://54.191.229.56:5000/web/signin")

@server.route('/payment/success')
class paySuccess(Resource):
    def get(self):
        if 'id' not in session:
            return redirect("http://54.191.229.56:5000/web/signin")
        paykey = request.args.get("paymentKey")
        orderId = request.args.get("orderId")
        amount = request.args.get("amount")
        tp =tosspay.TossPay()
        res = tp.signIn(paykey, amount, orderId)

        res = json.loads(res)

        if "paymentKey" in res:
            session['orderName'] = res['orderName']
            return redirect("http://54.191.229.56:5000/webserver/success")
        else:
            return redirect("http://54.191.229.56:5000/webserver/fail")
        return "0"
@server.route('/success')
class paySuccess(Resource):
    def get(self):
        if 'orderName' not in session:
            return redirect("http://54.191.229.56:5000/web/signin")
        else:
            return make_response(render_template('success.html'))

@server.route('/fail')
class payFail(Resource):
    def get(self):
        return make_response(render_template('success.html'))

