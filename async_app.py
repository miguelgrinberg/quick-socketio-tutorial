import socketio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
    '/': './public/'
})


async def task(sid):
    await sio.sleep(5)
    result = await sio.call('mult', {'numbers': [3, 4]}, to=sid)
    print(result)


@sio.event
async def connect(sid, environ):
    print(sid, 'connected')
    sio.start_background_task(task, sid)


@sio.event
async def disconnect(sid):
    print(sid, 'disconnected')


@sio.event
async def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    return {'result': result}
