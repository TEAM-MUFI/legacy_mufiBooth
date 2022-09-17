from flask import request
from flask_restx import Resource, Api, Namespace

web = Namespace('web')

@web.route('')
class webPost(Resource):
    def post(self):
        return {'hello':'world'}
