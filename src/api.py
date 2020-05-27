import os
import cv2
import json
import base64

import numpy as np

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename

from mask_detector import detect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_786acdaf'
socketio = SocketIO(app)

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_busy():

    with open('src/database.json', 'r') as json_file:
        data = json.load(json_file)
    if(data['flag_occupied'] == "BUSY"):
        return True
    else:
        with open('src/database.json', 'w') as json_file:
            data['flag_occupied'] = "BUSY"
            json.dump(data, json_file)
        return False


def not_busy():
    with open('src/database.json', 'r') as json_file:
        data = json.load(json_file)

    with open('src/database.json', 'w') as json_file:
        data['flag_occupied'] = "NOT BUSY"
        json.dump(data, json_file)

    print("NOT BUSY")


global bussy
bussy = False


@app.route('/detect/', methods=['POST'])
def upload_file():
    global bussy
    if bussy:
        resp = jsonify({'message': 'Service is being used'})
        resp.status_code = 503
        return resp
    bussy = True

    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        bussy = False
        return resp

    file_1 = request.files['file']

    if file_1.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        bussy = False
        return resp

    if file_1 and allowed_file(file_1.filename):
        filename = secure_filename(file_1.filename)

        file_1.save(os.path.join("./", filename))
        img = cv2.imread(f"./{filename}")

        detections = detect(img)
        print(detections)
        resp = jsonify({'message': detections})
        resp.status_code = 200
        bussy = False
        return resp

    else:
        resp = jsonify({
            'message': f"Allowed file types are {','.join(ALLOWED_EXTENSIONS)}"
        })
        resp.status_code = 400
        bussy = False
        return resp


def frame_from_b64image(b64image):
    nparr = np.frombuffer(base64.b64decode(b64image), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)


@socketio.on('message')
def handle_message(b64image):
    frame = frame_from_b64image(b64image)
    detections = detect(frame)
    send(detections)


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    socketio.run(app, host='0.0.0.0')
    print("Ready for action...")
