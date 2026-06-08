import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


EMAIL_CONFIG_FILE = "data/email_config.txt"


# =====================================================
# SAVE EMAIL CONFIG
# =====================================================

def save_email_config(email, app_password):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        EMAIL_CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{email}\n{app_password}"
        )

    return (
        "Email configuration saved successfully."
    )


# =====================================================
# LOAD EMAIL CONFIG
# =====================================================

def load_email_config():

    if not os.path.exists(
        EMAIL_CONFIG_FILE
    ):

        return None, None

    try:

        with open(
            EMAIL_CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.read().splitlines()

            if len(lines) < 2:
                return None, None

            return lines[0], lines[1]

    except:

        return None, None


# =====================================================
# SEND EMAIL
# =====================================================

def send_email(to_email, subject, body):

    sender_email, app_password = load_email_config()

    if not sender_email or not app_password:

        return (
            "Email is not configured.\n"
            "Use:\n"
            "setup email your_email@gmail.com your_app_password"
        )

    try:

        message = MIMEMultipart()

        message["From"] = sender_email

        message["To"] = to_email

        message["Subject"] = subject

        message.attach(
            MIMEText(
                body,
                "plain"
            )
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            app_password
        )

        server.send_message(
            message
        )

        server.quit()

        return (
            "Email sent successfully."
        )

    except Exception as e:

        return (
            "Email sending failed:\n"
            f"{e}"
        )