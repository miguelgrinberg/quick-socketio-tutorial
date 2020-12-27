import asyncio
import sys
import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connected')
    result = sio.call('sum', {'numbers': [1, 2]})
    print(result)


@sio.event
def connect_error(e):
    print(e)


@sio.event
def disconnect():
    print('disconnected')


@sio.event
def mult(data):
    return data['numbers'][0] * data['numbers'][1]


@sio.event
def client_count(count):
    print('There are', count, 'connected clients.')


@sio.event
def room_count(count):
    print('There are', count, 'clients in my room.')


@sio.event
def user_joined(username):
    print('User', username, 'has joined.')


@sio.event
def user_left(username):
    print('User', username, 'has left.')


def main(username):
    sio.connect('http://localhost:8000',
                headers={'X-Username': username})
    sio.wait()


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
