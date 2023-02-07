from flask import request, render_template, send_file, make_response, send_from_directory, redirect, url_for
from flask_restx import Resource, Api, Namespace
from werkzeug.serving import WSGIRequestHandler

web = Namespace('web')

WSGIRequestHandler.protoco_version = "HTTP/1.1"



@web.route('/frame/<string:file>')
class webRender(Resource):
    def get(self, file):
        return send_file("./static/img/frame/" + file)


@web.route('/signin') #로그인페이지
class webRender(Resource):
    def get(self):
        return make_response(render_template('signin.html'))


@web.route('/picture/<string:name>')
class picture(Resource):
    def get(self,name):
        return send_file("./picture/"+name)


@web.route('/subphoto/<string:name>')
class subphoto(Resource):
    def get(self,name):
        return send_file("picture/"+name)
