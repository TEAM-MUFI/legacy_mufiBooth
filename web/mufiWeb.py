from flask import request, render_template, send_file, make_response, send_from_directory
from flask_restx import Resource, Api, Namespace
from werkzeug.serving import WSGIRequestHandler

web = Namespace('web')

WSGIRequestHandler.protoco_version = "HTTP/1.1"
@web.route('')
class webPost(Resource):
    def post(self):
        return {'hello':'world'}

@web.route('/frame/<string:file>')
class webRender(Resource):
    def get(self, file):
        return send_file("./static/img/frame/" + file)

@web.route('/frame/<string:핀번호>')
class webRender(Resource):
    def get(self, file):
        return send_file("./static/img/frame/" + file)

@web.route('/test1')
class webRender(Resource):
    def get(self):
        return make_response(render_template('new-1.html'))

@web.route('/test2')
class webRender(Resource):
    def get(self):
        return make_response(render_template('new-2.html'))

@web.route('/test3')
class webRender(Resource):
    def get(self):
        return make_response(render_template('new-3.html'))

@web.route('/test4')
class webRender(Resource):
    def get(self):
        return make_response(render_template('new-4.html'))

@web.route('/test5')
class webRender(Resource):
    def get(self):
        return make_response(render_template('new-5.html'))