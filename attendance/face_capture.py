import cv2
import numpy as np
from deepface import DeepFace

def capture_face(img):
    try:
        detection = DeepFace.extract_faces(img, detector_backend="centerface", enforce_detection=False)[0]
        x, y, w, h = detection['facial_area']['x'], detection['facial_area']['y'], detection['facial_area']['w'], detection['facial_area']['h']
        face = img[y:y+h, x:x+w]
        return face, True
    except IndexError:
        return None, False
    
def get_encode(img):
    re_img = cv2.resize(img,(160, 160))
    return DeepFace.represent(img_path=re_img, model_name="Facenet", normalization="Facenet2018", enforce_detection=False)[0]["embedding"]