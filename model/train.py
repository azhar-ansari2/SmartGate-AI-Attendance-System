import os
import cv2
import joblib
import numpy as np

from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATASET_PATH = "UTKFace"

X = []
y = []

print("Loading dataset...")

files = [f for f in os.listdir(DATASET_PATH) if f.endswith(".jpg")]

# First test with 5000 images
files = files[:6000]

for file in files:

    try:
        gender = int(file.split("_")[1])

        path = os.path.join(DATASET_PATH, file)

        img = cv2.imread(path)

        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray = cv2.resize(gray, (64, 64))

        X.append(gray.flatten())

        y.append(gender)

    except:
        continue

X = np.array(X)
y = np.array(y)

print("Images Loaded:", len(X))

print("Applying PCA...")

pca = PCA(n_components=150)

X_pca = pca.fit_transform(X)

print("Training Logistic Regression...")

X_train, X_test, y_train, y_test = train_test_split(
    X_pca,
    y,
    test_size=0.2,
    random_state=42
)

clf = LogisticRegression(
    max_iter=2000
)

clf.fit(X_train, y_train)

pred = clf.predict(X_test)

acc = accuracy_score(y_test, pred)

print(f"Accuracy: {acc*100:.2f}%")

os.makedirs("model", exist_ok=True)

joblib.dump(
    pca,
    "model/pca_model.pkl"
)

joblib.dump(
    clf,
    "model/classifier.pkl"
)

print("Models Saved Successfully")