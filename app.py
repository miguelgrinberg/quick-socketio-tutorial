import random
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})
client_count = 0
a_count = 0
b_count = 0


def task(sid):
    sio.sleep(5)
    result = sio.call('mult', {'numbers': [3, 4]}, to=sid)
    print(result)


@sio.event
def connect(sid, environ):
    global client_count
    global a_count
    global b_count

    username = environ.get('HTTP_X_USERNAME')
    print('username:', username)
    if not username:
        return False

    with sio.session(sid) as session:
        session['username'] = username
    sio.emit('user_joined', username)

    client_count += 1
    print(sid, 'connected')
    sio.start_background_task(task, sid)
    sio.emit('client_count', client_count)
    if random.random() > 0.5:
        sio.enter_room(sid, 'a')
        a_count += 1
        sio.emit('room_count', a_count, to='a')
    else:
        sio.enter_room(sid, 'b')
        b_count += 1
        sio.emit('room_count', b_count, to='b')


@sio.event
def disconnect(sid):
    global client_count
    global a_count
    global b_count
    client_count -= 1
    print(sid, 'disconnected')
    sio.emit('client_count', client_count)
    if 'a' in sio.rooms(sid):
        a_count -= 1
        sio.emit('room_count', a_count, to='a')
    else:
        b_count -= 1
        sio.emit('room_count', b_count, to='b')

    with sio.session(sid) as session:
        sio.emit('user_left', session['username'])


@sio.event
def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    return {'result': result}
