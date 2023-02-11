# 첫 번째 Flask Server
from flask import Flask, render_template, make_response, session
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from kiosk.mufiKiosk import kiosk
from web.mufiWeb import web
from webserver.WebServer import server
from backoffice.BackOffice import boserver
from markupsafe import escape
from datetime import timedelta
from flask_cors import CORS, cross_origin
import sys
from flask import send_file

sys.setrecursionlimit(10**7)

app = Flask(__name__)
app.config['RESTFUL_JSON'] = {'ensure_ascii' : False}
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'mufiHome'

app.config["PERMANENT_SESSION_LIFETIME"]=timedelta(minutes=15)  #세션 시간 15분 설정
cors = CORS(app, resources={ r'/kiosk/*': {'origins': '*'}, r'/back_office/*': {'origins': '*'} }) # /kiosk에 접속 cors 허용

api = Api(app)


api.add_namespace(kiosk,'/kiosk')

api.add_namespace(web,'/web')

api.add_namespace(server,'/webserver')

api.add_namespace(boserver,'/back_office')

@api.route('/main')
class favicon(Resource):
    def get(self):
        return make_response(render_template('signin.html'))


if __name__ =='__main__':
    app.run(debug=False,host='locahost', port=3000, threaded=True)
