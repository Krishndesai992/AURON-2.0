import os
import json
import hashlib


VOICE_AUTH_FILE = "data/voice_auth.json"


# =====================================================
# NORMALIZE PHRASE
# =====================================================

def normalize_phrase(phrase):

    return (
        phrase
        .lower()
        .strip()
        .replace(".", "")
        .replace(",", "")
        .replace("!", "")
        .replace("?", "")
    )


# =====================================================
# HASH PHRASE
# =====================================================

def hash_phrase(phrase):

    normalized = normalize_phrase(
        phrase
    )

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


# =====================================================
# VOICE AUTH EXISTS
# =====================================================

def voice_auth_exists():

    return os.path.exists(
        VOICE_AUTH_FILE
    )


# =====================================================
# SET VOICE PHRASE
# =====================================================

def setup_voice_phrase(phrase):

    if not phrase.strip():

        return False, "Voice phrase cannot be empty."

    os.makedirs(
        "data",
        exist_ok=True
    )

    data = {
        "voice_phrase_hash":
            hash_phrase(
                phrase
            )
    }

    with open(
        VOICE_AUTH_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    return True, "Voice phrase setup successful."


# =====================================================
# VERIFY VOICE PHRASE
# =====================================================

def verify_voice_phrase(phrase):

    if not voice_auth_exists():

        return False, "Voice phrase is not configured."

    try:

        with open(
            VOICE_AUTH_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        saved_hash = data.get(
            "voice_phrase_hash"
        )

        entered_hash = hash_phrase(
            phrase
        )

        if entered_hash == saved_hash:

            return True, "Voice authentication successful."

        return False, "Voice phrase did not match."

    except Exception as e:

        return False, f"Voice authentication error: {e}"


# =====================================================
# RESET VOICE AUTH
# =====================================================

def reset_voice_auth():

    if os.path.exists(
        VOICE_AUTH_FILE
    ):

        os.remove(
            VOICE_AUTH_FILE
        )

    return "Voice authentication reset successfully."