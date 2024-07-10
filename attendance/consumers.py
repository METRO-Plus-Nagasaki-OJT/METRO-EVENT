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

l2_normalizer = Normalizer("l2")


def get_embeddings_dict():
    with open("./embeddings/encodings.pkl", "rb") as f:
        encoding_dict = pkl.load(f)
    return encoding_dict


encoding_dict = get_embeddings_dict()


def get_encode(img):
    return DeepFace.represent(img_path=img, model_name="Facenet")[0]["embedding"]


def compare_embeddings_cosine(embedding1, embedding2, threshold=0.8):
    similarity = 1 - cosine(embedding1, embedding2)
    return similarity, similarity > (1 - threshold)


def verify(encode):
    encode = l2_normalizer.transform(np.array(encode).reshape(1, -1))[0]
    highest_similarity = -1
    best_matched = None
    for name, embedding in encoding_dict.items():
        similarity, is_match = compare_embeddings_cosine(encode, embedding)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_matched = name
    if best_matched:
        print(best_matched)


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
        image = get_encode(image)
        pred = verify(image)
        self.send(text_data=json.dumps({"image_url": True}))
