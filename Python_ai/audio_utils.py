import base64
import librosa
import numpy as np
from pydub import AudioSegment
from io import BytesIO

def _extract_features_from_samples(samples, sr=16000):
    samples = samples.astype(float)
    samples /= np.max(np.abs(samples)) + 1e-6

    mfcc = librosa.feature.mfcc(y=samples, sr=sr, n_mfcc=13)
    mfcc_mean = mfcc.mean(axis=1)
    mfcc_std = mfcc.std(axis=1)

    zcr = librosa.feature.zero_crossing_rate(samples).mean()
    rms = librosa.feature.rms(y=samples).mean()

    return np.hstack([
        mfcc_mean,  # 13
        mfcc_std,   # 13
        zcr,        # 1
        rms         # 1
    ])              # TOTAL = 28 features


def extract_features_from_mp3(mp3_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    samples = np.array(audio.get_array_of_samples())
    return _extract_features_from_samples(samples)


def extract_features_from_base64(base64_audio):
    audio_bytes = base64.b64decode(base64_audio)
    audio = AudioSegment.from_mp3(BytesIO(audio_bytes))
    audio = audio.set_frame_rate(16000).set_channels(1)
    samples = np.array(audio.get_array_of_samples())
    return _extract_features_from_samples(samples)
