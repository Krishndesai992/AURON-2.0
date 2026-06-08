from ai.ollama_client import ask_ai


# =====================================================
# GENERATE EMAIL DRAFT
# =====================================================

def generate_email_draft(request):

    prompt = f"""
You are AURON Email Assistant.

Generate a professional email.

Requirements:
- Include Subject
- Professional formatting
- Proper greeting
- Proper closing
- Clear and concise
- Ready to send

User Request:
{request}

Return:

Subject:

Email:
"""

    messages = [

        {
            "role": "system",
            "content":
                (
                    "You are an expert "
                    "professional email writer."
                )
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
# EMAIL TEMPLATES
# =====================================================

def generate_leave_email():

    return """
Subject: Leave Request

Dear Sir/Madam,

I hope you are doing well.

I would like to request leave for tomorrow due to personal reasons.

I will ensure that all pending work is managed appropriately.

Thank you for your understanding.

Regards,
Krish Desai
"""


def generate_progress_email():

    return """
Subject: Internship Progress Update

Dear Sir/Madam,

I would like to provide an update on my current progress.

Completed:
- Assigned development tasks
- Testing and validation

In Progress:
- Feature implementation
- Documentation updates

Please let me know if any additional work should be prioritized.

Regards,
Krish Desai
"""


def generate_meeting_followup():

    return """
Subject: Meeting Follow-Up

Dear Sir/Madam,

Thank you for today's meeting.

I have noted the discussed points and will proceed with the assigned tasks.

Please let me know if any clarification is required.

Regards,
Krish Desai
"""