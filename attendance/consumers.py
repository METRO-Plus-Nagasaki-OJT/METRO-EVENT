import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import numpy as np
import cv2
import base64
import pickle as pkl
from deepface import DeepFace
from scipy.spatial.distance import cosine
from sklearn.preprocessing import Normalizer
from collections import Counter
import os
from qreader import QReader
from .face_capture import capture_face

l2_normalizer = Normalizer("l2")

def load_pickle(path):
    with open(path, "rb") as f:
        pklrick = pkl.load(f)
    return pklrick

encoding_dict = load_pickle("./embeddings/encodings.pkl")
qr_reader = QReader()

def get_encode(img):
    embed = DeepFace.represent(img_path=img, model_name="Facenet", anti_spoofing=True, enforce_detection=False)[0]["embedding"]
    return l2_normalizer.transform(np.array(embed).reshape(1, -1))[0]


def compare_embeddings_cosine(embedding1, embedding2, threshold=0.8):
    similarity = 1 - cosine(embedding1, embedding2)
    return similarity, similarity > (1 - threshold)

def load_mls():
    # model_lists = ["isolationforest.pkl", "oneclasssvm.pkl", "ellipticenvelope.pkl"]
    # models = []
    # for i in range(len(model_lists)):
    #     print(model_lists[i])
    #     models.append(load_pickle(os.path.join("./embeddings",model_lists[i])))
    model = load_pickle("./embeddings/isolationforest.pkl")
    return model

def check_unknown(encode):
    l_o_models = load_mls()
    result = l_o_models.predict([encode])[0]
    print(result)
    return True if result == -1 else False

def read_qr(img):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return qr_reader.detect_and_decode(rgb_img)

def verify(encode, threshold):
    highest_similarity = -1
    best_matched = None
    for name, embedding in encoding_dict.items():
        similarity, is_match = compare_embeddings_cosine(encode, embedding)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_matched = name
    if best_matched and highest_similarity > threshold:
        print(best_matched)
        return best_matched
    else:
        return None


class ImageConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        img_base64, qr = text_data_json["image_url"], text_data_json["qr_code"]
        success_message = None
        base64_data = img_base64.split(",")[1]
        byte_data = base64.b64decode(base64_data)
        img_np = np.fromstring(byte_data, np.uint8)
        image = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
        is_qr = False
        if not qr:
            face = capture_face(image)
            encode = get_encode(face)
            pred = verify(encode, 0.8)
            unknown = check_unknown(encode)
            if pred == None and unknown:
                success_message = False
            elif pred and not unknown:
                success_message = True
        else:
            is_qr = True
            success_message = True
            qr_code = read_qr(image)[0]
            print(qr_code)
        self.send(text_data=json.dumps({"success":success_message, "qr_code":is_qr}))
