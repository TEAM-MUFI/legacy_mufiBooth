from flask import request
from flask_restx import Resource, Api, Namespace

kiosk = Namespace('kiosk')

@kiosk.route('')
class test(Resource):
    def get(self):
        return{'hi':'hello'}

@kiosk.route('/pin/<string:pin>')
class getKiosk(Resource):
    def get(self, pin):
        return {'correct' :  False}
