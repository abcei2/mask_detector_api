import os
import cv2

import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

mask_model_path = os.path.join(
    os.path.dirname(__file__), 'model', 'mask_detector.model'
)
mask_model = load_model(mask_model_path)

prototxtPath = os.path.join(
    os.path.dirname(__file__), 'model_faces_detector', 'deploy.prototxt'
)
weightsPath = os.path.join(
    os.path.dirname(__file__), 'model_faces_detector', 'res10_300x300_ssd_iter_140000.caffemodel'
)
net = cv2.dnn.readNet(prototxtPath, weightsPath)

def extract_face(img):

    (h, w) = img.shape[:2]
    # construct a blob from the image
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    print("[INFO] computing face detections...")
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    if detections.shape[2]>0:
        # the detection
        confidence = detections[0, 0, 0, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            face_bbox={
                'upper_left':[int(startX), int(startY)],
                'down_right':[int(endX), int(endY)]
            }
            
            face_image= img[startY:endY, startX:endX]

            return (face_image, face_bbox)
        else:
            return (None,None)
    else:
        return (None,None)

def detect_faces(img):
    face, box = extract_face(img)

    if face is not None:
        detections={
            "image_width":img.shape[1],
            "image_height":img.shape[0],
            "num_of_detections":len(box),
            "faces_detected":box
        }
        return detections
    else:

        detections={
            "image_width":img.shape[1],
            "image_height":img.shape[0],
            "num_of_detections":0,
            "faces_detected":None
        }
        return detections
        
def detect(img):
    face, box = extract_face(img)

    if face is not None:
        face = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (224, 224))
        face = img_to_array(face)
        face = preprocess_input(face)
        face = np.expand_dims(face, axis=0)

        mask, withoutMask = mask_model.predict(face)[0]
        if mask>withoutMask and mask>0.9:
            return {'with_mask': True, 'box': box}
        else:
            return {'with_mask': False, 'box': box}
    else:
        return {'with_mask': None, 'box': None}
