import os
from datetime import datetime

NOTES_FOLDER = "data/notes"


def save_note(note_text):

    os.makedirs(NOTES_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"note_{timestamp}.txt"

    filepath = os.path.join(NOTES_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(note_text)

    return filepath


def get_all_notes():

    os.makedirs(NOTES_FOLDER, exist_ok=True)

    notes = []

    for file in os.listdir(NOTES_FOLDER):

        if file.endswith(".txt"):

            notes.append(file)

    notes.sort(reverse=True)

    return notes