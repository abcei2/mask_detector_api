import os
import cv2
import insightface

import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

mask_model_path = os.path.join(
    os.path.dirname(__file__), 'model', 'mask_detector.model'
)
mask_model = load_model(mask_model_path)

insight_model = insightface.model_zoo.get_model('retinaface_r50_v1')
insight_model.prepare(ctx_id=-1, nms=0.4)


def extract_face(img):
    bboxs, landmarks = insight_model.detect(img, threshold=0.5, scale=1.0)

    faces = [
        {
            "upper_left": [int(bbox[0]), int(bbox[1])],
            "down_right": [int(bbox[2]), int(bbox[3])],
            "landmarks": [
                [int(coord[0]), int(coord[1])] for coord in landmark
            ]
        } for bbox, landmark in zip(bboxs, landmarks) if bboxs is not None
    ]

    face = faces[0] if len(faces) > 0 else None

    return (img[
        face['upper_left'][1]:face['down_right'][1],
        face['upper_left'][0]:face['down_right'][0]
    ], face) if face else (None, None)


def detect(img):
    face, box = extract_face(img)
    face = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224, 224))
    face = img_to_array(face)
    face = preprocess_input(face)
    face = np.expand_dims(face, axis=0)

    mask, withoutMask = mask_model.predict(face)[0]
    return {'with_mask': bool(mask > withoutMask), 'box': box}
