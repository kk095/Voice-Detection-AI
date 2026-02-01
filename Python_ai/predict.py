import sys
import json
import joblib
import os

from audio_utils import extract_features_from_base64

# Always resolve paths from this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")

# Read Base64 audio from STDIN
base64_audio = sys.stdin.read()

features = extract_features_from_base64(base64_audio)

model = joblib.load(MODEL_PATH)
prob = model.predict_proba([features])[0][1]
AI_THRESHOLD = 0.7  # safer threshold

classification = "AI_GENERATED" if prob >= AI_THRESHOLD else "HUMAN"

result = {
    "classification":classification,
    "confidenceScore": round(float(prob), 2),
    "explanation": (
        "Unnaturally consistent acoustic patterns detected"
        if prob >= 0.5
        else "Natural pitch variation and human-like pauses detected"
    )
}

print(json.dumps(result))
