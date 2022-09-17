from flask import request
from flask_restx import Resource, Api, Namespace

kisok = Namespace('kiosk')

kiosk.route('pin/<string:pin>')
class getKiosk(Resource):
    def get(self, pin):
        return {'correct' :  False}
