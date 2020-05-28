import time
import base64
import socketio

sio = socketio.Client()
start = None


@sio.event
def connect():
    print('connection established')


@sio.event
def message(msg):
    print(f"Elapsed time: {time.time() - start} sec")
    print('message received with ', msg)
    # sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')


# sio.connect('ws://localhost:8000/', socketio_path='/masks/socket.io')
sio.connect('wss://ai.tucanoar.com/', socketio_path='/masks/socket.io')

with open("./data/ym_poor.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    start = time.time()
    sio.send(encoded_string)
    # for i in range(20):
    #     sio.send(encoded_string)
    #     time.sleep(0.3)

time.sleep(6)
sio.disconnect()
