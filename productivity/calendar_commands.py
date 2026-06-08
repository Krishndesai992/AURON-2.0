from productivity.calendar_manager import (
    add_calendar_event,
    show_calendar_events,
    delete_calendar_event,
    today_schedule,
    tomorrow_schedule
)


# =====================================================
# PROCESS CALENDAR COMMAND
# =====================================================

def process_calendar_command(user_message):

    user_message_lower = user_message.lower().strip()

    # =====================================================
    # ADD CALENDAR EVENT
    # =====================================================

    if (
        user_message_lower.startswith("add calendar event")
        or user_message_lower.startswith("add event")
    ):

        event_text = (
            user_message
            .replace("add calendar event", "")
            .replace("add event", "")
            .strip()
        )

        return add_calendar_event(
            event_text
        )

    # =====================================================
    # SHOW CALENDAR EVENTS
    # =====================================================

    if (
        user_message_lower == "show calendar events"
        or user_message_lower == "show events"
        or user_message_lower == "my calendar"
    ):

        return show_calendar_events()

    # =====================================================
    # TODAY SCHEDULE
    # =====================================================

    if (
        user_message_lower == "today's schedule"
        or user_message_lower == "today schedule"
        or user_message_lower == "show today's schedule"
    ):

        return today_schedule()

    # =====================================================
    # TOMORROW SCHEDULE
    # =====================================================

    if (
        user_message_lower == "tomorrow's schedule"
        or user_message_lower == "tomorrow schedule"
        or user_message_lower == "show tomorrow schedule"
    ):

        return tomorrow_schedule()

    # =====================================================
    # DELETE CALENDAR EVENT
    # =====================================================

    if (
        user_message_lower.startswith("delete calendar event")
        or user_message_lower.startswith("delete event")
    ):

        event_name = (
            user_message
            .replace("delete calendar event", "")
            .replace("delete event", "")
            .strip()
        )

        return delete_calendar_event(
            event_name
        )

    return None