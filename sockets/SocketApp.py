from flask import Blueprint
from flask_socketio import SocketIO, join_room, leave_room, close_room, emit, rooms
import jwt
from jwt.exceptions import ExpiredSignatureError
import time


from keyLoad import KeyLoad
from db import MufiData

import eventlet

eventlet.monkey_patch()

key = KeyLoad()

SECRET_KEY  = key.getSecretKey()

socketioApp = Blueprint('socketioApp', __name__)
socketio = SocketIO()


# Socket.IO event handlers
@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('kiosk_join_room')
def on_join_room(data):

    kiosk_id = data['kiosk_id']
    sid = data['sid']

    md = MufiData()

    data = md.selectdb("select * from kiosk where id = '%s';" % kiosk_id)

    if(len(data) == 0):
        emit('join_room'+kiosk_id, {'isSuccess' : 'fail',
                                    'reason' : 'invalid'
                                    })
    join_room(kiosk_id)

    payload = {
        "kiosk_id" : kiosk_id,
        "sid" : sid,
        "exp" : int(time.time())+(60*60)
    }
    encodingData = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    emit('join_room'+kiosk_id, {'isSuccess' : 'true', 'jwt': encodingData}, room = kiosk_id)

@socketio.on('leave_room')
def on_leave_room(data):
    leave_room(data)

@socketio.on('close_room')
def on_close_room(data):
    emit('access_close_'+data,"success")
    close_room(data)

@socketio.on('disconnect')
def on_disconnect():
    print('client disconnect')

@socketio.on('user_send_jwt')
def on_room_message(data):
    if( ('jwt' not in data) or ('pin' not in data) or ('user_id' not in data)): 
        emit("user_"+pin+"_state", {'isSuccess':'Fail', "message": "token error"})
        return
    jwt = data['jwt']
    pin = data['pin']
    user_id = data['user_id']
    payload = tokenToJson(jwt)
    if(payload == False):
        emit("user_"+pin+"_state", {'isSuccess':'Fail', "message": "token error"})
        return

    kiosk_id = payload['kiosk_id']
    sid = payload['sid']
    join_room(kiosk_id)

    md = MufiData()
    res = md.selectdb("select orderid, ordername, userid, state from orders where pinnumber = '%s';" % pin)
    ordersCount =len(res)
    if(ordersCount==0):
        emit("user_"+pin+"_state", {'isSuccess':'Fail', "message": "fake pin number"})
        return

    if(res[0]['state'] == 0):
        emit("user_"+pin+"_state", {'isSuccess':'Fail', "message": "this coupon canceled"})
        return

    ordername = res[0]['ordername']
    orderid = res[0]['orderid']
    if(res[0]['userid'] != user_id):
        emit("user_"+pin+"_state", {'isSuccess':'Fail', "message": "uncorrect user"})
        return

    sql ="""select * from photo where orderid = '%s'"""%orderid
    res = md.selectdb(sql)

    if(len(res)!=0):
        emit("user_"+pin+"_state", {'isSuccess':'Fail', "message": "already used"})
        return

    emit("user_"+pin+"_state", {'isSuccess':'Success', "message": "thank you"})
    emit('user_data', {'pin' : pin, 'orderId': orderid, 'orderName': ordername, 'userId': user_id}, room=sid)

    leave_room(kiosk_id)

def tokenToJson(token):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
  except:
    return False
  return False
