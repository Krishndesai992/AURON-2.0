from ai.ollama_client import ask_ai

from productivity.task_manager import (
    get_task_context
)

from productivity.day_summary import (
    generate_day_summary
)

from core.meeting_mode import (
    read_latest_meeting
)

from core.vector_memory import (
    get_memory_context
)

from core.memory import (
    load_memory
)


# =====================================================
# GENERATE DAILY STANDUP
# =====================================================

def generate_standup_report():

    task_context = get_task_context()

    day_summary = generate_day_summary()

    meeting_context = read_latest_meeting()

    memory_context = get_memory_context(
        "yesterday today work progress blockers internship tasks meetings"
    )

    recent_memory = load_memory()

    recent_chat_text = ""

    for item in recent_memory:

        recent_chat_text += (
            f"{item['role']}: "
            f"{item['content']}\n"
        )

    prompt = f"""
You are AURON Daily Standup Generator.

Generate a professional daily standup update for an internship/work setting.

Use the available context and return only this format:

DAILY STANDUP
-------------

Yesterday I worked on:
- ...

Today I will work on:
- ...

Blockers:
- ...

Notes:
- ...

Rules:
- Keep it concise.
- Use professional wording.
- If blockers are not found, write "No blockers currently identified."
- Do not invent unrealistic details.
- Prefer actual tasks, meetings, and recent work context.

Current Tasks:
{task_context}

Generated Day Summary:
{day_summary}

Latest Meeting Notes:
{meeting_context}

Relevant Long-Term Memory:
{memory_context}

Recent Conversation Memory:
{recent_chat_text}
"""

    messages = [

        {
            "role": "system",
            "content":
                (
                    "You are a professional "
                    "internship daily standup assistant."
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