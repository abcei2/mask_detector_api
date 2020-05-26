from mask_detector.detections_utils import *
from tensorflow.keras.models import load_model

model = load_model("src/mask_detector/model/mask_detector.model")


def do_detect(img):
    return detect(model, img)
