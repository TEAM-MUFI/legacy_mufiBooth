from flask import request, render_template, send_file, make_response, send_from_directory, redirect, url_for
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

# @web.route('/frame/<string:pin>')
# class webRender(Resource):
    # def get(self, pin):
        # return send_file("./static/img/frame/" + file)
        
@web.route('/signin') #로그인페이지
class webRender(Resource):
    def get(self):
        return make_response(render_template('signin.html'))


@web.route('/id') #사진 촬영/조회 선택 페이지
class webRender(Resource):
    def get(self):
        return make_response(render_template('id.html'))


@web.route('/idrequest', methods=['POST']) #로그인성공후
class webRender(Resource):
    def get(self):
        #ㅁㄴㅇㄹ
        return #

@web.route('/select') #사진 촬영/조회 선택 페이지
class webRender(Resource):
    def get(self):
        return make_response(render_template('select.html'))

@web.route('/pin') #핀 번호 발급 페이지
class webRender(Resource):
    def get(self):
        return make_response(render_template('pin.html'))

@web.route('/photo/<string:token>') #사진 조회 페이지
class webRender(Resource):
    def get(self,token):
        return make_response(render_template('photo.html'))
