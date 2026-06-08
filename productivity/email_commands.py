from productivity.email_assistant import (
    generate_email_draft,
    generate_leave_email,
    generate_progress_email,
    generate_meeting_followup
)

from productivity.email_sender import (
    save_email_config,
    send_email
)

from productivity.email_reader import (
    check_unread_emails,
    summarize_latest_emails,
    summarize_today_emails,
    show_important_emails
)


# =====================================================
# PROCESS EMAIL COMMAND
# =====================================================

def process_email_command(user_message):

    user_message_lower = user_message.lower().strip()

    # =====================================================
    # SETUP EMAIL
    # Format:
    # setup email your@gmail.com app_password
    # =====================================================

    if user_message_lower.startswith("setup email"):

        parts = user_message.split()

        if len(parts) < 4:

            return (
                "Invalid setup format.\n"
                "Use:\n"
                "setup email your_email@gmail.com your_app_password"
            )

        email = parts[2]

        app_password = parts[3]

        return save_email_config(
            email,
            app_password
        )

    # =====================================================
    # SEND EMAIL
    # Format:
    # send email to someone@gmail.com subject Hello body Message
    # =====================================================

    if user_message_lower.startswith("send email to"):

        try:

            cleaned = user_message.replace(
                "send email to",
                ""
            ).strip()

            to_email, rest = cleaned.split(
                " subject ",
                1
            )

            subject, body = rest.split(
                " body ",
                1
            )

            return send_email(
                to_email.strip(),
                subject.strip(),
                body.strip()
            )

        except Exception:

            return (
                "Invalid send email format.\n"
                "Use:\n"
                "send email to someone@gmail.com subject Your Subject body Your message"
            )

    # =====================================================
    # DRAFT EMAIL
    # =====================================================

    if user_message_lower.startswith("draft email"):

        request = (
            user_message
            .replace(
                "draft email",
                ""
            )
            .strip()
        )

        return generate_email_draft(
            request
        )

    # =====================================================
    # EMAIL TEMPLATES
    # =====================================================

    if user_message_lower == "leave email":

        return generate_leave_email()

    if user_message_lower == "progress email":

        return generate_progress_email()

    if user_message_lower == "meeting followup email":

        return generate_meeting_followup()

    # =====================================================
    # CHECK UNREAD EMAILS
    # =====================================================

    if (
        user_message_lower == "check unread emails"
        or user_message_lower == "show unread emails"
        or user_message_lower == "unread emails"
    ):

        return check_unread_emails()

    # =====================================================
    # SUMMARIZE LATEST EMAILS
    # =====================================================

    if (
        user_message_lower == "summarize latest emails"
        or user_message_lower == "summarize recent emails"
        or user_message_lower == "latest email summary"
    ):

        return summarize_latest_emails()

    # =====================================================
    # SUMMARIZE TODAY'S EMAILS
    # =====================================================

    if (
        user_message_lower == "summarize today's emails"
        or user_message_lower == "summarize today emails"
        or user_message_lower == "today email summary"
        or user_message_lower == "summarize my emails today"
    ):

        return summarize_today_emails()

    # =====================================================
    # IMPORTANT EMAILS
    # =====================================================

    if (
        user_message_lower == "show important emails"
        or user_message_lower == "important emails"
        or user_message_lower == "find important emails"
    ):

        return show_important_emails()

    return None