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
from attendance.face_capture import get_encode, check_modelnembed, load_pickle
from participant.models import Participant
from attendance.models import Attendance
import datetime
from django.core.cache import cache
from attendance.setting_env_variable import set_env_variable
from cryptography.fernet import Fernet
import os

cipher_suite = Fernet(os.getenv("P_HUB_EK"))
qr_reader = QReader()

def get_participants(id):
    cache.delete(f"{id}")
    data = cache.get(f"{id}")
    if data:
        embeddings = data["embeddings"]
        participant_ids = data["participant_ids"]
        participant_id_qr = data["participant_id_qr"]
        return participant_ids, embeddings, participant_id_qr
    else:
        p_in_ongoing_events = Participant.objects.filter(event__id=id, face=True)
        participant_ids = [str(id) for id in list(p_in_ongoing_events.values_list('id', flat=True))]
        participant_id_qr = [str(id) for id in list(Participant.objects.filter(event__id=id).values_list('id', flat=True))]
        embeddings = [json.loads(i) for i in list(p_in_ongoing_events.values_list('facial_feature', flat=True))]
        cache.set(f"{id}", {"participant_ids": participant_ids, "embeddings": embeddings, "participant_id_qr": participant_id_qr},60 * 60 * 60 * 0)
        return participant_ids, embeddings, participant_id_qr

def compare_embeddings_cosine(embedding1, embedding2):
    similarity = 1 - cosine(embedding1, embedding2)
    return similarity

def load_mls():
    # model_lists = ["isolationforest copy.pkl", "oneclasssvm copy.pkl", "ellipticenvelope copy.pkl"]
    # models = []
    # for i in range(len(model_lists)):
    #     models.append(load_pickle(os.path.join("./embeddings",model_lists[i])))
    model = check_modelnembed("embeddings/unknown_classifier_isofor.pkl", True, [])
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

def verify(encode, threshold, embeddings, participant_ids):
    highest_similarity = -1
    best_matched = None
    if len(embeddings) != 0:
        for participant_id, embedding in zip(participant_ids, embeddings):
            similarity = compare_embeddings_cosine(encode, embedding)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_matched = participant_id
            print(participant_id,similarity)
        if best_matched in participant_ids and highest_similarity > threshold:
            return True, best_matched
        else:
            return False, best_matched
    else:
        return False, best_matched

def add_attendance(in_status, participant_id):
    today = datetime.datetime.now()
    attendance = Attendance.objects.get(participant_id=participant_id, date=today.date())
    if in_status == True:
        attendance.entry_1 = today.time()
    else:
        attendance.leave_1 = today.time()
    attendance.save()


class ImageConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"monitor"

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
        is_qr = text_data_json["qr_code"]
        event_id = text_data_json["event_id"]
        in_out_status = text_data_json["in"]

        success_message = False
        base64_data = img_base64.split(",")[1]
        byte_data = base64.b64decode(base64_data)
        img_np = np.fromstring(byte_data, np.uint8)
        image = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
        participant_ids, embeddings, participant_id_qr = get_participants(event_id)

        if not is_qr:
            encode = get_encode(image)
            pred, pred_id = verify(encode, 0.8, embeddings, participant_ids)
            if pred:
                success_message = True
                add_attendance(in_out_status, pred_id)
                self.broadcast_attendance_update(pred_id, in_out_status, event_id)
        else:
            #set_env_variable("ENCRYPTION_KEY", "nDjgKXPfLCRuQ3fvYSg-rJ0kg-tUTPx_GJvHYgsr2Rg=", system=True)
            qr_code = read_qr(image)
            if qr_code is None:
                success_message = False
            else:
                encrypted_id = cipher_suite.decrypt(qr_code[0].encode()).decode()       
                if encrypted_id in participant_id_qr:
                    success_message = True
                    add_attendance(in_out_status, int(encrypted_id))

        self.send(text_data=json.dumps({"success": success_message, "qr_code": is_qr}))

    def broadcast_attendance_update(self, participant_id, status, event_id):
        if not isinstance(status, str):
            status = str(status)
            
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "attendance_update",
                "participant_id": participant_id,
                "status": status,
                "event_id": event_id,
            }
        )

    def attendance_update(self, event):
        print('Sending attendance update:', event)
        self.send(text_data=json.dumps({
            "participant_id": event["participant_id"],
            "status": event["status"],
            "event_id": event["event_id"],
        }))


