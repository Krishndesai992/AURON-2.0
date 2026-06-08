from core.meeting_mode import (
    start_meeting_mode,
    stop_meeting_mode,
    add_meeting_note,
    is_meeting_active,
    read_latest_meeting
)

from core.meeting_analyzer import (
    summarize_meeting,
    extract_deadlines,
    extract_tasks
)


def process_meeting_command(command):

    command = command.lower().strip()

    # ==========================================
    # START MEETING
    # ==========================================

    if (
        "start meeting mode" in command
        or "start meeting" in command
    ):

        return start_meeting_mode()

    # ==========================================
    # STOP MEETING
    # ==========================================

    elif (
        "stop meeting mode" in command
        or "stop meeting" in command
    ):

        return stop_meeting_mode()

    # ==========================================
    # SHOW LAST MEETING
    # ==========================================

    elif (

        "show last meeting" in command
        or "show latest meeting" in command
        or "what happened in meeting" in command
        or "what happened today" in command
        or "what happened in today's meeting" in command
    ):

        return read_latest_meeting()

    # ==========================================
    # SUMMARIZE MEETING
    # ==========================================

    elif (

        "summarize last meeting" in command
        or "summarize meeting" in command
        or "meeting summary" in command
    ):

        meeting_text = (
            read_latest_meeting()
        )

        return summarize_meeting(
            meeting_text
        )

    # ==========================================
    # DEADLINES
    # ==========================================

    elif (

        "what deadlines were discussed"
        in command
        or "meeting deadlines"
        in command
        or "deadlines from meeting"
        in command
    ):

        meeting_text = (
            read_latest_meeting()
        )

        return extract_deadlines(
            meeting_text
        )

    # ==========================================
    # TASKS / ASSIGNED WORK
    # ==========================================

    elif (

        "what work am i assigned"
        in command
        or "what task did boss assign me"
        in command
        or "assigned tasks"
        in command
        or "meeting tasks"
        in command
    ):

        meeting_text = (
            read_latest_meeting()
        )

        return extract_tasks(
            meeting_text
        )

    return None


def handle_meeting_note(user_message):

    if not is_meeting_active():
        return

    blocked_words = [

        "start meeting",
        "stop meeting",
        "show meeting",
        "what happened",
        "summarize meeting",
        "meeting summary",
        "meeting deadlines",
        "assigned tasks",
        "what task did boss assign me",
        "what work am i assigned"
    ]

    lower_message = (
        user_message.lower()
    )

    for word in blocked_words:

        if word in lower_message:
            return

    add_meeting_note(
        user_message
    )