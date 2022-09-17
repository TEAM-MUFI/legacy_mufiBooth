# 첫 번째 Flask Server
from flask import Flask  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from test import test
from kiosk.mufiKiosk import kiosk

app = Flask(__name__)
api = Api(app)  # Flask 객체에 Api 객체 등록


api.add_namespace(test,'/test')

api.add_namespace(kiosk,'/kiosk')

#api.add_namespace(,'/page')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
