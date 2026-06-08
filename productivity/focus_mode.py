import json
import os
from datetime import datetime


FOCUS_FILE = "data/focus_sessions.json"

focus_active = False
focus_start_time = None
focus_type = None


def load_focus_sessions():

    if not os.path.exists(FOCUS_FILE):
        return []

    try:
        with open(FOCUS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except:
        return []


def save_focus_sessions(sessions):

    os.makedirs("data", exist_ok=True)

    with open(FOCUS_FILE, "w", encoding="utf-8") as file:
        json.dump(sessions, file, indent=4)


def start_focus_mode(session_type="Focus"):

    global focus_active
    global focus_start_time
    global focus_type

    if focus_active:
        return "Focus mode is already active."

    focus_active = True
    focus_start_time = datetime.now()
    focus_type = session_type

    return f"{session_type} mode started. Stay focused."


def stop_focus_mode():

    global focus_active
    global focus_start_time
    global focus_type

    if not focus_active:
        return "No active focus session found."

    end_time = datetime.now()

    duration_minutes = int(
        (end_time - focus_start_time).total_seconds() // 60
    )

    session = {
        "type": focus_type,
        "start_time": str(focus_start_time),
        "end_time": str(end_time),
        "duration_minutes": duration_minutes
    }

    sessions = load_focus_sessions()
    sessions.append(session)
    save_focus_sessions(sessions)

    completed_type = focus_type

    focus_active = False
    focus_start_time = None
    focus_type = None

    return (
        f"{completed_type} session stopped.\n"
        f"Duration: {duration_minutes} minutes."
    )


def get_focus_status():

    if not focus_active:
        return "No focus session is currently active."

    current_time = datetime.now()

    duration_minutes = int(
        (current_time - focus_start_time).total_seconds() // 60
    )

    return (
        f"{focus_type} mode is active.\n"
        f"Duration: {duration_minutes} minutes."
    )


def get_focus_overlay_data():

    if not focus_active:

        return {
            "active": False,
            "type": "None",
            "minutes": 0,
            "display": "Focus: OFF"
        }

    current_time = datetime.now()

    duration_minutes = int(
        (current_time - focus_start_time).total_seconds() // 60
    )

    return {
        "active": True,
        "type": focus_type,
        "minutes": duration_minutes,
        "display": f"{focus_type}: {duration_minutes} min"
    }


def show_focus_history():

    sessions = load_focus_sessions()

    if not sessions:
        return "No focus sessions found."

    output = "Focus History:\n\n"

    for i, session in enumerate(sessions[-10:], start=1):

        output += (
            f"{i}. "
            f"{session['type']} - "
            f"{session['duration_minutes']} min\n"
        )

    return output