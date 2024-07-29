import cv2
import numpy as np
from deepface import DeepFace
import pickle as pkl
import os

def capture_face(img):
    try:
        detection = DeepFace.extract_faces(img, detector_backend="retinaface", enforce_detection=False)[0]
        print(detection)
        x, y, w, h = detection['facial_area']['x'], detection['facial_area']['y'], detection['facial_area']['w'], detection['facial_area']['h']
        if w < 100 and h < 100:
            return None, False
        else:
            face = img[y:y+h, x:x+w]
            return face, True
    except IndexError:
        return None, False
    
def get_encode(img):
    try:
        re_img = cv2.resize(img,(160, 160))
        return DeepFace.represent(img_path=re_img, model_name="Facenet", normalization="Facenet2018", enforce_detection=False, detector_backend="retinaface")[0]["embedding"]
    except Exception as e:
        pass

def load_pickle(path):
    with open(path, "rb") as f:
        pklrick = pkl.load(f)
    return pklrick

def save_embeddings(path, is_model, embeddings):
    with open(path, "wb") as f:
        if is_model:
            pkl.dump(embeddings, f)
        else:
            if len(embeddings) > 0:
                pkl.dump(embeddings, f)
            else:
                empty_dict = {}
                pkl.dump(empty_dict, f)
        

def check_modelnembed(path, is_model, embeddings):
    if os.path.exists(path):
        return load_pickle(path)
    else:
        save_embeddings(path, is_model, embeddings)
        return load_pickle(path)