from flask import request, make_response, render_template
from flask_restx import Resource, Api, Namespace
from webserver import kakaoLogin
from webserver import tosspay

server = Namespace('webserver')

@server.route('/oauth')
class signup(Resource):
    def get(self):
        code = str(request.args.get('code'))
        kl = kakaoLogin.KakaoLogin()
        res = kl.getToken(code)

        return make_response(render_template('new-2.html'))

@server.route('/pay/success')
class paysuccess(Resource):
    def get(self):
        paymentkey = str(request.args.get('paymentKey'))
        orderId = str(request.args.get('orderId'))
        amount = str(request.args.get('amount'))
        tp = tosspay.TossPay()
        res = tp.signIn(paymentkey,orderId,amount)
        
