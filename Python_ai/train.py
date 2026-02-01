import os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

from audio_utils import extract_features_from_mp3


DATA_DIR = "data"
HUMAN_DIR = os.path.join(DATA_DIR, "human")
AI_DIR = os.path.join(DATA_DIR, "ai")

X = []
y = []

print("Loading HUMAN samples...")
for file in os.listdir(HUMAN_DIR):
    if file.endswith(".mp3"):
        path = os.path.join(HUMAN_DIR, file)
        features = extract_features_from_mp3(path)
        X.append(features)
        y.append(0)   # 0 = HUMAN

print("Loading AI samples...")
for file in os.listdir(AI_DIR):
    if file.endswith(".mp3"):
        path = os.path.join(AI_DIR, file)
        features = extract_features_from_mp3(path)
        X.append(features)
        y.append(1)   # 1 = AI_GENERATED

X = np.array(X)
y = np.array(y)

print(f"Total samples: {len(X)}")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"Model accuracy: {acc:.2f}")

# Save model
joblib.dump(model, "model.joblib")
print("✅ model.joblib saved successfully")
cd