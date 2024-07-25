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
from attendance.face_capture import capture_face, get_encode, check_modelnembed, load_pickle
from participant.models import Participant
from attendance.models import Attendance
import datetime

qr_reader = QReader()

def get_participants(id):
    p_in_ongoing_events = Participant.objects.filter(event__id=id)
    participant_ids = [str(id) for id in list(p_in_ongoing_events.values_list('id', flat=True))]
    print(participant_ids)
    embeddings = [json.loads(i) for i in list(p_in_ongoing_events.values_list('facial_feature', flat=True))]
    return participant_ids, embeddings

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
    print(pred)
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
        if best_matched in participant_ids and highest_similarity > threshold:
            return True, best_matched
        else:
            return False
    else:
        return False

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
        img_base64, is_qr, event_id, in_out_status = text_data_json["image_url"], text_data_json["qr_code"], text_data_json["event_id"], text_data_json["in"]
        success_message = False
        base64_data = img_base64.split(",")[1]
        byte_data = base64.b64decode(base64_data)
        img_np = np.fromstring(byte_data, np.uint8)
        image = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
        participant_ids, embeddings = get_participants(event_id)
        if not is_qr:
            face, status = capture_face(image)
            if status == False:
                success_message = False
            else:
                encode = get_encode(face)
                pred, pred_id = verify(encode, 0.8, embeddings, participant_ids)
                unknown = check_unknown(encode)
                if pred == False or unknown:
                    success_message = False
                elif pred and not unknown:
                    success_message = True
                    add_attendance(in_out_status, pred_id)
        else:
            is_qr = True
            qr_code = read_qr(image)
            print(qr_code)
            if qr_code is None:
                success_message = False
            else:         
                if qr_code[0] in participant_ids:
                    success_message = True
                    add_attendance(in_out_status, int(qr_code[0]))
        print(success_message)
        self.send(text_data=json.dumps({"success":success_message, "qr_code":is_qr}))
