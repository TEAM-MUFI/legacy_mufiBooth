# 첫 번째 Flask Server
from flask import Flask, render_template, make_response, session
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from kiosk.mufiKiosk import kiosk
from web.mufiWeb import web
from webserver.WebServer import server
from backoffice.BackOffice import boserver
from sockets.SocketApp import socketioApp, socketio
from markupsafe import escape
from datetime import timedelta
from flask_cors import CORS, cross_origin
import sys
from flask import send_file
from keyLoad import KeyLoad

sys.setrecursionlimit(10**7)

app = Flask(__name__)
app.config['RESTFUL_JSON'] = {'ensure_ascii' : False}
app.config['JSON_AS_ASCII'] = False

key = KeyLoad()
app.secret_key = key.getSecretKey()


app.config["PERMANENT_SESSION_LIFETIME"]=timedelta(minutes=20)  #세션 시간 10분 설정

CORS(app)

app.register_blueprint(socketioApp, url_prefix='/socketio')
socketio.init_app(app, async_mode="eventlet", cors_allowed_origins="*",
                        logger=True, engineio_logger=True)

@app.errorhandler(404)
def page_not_found(error):
    return "Error", 404

@app.route('/')
def test():
    return make_response(render_template('signin.html'))

@app.route('/main')
def home():
    return make_response(render_template('signin.html'))

api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs", terms_url="/api-docs")

api.add_namespace(kiosk,'/kiosk')

api.add_namespace(web,'/web')

api.add_namespace(server,'/webserver')

api.add_namespace(boserver,'/back_office')


if __name__ =='__main__':
    app.run(debug=False,host='locahost', port=3000, threaded=True)
