import os
from datetime import datetime


MEETING_FOLDER = "data/meeting_notes"

meeting_active = False
meeting_file_path = None


def start_meeting_mode():

    global meeting_active
    global meeting_file_path

    os.makedirs(
        MEETING_FOLDER,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y_%m_%d_%H_%M_%S"
    )

    filename = (
        f"meeting_{timestamp}.txt"
    )

    meeting_file_path = os.path.join(
        MEETING_FOLDER,
        filename
    )

    with open(
        meeting_file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "=====================================\n"
        )

        file.write(
            "AURON MEETING MODE SESSION\n"
        )

        file.write(
            f"Started: "
            f"{datetime.now()}\n"
        )

        file.write(
            "=====================================\n\n"
        )

    meeting_active = True

    return (
        "Meeting mode started. "
        "I am now taking notes."
    )


def stop_meeting_mode():

    global meeting_active
    global meeting_file_path

    if not meeting_active:

        return (
            "Meeting mode is not active."
        )

    with open(
        meeting_file_path,
        "a",
        encoding="utf-8"
    ) as file:

        file.write("\n")

        file.write(
            "=====================================\n"
        )

        file.write(
            f"Ended: "
            f"{datetime.now()}\n"
        )

        file.write(
            "=====================================\n"
        )

    meeting_active = False

    return (
        "Meeting mode stopped. "
        "Notes saved successfully."
    )


def add_meeting_note(text):

    global meeting_active
    global meeting_file_path

    if not meeting_active:

        return

    timestamp = datetime.now().strftime(
        "%H:%M"
    )

    note = (
        f"[{timestamp}] "
        f"{text}\n"
    )

    with open(
        meeting_file_path,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(note)


def is_meeting_active():

    return meeting_active


def get_latest_meeting_file():

    if not os.path.exists(
        MEETING_FOLDER
    ):

        return None

    files = [
        os.path.join(
            MEETING_FOLDER,
            file
        )
        for file in os.listdir(
            MEETING_FOLDER
        )
        if file.endswith(".txt")
    ]

    if not files:

        return None

    return max(
        files,
        key=os.path.getctime
    )


def read_latest_meeting():

    latest = get_latest_meeting_file()

    if not latest:

        return (
            "No meeting notes found."
        )

    with open(
        latest,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()