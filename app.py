import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})


@sio.event
def connect(sid, environ):
    print(sid, 'connected')


@sio.event
def disconnect(sid):
    print(sid, 'disconnected')


@sio.event
def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    sio.emit('sum_result', {'result': result}, to=sid)
