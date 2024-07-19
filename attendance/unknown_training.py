import pickle as pkl
from attendance.face_capture import load_pickle, save_embeddings
from participant.models import Participant
from sklearn.ensemble import IsolationForest

def get_participant_count():
    count = Participant.objects.count()
    return count

def get_data():
    encodings = load_pickle("embeddings/attendance_embeddings.pkl")
    embeddings = []
    for label, data in encodings.items():
        embeddings.append(data)

def train_unknown_classifier():
    data = get_data()
    model = IsolationForest(random_state=42, contamination=0.01, max_features=128, max_samples=get_participant_count(), n_estimators=50)
    model.fit(data)
    save_embeddings("embeddings/unknown_classifier_isofor.pkl", model)