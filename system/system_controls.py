from system.app_launcher import (
    open_application,
    open_youtube,
    open_google,
    google_search,
    open_chrome,
    open_website
)


# ==========================================
# PROCESS SYSTEM COMMAND
# ==========================================

def process_system_command(command):

    command = command.lower()


    # ==========================================
    # YOUTUBE
    # ==========================================

    if "youtube" in command:

        return open_youtube()


    # ==========================================
    # GOOGLE
    # ==========================================

    elif command == "open google":

        return open_google()


    # ==========================================
    # CHROME
    # ==========================================

    elif "open chrome" in command:

        return open_chrome()


    # ==========================================
    # GOOGLE SEARCH
    # ==========================================

    elif "search google for" in command:

        query = command.replace(
            "search google for",
            ""
        ).strip()

        return google_search(query)


    # ==========================================
    # OPEN WEBSITE
    # ==========================================

    elif "open website" in command:

        website = command.replace(
            "open website",
            ""
        ).strip()

        if not website.startswith("http"):

            website = "https://" + website

        return open_website(website)


    # ==========================================
    # OPEN APPLICATIONS
    # ==========================================

    elif "open" in command:

        app_name = command.replace(
            "open",
            ""
        ).strip()

        return open_application(app_name)


    # ==========================================
    # NO COMMAND
    # ==========================================

    return None