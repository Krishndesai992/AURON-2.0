import os
import webbrowser
import urllib.parse


# ==========================================
# OPEN APPLICATION
# ==========================================

def open_application(app_name):

    app_name = app_name.lower()

    applications = {

        "notepad": "notepad.exe",

        "calculator": "calc.exe",

        "cmd": "cmd.exe",

        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    }

    if app_name in applications:

        try:

            os.startfile(applications[app_name])

            return f"Opening {app_name}."

        except Exception:

            return f"Could not open {app_name}."

    return f"{app_name} is not configured."


# ==========================================
# OPEN YOUTUBE
# ==========================================

def open_youtube():

    webbrowser.open(
        "https://www.youtube.com"
    )

    return "Opening YouTube."


# ==========================================
# OPEN GOOGLE
# ==========================================

def open_google():

    webbrowser.open(
        "https://www.google.com"
    )

    return "Opening Google."


# ==========================================
# GOOGLE SEARCH
# ==========================================

def google_search(query):

    encoded_query = urllib.parse.quote(query)

    url = f"https://www.google.com/search?q={encoded_query}"

    webbrowser.open(url)

    return f"Searching Google for {query}"


# ==========================================
# OPEN CHATGPT
# ==========================================

def open_chatgpt():

    webbrowser.open(
        "https://chat.openai.com"
    )

    return "Opening ChatGPT."


# ==========================================
# OPEN CHROME
# ==========================================

def open_chrome():

    chrome_paths = [

        r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]

    for path in chrome_paths:

        if os.path.exists(path):

            os.startfile(path)

            return "Opening Chrome."

    return "Chrome is not installed."


# ==========================================
# OPEN FOLDER
# ==========================================

def open_folder(path):

    if os.path.exists(path):

        os.startfile(path)

        return "Opening folder."

    return "Folder not found."


# ==========================================
# OPEN WEBSITE
# ==========================================

def open_website(url):

    webbrowser.open(url)

    return f"Opening {url}"