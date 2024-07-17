import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import numpy as np
import cv2
import base64
import pickle as pkl
from scipy.spatial.distance import cosine
from sklearn.preprocessing import Normalizer
from collections import Counter
from qreader import QReader
from .face_capture import capture_face, get_encode
from participant.models import Participant
from django.utils import timezone

# l2_normalizer = Normalizer("l2")

def load_pickle(path):
    with open(path, "rb") as f:
        pklrick = pkl.load(f)
    return pklrick

encoding_dict = load_pickle("./embeddings/encodings_2fn.pkl")
qr_reader = QReader()


def compare_embeddings_cosine(embedding1, embedding2, threshold=0.8):
    similarity = 1 - cosine(embedding1, embedding2)
    return similarity, similarity > (1 - threshold)

def load_mls():
    # model_lists = ["isolationforest copy.pkl", "oneclasssvm copy.pkl", "ellipticenvelope copy.pkl"]
    # models = []
    # for i in range(len(model_lists)):
    #     models.append(load_pickle(os.path.join("./embeddings",model_lists[i])))
    model = load_pickle("./embeddings/isolationforest copy 2.pkl")
    return model

def check_unknown(encode):
    model = load_mls()
    pred = model.predict([encode])[0]
    # results = []
    # for i in l_o_models:
    #     results.append(i.predict([encode])[0])
    # print(results)
    # count = Counter(results)
    # most_common_element = count.most_common(1)[0][0]
    return True if pred == -1 else False

def read_qr(img):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return qr_reader.detect_and_decode(rgb_img)

def verify(encode, threshold):
    highest_similarity = -1
    best_matched = None
    for name, embedding in encoding_dict.items():
        similarity, is_match = compare_embeddings_cosine(encode, embedding[0])
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_matched = name
    if best_matched and highest_similarity > threshold:
        print(best_matched)
        return True
    else:
        return False


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
        success_message = False
        base64_data = img_base64.split(",")[1]
        byte_data = base64.b64decode(base64_data)
        img_np = np.fromstring(byte_data, np.uint8)
        image = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
        is_qr = False
        if not qr:
            face, status = capture_face(image)
            if status == False:
                success_message = False
            else:
                encode = get_encode(face)
                pred = verify(encode, 0.8)
                unknown = check_unknown(encode)
                if pred == False or unknown:
                    success_message = False
                elif pred and not unknown:
                    success_message = True
        else:
            is_qr = True
            qr_code = read_qr(image)
            if qr_code is None:
                success_message = False
            else:
                now = timezone.now()
                p_in_ongoing_events = Participant.objects.filter(event__end_time__gt=now)
                participant_ids = list(p_in_ongoing_events.values_list('id', flat=True))
                if qr_code[0] in participant_ids:
                    success_message = True

        self.send(text_data=json.dumps({"success":success_message, "qr_code":is_qr}))
