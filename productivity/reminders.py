import os
from datetime import datetime


# =====================================================
# SAVE REMINDER
# =====================================================

def save_reminder(reminder_text):

    os.makedirs(
        "data/reminders",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = f"reminder_{timestamp}.txt"

    filepath = os.path.join(
        "data/reminders",
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(reminder_text)

    return filepath