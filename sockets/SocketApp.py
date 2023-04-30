from flask import Blueprint
from flask_socketio import SocketIO, join_room, leave_room, close_room, emit

socketioApp = Blueprint('socketioApp', __name__)
socketio = SocketIO()

# Socket.IO event handlers
@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('join_room')
def on_join_room(data):
    join_room(data)

@socketio.on('leave_room')
def on_leave_room(data):
    leave_room(data)

@socketio.on('close_room')
def on_close_room(data):
    close_room(data)

@socketio.on('disconnect')
def on_disconnect():
    print('client disconnect')

@socketio.on('message')
def on_message(data):
    emit('receive_message', data)

@socketio.on('room_message')
def on_room_message(data):
    room = data['room']
    message = data['message']
    emit('message', {'message': message}, room=room)
