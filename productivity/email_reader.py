import imaplib
import email
from email.header import decode_header
from datetime import datetime

from ai.ollama_client import ask_ai

from productivity.email_sender import load_email_config


# =====================================================
# DECODE EMAIL TEXT
# =====================================================

def decode_text(text):

    if not text:
        return ""

    decoded_parts = decode_header(text)

    final_text = ""

    for part, encoding in decoded_parts:

        if isinstance(part, bytes):

            try:
                final_text += part.decode(
                    encoding or "utf-8",
                    errors="ignore"
                )

            except:
                final_text += part.decode(
                    "utf-8",
                    errors="ignore"
                )

        else:

            final_text += part

    return final_text


# =====================================================
# CONNECT TO GMAIL
# =====================================================

def connect_to_gmail():

    email_address, app_password = load_email_config()

    if not email_address or not app_password:

        return None, (
            "Email is not configured.\n"
            "Use:\n"
            "setup email your_email@gmail.com your_app_password"
        )

    try:

        mail = imaplib.IMAP4_SSL(
            "imap.gmail.com"
        )

        mail.login(
            email_address,
            app_password
        )

        return mail, None

    except Exception as e:

        return None, (
            "Could not connect to Gmail inbox:\n"
            f"{e}"
        )


# =====================================================
# GET EMAIL BODY
# =====================================================

def get_email_body(message):

    body = ""

    if message.is_multipart():

        for part in message.walk():

            content_type = part.get_content_type()

            content_disposition = str(
                part.get("Content-Disposition")
            )

            if (
                content_type == "text/plain"
                and "attachment" not in content_disposition
            ):

                try:

                    payload = part.get_payload(
                        decode=True
                    )

                    if payload:

                        body += payload.decode(
                            errors="ignore"
                        )

                except:

                    pass

    else:

        try:

            payload = message.get_payload(
                decode=True
            )

            if payload:

                body = payload.decode(
                    errors="ignore"
                )

        except:

            pass

    return body.strip()


# =====================================================
# FETCH EMAILS
# =====================================================

def fetch_emails(search_criteria="ALL", limit=5):

    mail, error = connect_to_gmail()

    if error:
        return None, error

    try:

        mail.select("inbox")

        status, messages = mail.search(
            None,
            search_criteria
        )

        if status != "OK":

            return None, (
                "Could not search inbox."
            )

        email_ids = messages[0].split()

        email_ids = email_ids[-limit:]

        emails = []

        for email_id in reversed(email_ids):

            status, msg_data = mail.fetch(
                email_id,
                "(RFC822)"
            )

            if status != "OK":
                continue

            raw_email = msg_data[0][1]

            message = email.message_from_bytes(
                raw_email
            )

            subject = decode_text(
                message.get("Subject")
            )

            sender = decode_text(
                message.get("From")
            )

            date = decode_text(
                message.get("Date")
            )

            body = get_email_body(
                message
            )

            emails.append({

                "from": sender,
                "subject": subject,
                "date": date,
                "body": body[:1500]

            })

        mail.logout()

        return emails, None

    except Exception as e:

        try:
            mail.logout()
        except:
            pass

        return None, (
            "Email fetch failed:\n"
            f"{e}"
        )


# =====================================================
# CHECK UNREAD EMAILS
# =====================================================

def check_unread_emails():

    emails, error = fetch_emails(
        "UNSEEN",
        limit=10
    )

    if error:
        return error

    if not emails:

        return (
            "No unread emails found."
        )

    output = (
        f"Unread Emails: {len(emails)}\n\n"
    )

    for i, mail_item in enumerate(
        emails,
        start=1
    ):

        output += (
            f"{i}. From: {mail_item['from']}\n"
            f"Subject: {mail_item['subject']}\n\n"
        )

    return output


# =====================================================
# SUMMARIZE LATEST EMAILS
# =====================================================

def summarize_latest_emails():

    emails, error = fetch_emails(
        "ALL",
        limit=5
    )

    if error:
        return error

    if not emails:

        return (
            "No emails found."
        )

    email_text = ""

    for item in emails:

        email_text += (
            f"From: {item['from']}\n"
            f"Subject: {item['subject']}\n"
            f"Body: {item['body']}\n\n"
        )

    prompt = f"""
You are AURON Email Assistant.

Summarize the latest emails clearly.

Return:
1. Important emails
2. Quick summaries
3. Action items if any

Emails:
{email_text}
"""

    messages = [

        {
            "role": "system",
            "content":
                "You summarize inbox emails professionally."
        },

        {
            "role": "user",
            "content": prompt
        }

    ]

    return ask_ai(
        messages
    )


# =====================================================
# SUMMARIZE TODAY EMAILS
# =====================================================

def summarize_today_emails():

    today = datetime.now().strftime(
        "%d-%b-%Y"
    )

    emails, error = fetch_emails(
        f'SINCE "{today}"',
        limit=10
    )

    if error:
        return error

    if not emails:

        return (
            "No emails found for today."
        )

    email_text = ""

    for item in emails:

        email_text += (
            f"From: {item['from']}\n"
            f"Subject: {item['subject']}\n"
            f"Body: {item['body']}\n\n"
        )

    prompt = f"""
Summarize today's emails.

Return:
- Important updates
- Action items
- Deadlines
- Emails requiring reply

Emails:
{email_text}
"""

    messages = [

        {
            "role": "system",
            "content":
                "You are an email productivity assistant."
        },

        {
            "role": "user",
            "content": prompt
        }
    ]

    return ask_ai(
        messages
    )


# =====================================================
# IMPORTANT EMAILS
# =====================================================

def show_important_emails():

    emails, error = fetch_emails(
        "ALL",
        limit=10
    )

    if error:
        return error

    if not emails:

        return (
            "No emails found."
        )

    email_text = ""

    for item in emails:

        email_text += (
            f"From: {item['from']}\n"
            f"Subject: {item['subject']}\n"
            f"Body: {item['body']}\n\n"
        )

    prompt = f"""
Find important emails from this inbox list.

Consider important:
- work/internship related
- deadlines
- interview/internship/job messages
- urgent requests
- project/task related

Return only important emails with reason.

Emails:
{email_text}
"""

    messages = [

        {
            "role": "system",
            "content":
                "You identify important emails."
        },

        {
            "role": "user",
            "content": prompt
        }
    ]

    return ask_ai(
        messages
    )