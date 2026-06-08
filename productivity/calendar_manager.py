import json
import os
import re

from datetime import datetime, timedelta


CALENDAR_FILE = "data/calendar_events.json"


# =====================================================
# LOAD EVENTS
# =====================================================

def load_events():

    if not os.path.exists(CALENDAR_FILE):
        return []

    try:

        with open(CALENDAR_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except:
        return []


# =====================================================
# SAVE EVENTS
# =====================================================

def save_events(events):

    os.makedirs("data", exist_ok=True)

    with open(CALENDAR_FILE, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=4)


# =====================================================
# PARSE DATE
# =====================================================

def parse_event_date(text):

    lower_text = text.lower()

    today = datetime.now().date()

    if "tomorrow" in lower_text:
        return str(today + timedelta(days=1))

    if "today" in lower_text:
        return str(today)

    date_match = re.search(
        r"\d{4}-\d{2}-\d{2}",
        text
    )

    if date_match:
        return date_match.group()

    return "unscheduled"


# =====================================================
# PARSE TIME
# =====================================================

def parse_event_time(text):

    lower_text = text.lower()

    time_match = re.search(
        r"(\d{1,2})(:\d{2})?\s*(am|pm)?",
        lower_text
    )

    if not time_match:
        return "unspecified"

    hour = int(time_match.group(1))

    minute = time_match.group(2)

    period = time_match.group(3)

    if minute:
        minute = minute.replace(":", "")
    else:
        minute = "00"

    if period == "pm" and hour != 12:
        hour += 12

    if period == "am" and hour == 12:
        hour = 0

    return f"{hour:02d}:{minute}"


# =====================================================
# ADD EVENT
# =====================================================

def add_calendar_event(event_text):

    event_text = event_text.strip()

    if not event_text:

        return "Please provide event details."

    events = load_events()

    event_date = parse_event_date(event_text)

    event_time = parse_event_time(event_text)

    event = {
        "title": event_text,
        "date": event_date,
        "time": event_time,
        "created_at": str(datetime.now()),
        "completed": False
    }

    events.append(event)

    save_events(events)

    return (
        "Calendar event added:\n"
        f"Title: {event_text}\n"
        f"Date: {event_date}\n"
        f"Time: {event_time}"
    )


# =====================================================
# SHOW EVENTS
# =====================================================

def show_calendar_events():

    events = load_events()

    if not events:
        return "No calendar events found."

    sorted_events = sorted(
        events,
        key=lambda event: (
            event.get("date", "unscheduled"),
            event.get("time", "unspecified")
        )
    )

    output = "Calendar Events:\n\n"

    for i, event in enumerate(sorted_events, start=1):

        output += (
            f"{i}. {event['title']}\n"
            f"   Date: {event.get('date', 'unscheduled')}\n"
            f"   Time: {event.get('time', 'unspecified')}\n\n"
        )

    return output


# =====================================================
# DELETE EVENT
# =====================================================

def delete_calendar_event(event_name):

    events = load_events()

    updated_events = [
        event
        for event in events
        if event_name.lower() not in event["title"].lower()
    ]

    if len(updated_events) == len(events):

        return "Calendar event not found."

    save_events(updated_events)

    return (
        "Calendar event deleted:\n"
        f"{event_name}"
    )


# =====================================================
# GET SCHEDULE BY DATE
# =====================================================

def get_schedule_by_date(target_date, title):

    events = load_events()

    if not events:
        return "No events scheduled."

    matched_events = [
        event
        for event in events
        if event.get("date") == target_date
    ]

    if not matched_events:
        return f"No events scheduled for {title}."

    matched_events = sorted(
        matched_events,
        key=lambda event: event.get("time", "unspecified")
    )

    output = f"{title} Schedule:\n\n"

    for event in matched_events:

        output += (
            f"- {event.get('time', 'unspecified')} "
            f"| {event['title']}\n"
        )

    return output


# =====================================================
# TODAY SCHEDULE
# =====================================================

def today_schedule():

    today = str(datetime.now().date())

    return get_schedule_by_date(
        today,
        "Today's"
    )


# =====================================================
# TOMORROW SCHEDULE
# =====================================================

def tomorrow_schedule():

    tomorrow = str(
        datetime.now().date() + timedelta(days=1)
    )

    return get_schedule_by_date(
        tomorrow,
        "Tomorrow's"
    )


# =====================================================
# CALENDAR CONTEXT
# =====================================================

def get_calendar_context():

    events = load_events()

    if not events:
        return ""

    context = "Calendar Events:\n"

    for event in events:

        context += (
            f"- {event['title']} "
            f"on {event.get('date', 'unscheduled')} "
            f"at {event.get('time', 'unspecified')}\n"
        )

    return context