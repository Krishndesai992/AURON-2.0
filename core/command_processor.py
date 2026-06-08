from datetime import datetime

from system.app_launcher import (
    open_notepad,
    open_calculator,
    open_cmd,
    open_explorer
)

from system.battery import get_battery_status


def process_command(user_input):

    text = user_input.lower()

    # =========================================
    # OPEN APPS
    # =========================================

    if "open notepad" in text:
        open_notepad()
        return "Opening Notepad."

    elif "open calculator" in text:
        open_calculator()
        return "Opening Calculator."

    elif "open cmd" in text:
        open_cmd()
        return "Opening Command Prompt."

    elif "open explorer" in text:
        open_explorer()
        return "Opening File Explorer."

    # =========================================
    # BATTERY
    # =========================================

    elif "battery" in text:
        return get_battery_status()

    # =========================================
    # TIME
    # =========================================

    elif "time" in text:

        current_time = datetime.now().strftime("%I:%M %p")

        return f"Current time is {current_time}"

    # =========================================
    # DATE
    # =========================================

    elif "date" in text:

        current_date = datetime.now().strftime("%d %B %Y")

        return f"Today's date is {current_date}"

    # =========================================
    # NO COMMAND FOUND
    # =========================================

    return None