import os
import json
import hashlib
import secrets


AUTH_FILE = "data/auth_config.json"


def _ensure_data_folder():

    os.makedirs(
        "data",
        exist_ok=True
    )


def _hash_value(value, salt):

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        value.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    )

    return hashed.hex()


def auth_exists():

    return os.path.exists(
        AUTH_FILE
    )


def setup_passkey(passkey):

    if not passkey.strip():

        return False, "Passkey cannot be empty."

    _ensure_data_folder()

    salt = secrets.token_hex(16)

    passkey_hash = _hash_value(
        passkey,
        salt
    )

    data = {
        "salt": salt,
        "passkey_hash": passkey_hash
    }

    with open(
        AUTH_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    return True, "Passkey setup successful."


def verify_passkey(passkey):

    if not auth_exists():

        return False, "No passkey setup found."

    try:

        with open(
            AUTH_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        salt = data.get("salt")

        saved_hash = data.get("passkey_hash")

        entered_hash = _hash_value(
            passkey,
            salt
        )

        if entered_hash == saved_hash:

            return True, "Authentication successful."

        return False, "Incorrect passkey."

    except Exception as e:

        return False, f"Authentication error: {e}"


def reset_auth():

    if os.path.exists(
        AUTH_FILE
    ):

        os.remove(
            AUTH_FILE
        )

    return "Authentication reset successfully."