import numpy as np
import threading
 
def record_and_verify_gender(duration=3, sample_rate=44100):
    """
    Record audio from microphone and classify gender from voice.
    Uses pitch (fundamental frequency) analysis.
    Male voice: ~85-180 Hz
    Female voice: ~165-255 Hz
    Returns: dict with gender and confidence
    """
    try:
        import sounddevice as sd
        import librosa
 
        # Record audio
        audio = sd.rec(int(duration * sample_rate),
                       samplerate=sample_rate,
                       channels=1, dtype='float32')
        sd.wait()
        audio = audio.flatten()
 
        # Analyze pitch
        pitches, magnitudes = librosa.piptrack(
            y=audio, sr=sample_rate,
            fmin=50, fmax=400
        )
        # Get mean pitch of most prominent frequencies
        pitch_vals = pitches[magnitudes > np.percentile(magnitudes, 75)]
        pitch_vals = pitch_vals[pitch_vals > 0]
 
        if len(pitch_vals) == 0:
            return {"gender": "Unknown", "confidence": 0.0, "pitch_hz": 0}
 
        mean_pitch = float(np.mean(pitch_vals))
 
        # Classify based on pitch
        # Overlap zone: 165-180 Hz — use confidence scoring
        if mean_pitch < 150:
            gender = "Male"
            confidence = min(95, 60 + (150 - mean_pitch) / 150 * 35)
        elif mean_pitch > 190:
            gender = "Female"
            confidence = min(95, 60 + (mean_pitch - 190) / 100 * 35)
        elif mean_pitch < 165:
            gender = "Male"
            confidence = max(55, 70 - (mean_pitch - 150) * 1.5)
        else:
            gender = "Female"
            confidence = max(55, 70 - (190 - mean_pitch) * 1.5)
 
        return {
            "gender": gender,
            "confidence": round(confidence, 1),
            "pitch_hz": round(mean_pitch, 1)
        }
 
    except ImportError:
        # Fallback demo if sounddevice/librosa not installed
        import random
        gender = random.choice(["Male", "Female"])
        return {
            "gender": gender,
            "confidence": round(random.uniform(75, 92), 1),
            "pitch_hz": round(random.uniform(100, 250), 1),
            "note": "Demo mode — install sounddevice & librosa for real voice analysis"
        }
    except Exception as e:
        return {"gender": "Unknown", "confidence": 0.0, "error": str(e)}
 
 
def announce(text: str):
    """
    Speak text via pyttsx3 in background thread.
    Won't block the Streamlit UI.
    """
    def _speak():
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 145)
            engine.setProperty('volume', 0.95)
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
 
    threading.Thread(target=_speak, daemon=True).start()