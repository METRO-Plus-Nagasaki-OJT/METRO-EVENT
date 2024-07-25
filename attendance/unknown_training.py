import pickle as pkl
from attendance.face_capture import load_pickle, save_embeddings, check_modelnembed
from participant.models import Participant
from sklearn.ensemble import IsolationForest
import json

def get_participant_count():
    count = Participant.objects.count()
    return count

def get_data():
    encodings = Participant.objects.values_list("facial_feature",flat=True)
    embeddings = [json.loads(i) for i in list(encodings)]
    print(embeddings)
    return embeddings

def train_unknown_classifier():
    data = get_data()
    model = IsolationForest(random_state=42, contamination=0.01, max_features=128, max_samples=get_participant_count(), n_estimators=150)
    model.fit(data)
    save_embeddings("embeddings/unknown_classifier_isofor.pkl", True, model)