import pyttsx3
import threading


# ==========================================================
# SPEECH LOCK
# ==========================================================

speech_lock = threading.Lock()


# ==========================================================
# CLEAN TEXT FOR SPEECH
# ==========================================================

def clean_text_for_speech(text):

    if not text:
        return ""

    cleaned = str(text)

    replacements = {
        "✅": "",
        "❌": "",
        "🎙": "",
        "🎤": "",
        "•": "",
        "*": "",
        "#": "",
        "`": "",
        "_": "",
        "|": " ",
        "-": " ",
        "\n": ". "
    }

    for old, new in replacements.items():

        cleaned = cleaned.replace(
            old,
            new
        )

    return cleaned.strip()


# ==========================================================
# SPEAK FUNCTION
# ==========================================================

def speak_text(text):

    cleaned_text = clean_text_for_speech(
        text
    )

    if not cleaned_text:
        return

    def run_speech():

        with speech_lock:

            engine = None

            try:

                engine = pyttsx3.init()

                voices = engine.getProperty(
                    "voices"
                )

                if voices:

                    engine.setProperty(
                        "voice",
                        voices[0].id
                    )

                engine.setProperty(
                    "rate",
                    170
                )

                engine.setProperty(
                    "volume",
                    1.0
                )

                engine.say(
                    cleaned_text
                )

                engine.runAndWait()

            except Exception as e:

                print(
                    "TTS Error:",
                    e
                )

            finally:

                try:

                    if engine:

                        engine.stop()

                except:

                    pass

    threading.Thread(
        target=run_speech,
        daemon=True
    ).start()