import json
import os
from datetime import datetime


STICKY_NOTES_FILE = "data/sticky_notes.json"


# =====================================================
# LOAD STICKY NOTES
# =====================================================

def load_sticky_notes():

    if not os.path.exists(
        STICKY_NOTES_FILE
    ):

        return []

    try:

        with open(
            STICKY_NOTES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except:

        return []


# =====================================================
# SAVE STICKY NOTES
# =====================================================

def save_sticky_notes(notes):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        STICKY_NOTES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            notes,
            file,
            indent=4
        )


# =====================================================
# ADD STICKY NOTE
# =====================================================

def add_sticky_note(note_text):

    note_text = note_text.strip()

    if not note_text:

        return (
            "Please provide sticky note content."
        )

    notes = load_sticky_notes()

    note = {

        "note": note_text,
        "created_at": str(
            datetime.now()
        )
    }

    notes.append(
        note
    )

    save_sticky_notes(
        notes
    )

    return (
        "Sticky note added:\n"
        f"{note_text}"
    )


# =====================================================
# SHOW STICKY NOTES
# =====================================================

def show_sticky_notes():

    notes = load_sticky_notes()

    if not notes:

        return (
            "No sticky notes found."
        )

    output = (
        "Sticky Notes:\n\n"
    )

    for i, note in enumerate(
        notes,
        start=1
    ):

        output += (
            f"{i}. "
            f"{note['note']}\n"
        )

    return output


# =====================================================
# DELETE STICKY NOTE
# =====================================================

def delete_sticky_note(note_keyword):

    notes = load_sticky_notes()

    updated_notes = [

        note
        for note in notes

        if note_keyword.lower()
        not in note["note"].lower()
    ]

    if len(updated_notes) == len(notes):

        return (
            "Sticky note not found."
        )

    save_sticky_notes(
        updated_notes
    )

    return (
        "Sticky note deleted:\n"
        f"{note_keyword}"
    )


# =====================================================
# CLEAR STICKY NOTES
# =====================================================

def clear_sticky_notes():

    save_sticky_notes(
        []
    )

    return (
        "All sticky notes cleared."
    )


# =====================================================
# STICKY NOTES CONTEXT
# =====================================================

def get_sticky_notes_context():

    notes = load_sticky_notes()

    if not notes:
        return ""

    context = (
        "Sticky Notes:\n"
    )

    for note in notes:

        context += (
            f"- {note['note']}\n"
        )

    return context