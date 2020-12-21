import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})


def task(sid):
    sio.sleep(5)
    result = sio.call('mult', {'numbers': [3, 4]}, to=sid)
    print(result)


@sio.event
def connect(sid, environ):
    print(sid, 'connected')
    sio.start_background_task(task, sid)


@sio.event
def disconnect(sid):
    print(sid, 'disconnected')


@sio.event
def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    return {'result': result}
