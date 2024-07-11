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

l2_normalizer = Normalizer("l2")

def load_pickle(path):
    with open(path, "rb") as f:
        pklrick = pkl.load(f)
    return pklrick

encoding_dict = load_pickle("./embeddings/encodings.pkl")

def get_encode(img):
    return DeepFace.represent(img_path=img, model_name="Facenet")[0]["embedding"]

def compare_embeddings_cosine(embedding1, embedding2, threshold=0.8):
    similarity = 1 - cosine(embedding1, embedding2)
    return similarity, similarity > (1 - threshold)

def load_mls():
    model_lists = ["isolationforest", "oneclasssvm", "ellipticenvelope"]
    for i in range(len(model_lists)):
        model_lists[i] = load_pickle(model_lists[i])
    return model_lists

def check_unknown(encode):
    l_o_models = load_mls()
    preds = []
    for i in l_o_models:
        preds.append(i.predict(encode))
    counts =  Counter(preds)
    result = counts.most_common(1)[0][0]
    return True if result == -1 else False

def verify(encode, threshold):
    encode = l2_normalizer.transform(np.array(encode).reshape(1, -1))[0]
    highest_similarity = -1
    best_matched = None
    for name, embedding in encoding_dict.items():
        similarity, is_match = compare_embeddings_cosine(encode, embedding)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_matched = name
    if best_matched and highest_similarity > threshold:
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
        img_base64 = text_data_json["image_url"]
        base64_data = img_base64.split(",")[1]
        byte_data = base64.b64decode(base64_data)
        img_np = np.fromstring(byte_data, np.uint8)
        image = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
        encode = get_encode(image)
        pred = verify(encode, 0.8)
        unknown = check_unknown(encode)
        success_message = None
        if pred == None and unknown:
            success_message = False
        elif pred and not unknown:
            success_message = True
        self.send(text_data=json.dumps({"success":success_message}))