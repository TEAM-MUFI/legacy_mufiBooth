from flask import Blueprint
from flask_socketio import SocketIO, join_room, leave_room, close_room, emit
import jwt
from jwt.exceptions import ExpiredSignatureError
import time

from keyLoad import KeyLoad
from db import MufiData

key = KeyLoad()

SECRET_KEY  = key.getSecretKey()

socketioApp = Blueprint('socketioApp', __name__)
socketio = SocketIO()


# Socket.IO event handlers
@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('kiosk_join_room')
def on_join_room(kiosk_id):

    md = MufiData()

    data = md.selectdb("select * from kiosk where id = '%s';" % kiosk_id)

    if(len(data) == 0):
        emit('join_room'+kiosk_id, {'isSuccess' : 'fail', 
                            'reason' : 'invalid'
                            })
    join_room(kiosk_id)

    payload = {
        "kiosk_id" : kiosk_id,
        "exp" : int(time.time())+60
    }
    encodingData = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    emit('join_room'+kiosk_id, {'isSuccess' : 'true', 'jwt': encodingData}, room=data)

@socketio.on('leave_room')
def on_leave_room(data):
    leave_room(data)

@socketio.on('close_room')
def on_close_room(data):
    close_room(data)
    emit('access_close',"success")

@socketio.on('disconnect')
def on_disconnect():
    print('client disconnect')

@socketio.on('message')
def on_message(data):
    emit('receive_message', data+"receive")

@socketio.on('room_message')
def on_room_message(data):
    room = data['room']
    message = data['message']
    emit('test_message', {'message': "receive message : " + message}, room=room)
