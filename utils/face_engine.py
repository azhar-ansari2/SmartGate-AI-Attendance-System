import cv2
import numpy as np
import json
import joblib
import os

from utils.database import get_all_employees

# =========================
# Load PCA + Gender Model
# =========================

MODEL_DIR = "model"

PCA_MODEL = os.path.join(
    MODEL_DIR,
    "pca_model.pkl"
)

CLF_MODEL = os.path.join(
    MODEL_DIR,
    "classifier.pkl"
)

if os.path.exists(PCA_MODEL) and os.path.exists(CLF_MODEL):

    pca = joblib.load(PCA_MODEL)

    clf = joblib.load(CLF_MODEL)

    print("Gender model loaded")

else:

    pca = None
    clf = None

    print("Gender model not found")


# =========================
# Face Detector
# =========================

CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# =========================
# Gender Classification
# =========================

def classify_gender(face_roi):

    if pca is None or clf is None:
        return "Unknown", 0.0

    try:

        gray = cv2.cvtColor(
            face_roi,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.resize(
            gray,
            (64, 64)
        )

        features = gray.flatten()

        features = features.reshape(1, -1)

        features = pca.transform(features)

        pred = clf.predict(features)[0]

        prob = clf.predict_proba(features)[0]

        gender = (
            "Male"
            if pred == 0
            else "Female"
        )

        confidence = round(
            float(max(prob)) * 100,
            2
        )

        return gender, confidence

    except Exception as e:

        print(
            "Gender Classification Error:",
            e
        )

        return "Unknown", 0.0


# =========================
# Face Encoding
# =========================

def encode_face(frame):

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]

    face = gray[y:y+h, x:x+w]

    face = cv2.resize(
        face,
        (64, 64)
    )

    return (
        face
        .flatten()
        .astype(np.float32)
        .tolist()
    )


# =========================
# Face Comparison
# =========================

def compare_faces(
    enc1,
    enc2,
    threshold=0.80
):

    if enc1 is None or enc2 is None:
        return False, 0.0

    try:

        if isinstance(enc1, str):
            enc1 = json.loads(enc1)

        if isinstance(enc2, str):
            enc2 = json.loads(enc2)

        e1 = np.array(
            enc1,
            dtype=np.float32
        )

        e2 = np.array(
            enc2,
            dtype=np.float32
        )

        norm1 = np.linalg.norm(e1)

        norm2 = np.linalg.norm(e2)

        if norm1 == 0 or norm2 == 0:
            return False, 0.0

        similarity = float(
            np.dot(e1, e2)
            /
            (norm1 * norm2)
        )

        score = round(
            similarity * 100,
            2
        )

        return (
            similarity >= threshold,
            score
        )

    except Exception as e:

        print(
            "Compare Error:",
            e
        )

        return False, 0.0


# =========================
# Main Recognition Function
# =========================

def detect_and_recognize(frame):

    result = {

        "face_detected": False,

        "matched": False,

        "employee": None,

        "gender": "Unknown",

        "gender_confidence": 0.0,

        "confidence": 0.0,

        "annotated_frame": frame
    }

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    if len(faces) == 0:
        return result

    result["face_detected"] = True

    x, y, w, h = faces[0]

    face_roi = frame[
        y:y+h,
        x:x+w
    ]

    # Gender Prediction

    gender, gender_conf = classify_gender(
        face_roi
    )

    result["gender"] = gender

    result["gender_confidence"] = gender_conf

    # Face Recognition

    current_encoding = encode_face(
        frame
    )

    employees = get_all_employees()

    best_employee = None

    best_score = 0

    for emp in employees:

        stored_encoding = emp.get(
            "face_encoding"
        )

        if not stored_encoding:
            continue

        matched, score = compare_faces(
            current_encoding,
            stored_encoding,
            threshold=0.80
        )

        if matched and score > best_score:

            best_employee = emp

            best_score = score

    if best_employee:

        result["matched"] = True

        result["employee"] = best_employee

        result["confidence"] = best_score

    return result