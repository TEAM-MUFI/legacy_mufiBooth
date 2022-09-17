from flask import request
from flask_restx import Resource, Api, Namespace

test = Namespace('Test')

@test.route('')
class getTest(Resource):
    def get(self):
        return "hi"
