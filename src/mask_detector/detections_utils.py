import cv2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

def detect(model,img):

    face = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224, 224))
    face = img_to_array(face)
    face = preprocess_input(face)
    face = np.expand_dims(face, axis=0)
    (mask, withoutMask) = model.predict(face)[0]
    with_mask=False
    print((mask, withoutMask))
    if mask>withoutMask:
        with_mask=True
    elif mask<=withoutMask:
        with_mask=False
    return {"with_mask":with_mask}