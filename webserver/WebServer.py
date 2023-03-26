from flask import request, make_response, render_template,session,redirect, escape
from flask_restx import Resource, Api, Namespace
from webserver import kakaoLogin
from webserver import tosspay
from db import MufiData
from datetime import timedelta, datetime
import time
import json
import random
from keyLoad import KeyLoad
import re


server = Namespace('webserver')
key = KeyLoad()
server.secret_key = key.getSecretKey()


@server.route('/oauth/<string:token>/<string:name>/<string:age>/<string:gender>/<string:messageid>/<string:accessToken>/<string:refreshToken>')
class signup(Resource):
    def get(self,token,name,age,gender,messageid, accessToken, refreshToken):
        md = MufiData()
        
        kakao = kakaoLogin.KakaoLogin()
        res = kakao.getToken(accessToken)
        res = json.loads(res)
        
        if 'id' not in res:
            if res['code'] == -401:
                accessToken = kakao.getRefreshToken(refreshToken)
                res = kakao.getToken(accessToken)
            else:
                return res
                
        if (str(res['id']) != token):
            return res
        
        userid =""
        data = md.selectdb("select * from user where token = '"+ token +"';")
        for i in data:
            userid = i['userid']
            session['id'] = i['userid']
            session['name'] = i['name']
            return redirect("https://www.muinfilm.shop/webserver/select")
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
        session['token'] = str(res['id'])
        session['name'] = name
        return redirect("https://www.muinfilm.shop/webserver/select")


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
            sql = """select * from photo where orderid ='%s'"""%orderid
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
            sql ="""select * from orders where state = 1 and userid ='%s'"""%session['id']
            res = md.selectdb(sql)
            for i in res:
                orderid.append(i['orderid'])
            for i in orderid:
                sql ="""select * from photo where orderid ='%s' and picturetitle = '0'"""%i
                res = md.selectdb(sql)
                for j in res:
                    orderidlist.append(j['orderid'])
                    pictureid.append(j['pictureid'])
            return make_response(render_template('photo.html', photo = pictureid, order = orderidlist, subcheck=1,count =len(pictureid) ))
        else:
            return redirect("http://www.muinfilm.shop/main")
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
        tp = tosspay.TossPay()
        md = MufiData()

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
        
        res = tp.signIn(paykey, amount, orderId)
        res = json.loads(res)

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
            #카카오톡 메세지 전송코드 준비중 
            #kakao = kakaoLogin.KakaoLogin()
            #res = kakao.sendMessagePin(session['token'], pin)
            p1 = str(pin[0])
            p2 = str(pin[1])
            p3 = str(pin[2])
            p4 = str(pin[3])
            p5 = str(pin[4])
            return make_response(render_template('success.html',pin=pin,pin1=p1,pin2=p2,pin3=p3,pin4=p4,pin5=p5))


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

@server.route('/coupon/registration/<string:code>')
class CouponList(Resource):
    def post(self, code):
        pattern = re.compile('[^a-zA-Z0-9&/]+')
        
        if pattern.search(code):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'please don\'t try hacking'}, ensure_ascii=False))
        
        if 'id' not in session:
            return redirect("http://www.muinfilm.shop/main")
        
        md = MufiData()
        sql = """select * from coupon where id = '%s'"""%(code)
        res = md.selectdb(sql)
        
        if(len(res)==0):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'worng code'}, ensure_ascii=False))
        
        if(res[0]['used'] == True):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'used code'}, ensure_ascii=False))
        
        count = request.form['count']
        bName = request.form['b_name']
        orderName = res[0]['name']
        
        if( int(count) != res[0]['count'] or bName != res[0]['business_name']):
            return make_response(json.dumps({'isSuccess': 'False', 'message' : 'uncorrect'}, ensure_ascii=False))
        
        d = datetime.now()
        day =  "%04d%02d%02d" % (d.year, d.month, d.day)
        dTime = "%02d%02d%02d%d" % (d.hour, d.minute, d.second, d.microsecond)
        dTime = dTime[:8]
        
        orderId = day + bName + dTime
        
        
        pw = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw += "0123456789"
        
        while(1):
            random.seed(time.time())
            pin = "".join(random.sample(pw, 5))
            sql = """select * from orders where pinnumber='%s'"""%pin
            tmpres = md.selectdb(sql)
            if(len(tmpres)==0):
                break
                
        sql = """insert into orders(orderid, ordername, pinnumber, userid) values('%s', '%s', '%s', '%s')"""%(orderId,orderName,pin,session['id'])
        md.insertdb(sql)
        
        sql = """update coupon set used = true where id = '%s'"""%(code)
        md.insertdb(sql)
        
        session['orderName'] = orderName
        
        return make_response(json.dumps({'isSuccess': 'True', 'message': 'coupon registration success', 'pin_number' : pin}, ensure_ascii=False))
        

@server.route('/coupon/list')
class CouponList(Resource):
    def get(self):
        if 'id' not in session:
            return redirect("http://www.muinfilm.shop/main")
        sql = """
select o.orderid, o.ordername, o.pinnumber, if (p.pictureid is NULL, 1, pictureid) as used from orders as o left join photo as p on o.orderid=p.orderid where o.userid = '%s' and o.state = 1"""%session['id'] + """ group by o.orderid, o.ordername, o.pinnumber, p.pictureid having p.pictureid like '%\\_0' or p.pictureid is NULL;"""

        md = MufiData()
        res = md.selectdb(sql)

        return make_response(render_template('buyList.html', orderList = res))
