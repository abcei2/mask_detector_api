import time
import base64
import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def message(msg):
    print('message received with ', msg)
    # sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')


# sio.connect('ws://localhost:8000/', socketio_path='/masks/socket.io')
sio.connect('wss://ai.tucanoar.com/', socketio_path='/masks/socket.io')

with open("./ym_poor.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    for i in range(10):
        sio.send(encoded_string)
        time.sleep(0.04)

time.sleep(1)
sio.disconnect()
