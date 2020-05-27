import os
import cv2
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

model_path = os.path.join(
    os.path.dirname(__file__), 'model', 'mask_detector.model'
)
model = load_model(model_path)


def detect(img):
    face = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224, 224))
    face = img_to_array(face)
    face = preprocess_input(face)
    face = np.expand_dims(face, axis=0)

    mask, withoutMask = model.predict(face)[0]
    return {"with_mask": bool(mask > withoutMask)}
