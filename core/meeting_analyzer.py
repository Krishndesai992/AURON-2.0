from ai.ollama_client import ask_ai


def summarize_meeting(meeting_text):

    prompt = f"""
You are an internship meeting assistant.

Analyze this meeting transcript and return:

1. Topics Discussed
2. Key Decisions
3. Deadlines
4. Action Items (TODOs)
5. Work Assigned to Me

Keep the answer structured and concise.

Meeting Transcript:
{meeting_text}
"""

    messages = [

        {
            "role": "system",
            "content":
                "You are a smart meeting assistant."
        },

        {
            "role": "user",
            "content": prompt
        }

    ]

    response = ask_ai(messages)

    return response


def extract_deadlines(meeting_text):

    prompt = f"""
Extract deadlines from this meeting.

Return only bullet points.

Meeting:
{meeting_text}
"""

    messages = [

        {
            "role": "user",
            "content": prompt
        }

    ]

    return ask_ai(messages)


def extract_tasks(meeting_text):

    prompt = f"""
Extract assigned work and action items.

Return concise bullet points.

Meeting:
{meeting_text}
"""

    messages = [

        {
            "role": "user",
            "content": prompt
        }

    ]

    return ask_ai(messages)