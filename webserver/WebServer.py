from flask import request, make_response, render_template,session,redirect, escape
from flask_restx import Resource, Api, Namespace
from webserver import kakaoLogin
from webserver import tosspay
from db import MufiData
from datetime import timedelta
import time
from datetime import datetime
import json
import random

server = Namespace('webserver')
server.secret_key = 'mufiHome'

@server.route('/oauth/<string:token>/<string:name>/<string:age>/<string:gender>/<string:messageid>')
class signup(Resource):
    def get(self,token,name,age,gender,messageid):
        md = MufiData()
        userid =""
        data = md.selectdb("select * from user where token = '"+ token +"';")
        for i in data:
            userid = i['userid']
            session['id'] = i['userid']
            session['name'] = i['name']
            return redirect("http://www.muinfilm.shop/webserver/select") 
        userid = datetime.now().strftime('%Y%m%d%H%M%S')
        userid += "MF"+str(int((time.time()%1)*1000))
        age = 20
        if(gender == 'male'):
            gender = 0
        else:
            gender = 1
        try:
            sql ="""insert into user(token, name, age, gender, userid,messageid) values('%s', '%s', %d, %d, '%s','%s')"""%(token, name, age, gender, userid,messageid)
        except:
            return "error"
        md.insertdb(sql)
        session['id'] = userid
        session['name'] = name
        return redirect("http://www.muinfilm.shop/webserver/select")

@server.route('/select')
class menu(Resource):
    def get(self):
        if 'id' in session:
            return make_response(render_template('select.html'))
        else:
            return redirect("http://www.muinfilm.shop/web/signin")


@server.route('/menu')
class menu(Resource):
    def get(self):
        if 'id' in session:
            if 'name' in session:
                return make_response(render_template('menu.html',name=session['name']))
            return redirect("http://www.muinfilm.shop/web/signin")
        else:
            return redirect("http://www.muinfilm.shop/web/signin")

@server.route('/subphoto/<string:orderid>')
class photo(Resource):
    def get(self,orderid):
        if 'id' in session:
            orderidlist = []
            pictureid = []
            md = MufiData()
            sql = """select * from picture where orderid ='%s'"""%orderid
            res = md.selectdb(sql)
            for j in res:
                orderidlist.append(orderid)
                pictureid.append(j['pictureid'])
            pictureid.sort()
            return make_response(render_template('photo.html',photo=pictureid, order = orderidlist, subcheck=0, count=len(pictureid)))
        else:
            return redirect("http://www.muinfilm.shop/web/signin")

@server.route('/photo/main')
class photo(Resource):
    def get(self):
        if 'id' in session:
            orderid = []
            orderidlist = []
            pictureid=[]
            md = MufiData()
            sql ="""select * from orders where userid ='%s'"""%session['id']
            res = md.selectdb(sql)
            for i in res:
                orderid.append(i['orderid'])
            for i in orderid:
                sql ="""select * from picture where orderid ='%s' and picturetitle = '0'"""%i
                res = md.selectdb(sql)
                for j in res:
                    orderidlist.append(j['orderid'])
                    pictureid.append(j['pictureid'])
            return make_response(render_template('photo.html', photo = pictureid, order = orderidlist, subcheck=1,count =len(pictureid) ))
        else:
            return redirect("http://www.muinfilm.shop/web/signin")
        return {"message":"errorMessage"}

@server.route('/payment/fail')
class payFail(Resource):
    def get(self):
        return make_response(render_template('fail.html'))


@server.route('/payment/success')
class paySuccess(Resource):
    def get(self):
        if 'id' not in session:
            return redirect("http://www.muinfilm.shop/web/signin")
        paykey = request.args.get("paymentKey")
        orderId = request.args.get("orderId")
        amount = request.args.get("amount")
        tp =tosspay.TossPay()
        md = MufiData()
        res = tp.signIn(paykey, amount, orderId)
        res = json.loads(res)

        if 'orderName' not in res:
            return redirect("http://www.muinfilm.shop/webserver/fail")

        pw = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw += "0123456789"
        pin=""

        while(1):
            random.seed(time.time())
            pin = "".join(random.sample(pw, 5))
            sql = """select * from orders where pinnumber='%s'"""%pin
            tmpres = md.selectdb(sql)
            if(len(tmpres)==0):
                break

        sql = """insert into orders(orderid, ordername, pinnumber, userid) values('%s', '%s', '%s', '%s')"""%(orderId,res['orderName'],pin,session['id'])
        md.insertdb(sql)

        if "paymentKey" in res:
            sql ="""insert into pay(paymentkey, kind, userid, orderid, price) values('%s', '%s', '%s', '%s', %d)"""%(paykey,"toss",session['id'],orderId,int(amount))
            md.insertdb(sql)
            session['orderName'] = res['orderName']
            return redirect("http://www.muinfilm.shop/webserver/success/"+pin)
        else:
            return redirect("http://www.muinfilm.shop/webserver/fail")
        return "0"

@server.route('/success/<string:pin>')
class paySuccess(Resource):
    def get(self,pin):
        if 'orderName' not in session:
            return redirect("http://www.muinfilm.shop/web/signin")
        else:
            p1 = str(pin[0])
            p2 = str(pin[1])
            p3 = str(pin[2])
            p4 = str(pin[3])
            p5 = str(pin[4])
            return make_response(render_template('success.html',pn=pin,pin1=p1,pin2=p2,pin3=p3,pin4=p4,pin5=p5))

@server.route('/fail')
class payFail(Resource):
    def get(self):
        return make_response(render_template('fail.html'))

@server.route('/id')
class admin(Resource):
    def get(self):
        return make_response(render_template('id.html'))

@server.route('/id/server')
class admin(Resource):
    def get(self):
        id = request.args.get("id")
        pw = request.args.get("token")
        md = MufiData()
        sql = """select * from user where userid='%s' and token='%s'"""%(id,pw)
        res = md.selectdb(sql)

        if(len(res)==0):
            return redirect("http://www.muinfilm.shop/webserver/id")
        else:
            session['id'] = id
            session['name'] = "tester"
            return redirect("http://www.muinfilm.shop/webserver/menu")

