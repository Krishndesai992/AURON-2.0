import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile


def listen_to_voice():

    recognizer = sr.Recognizer()

    try:

        # ============================================
        # RECORD AUDIO
        # ============================================

        sample_rate = 44100
        duration = 5

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        # ============================================
        # SAVE TEMP AUDIO
        # ============================================

        temp_wav = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )

        write(
            temp_wav.name,
            sample_rate,
            recording
        )

        # ============================================
        # SPEECH RECOGNITION
        # ============================================

        with sr.AudioFile(temp_wav.name) as source:

            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:

        return None

    except Exception as e:

        return f"Voice Error: {e}"