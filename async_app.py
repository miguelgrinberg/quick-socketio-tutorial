import random
import socketio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
    '/': './public/'
})
client_count = 0
a_count = 0
b_count = 0


async def task(sid):
    await sio.sleep(5)
    result = await sio.call('mult', {'numbers': [3, 4]}, to=sid)
    print(result)


@sio.event
async def connect(sid, environ):
    global client_count
    global a_count
    global b_count

    username = environ.get('HTTP_X_USERNAME')
    print('username:', username)
    if not username:
        return False

    async with sio.session(sid) as session:
        session['username'] = username
    await sio.emit('user_joined', username)

    client_count += 1
    print(sid, 'connected')
    sio.start_background_task(task, sid)
    await sio.emit('client_count', client_count)
    if random.random() > 0.5:
        sio.enter_room(sid, 'a')
        a_count += 1
        await sio.emit('room_count', a_count, to='a')
    else:
        sio.enter_room(sid, 'b')
        b_count += 1
        await sio.emit('room_count', b_count, to='b')


@sio.event
async def disconnect(sid):
    global client_count
    global a_count
    global b_count
    client_count -= 1
    print(sid, 'disconnected')
    await sio.emit('client_count', client_count)
    if 'a' in sio.rooms(sid):
        a_count -= 1
        await sio.emit('room_count', a_count, to='a')
    else:
        b_count -= 1
        await sio.emit('room_count', b_count, to='b')

    async with sio.session(sid) as session:
        await sio.emit('user_left', session['username'])


@sio.event
async def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    return {'result': result}
