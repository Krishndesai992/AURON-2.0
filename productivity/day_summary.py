from ai.ollama_client import ask_ai

from productivity.task_manager import (
    get_task_context
)

from core.vector_memory import (
    get_memory_context
)

from core.meeting_mode import (
    read_latest_meeting
)

from core.memory import (
    load_memory
)


# =====================================================
# GENERATE DAY SUMMARY
# =====================================================

def generate_day_summary():

    task_context = (
        get_task_context()
    )

    memory_context = (
        get_memory_context(
            "today work internship study project progress"
        )
    )

    meeting_context = (
        read_latest_meeting()
    )

    recent_chat = load_memory()

    chat_text = ""

    for item in recent_chat:

        chat_text += (
            f"{item['role']}: "
            f"{item['content']}\n"
        )

    prompt = f"""
You are AURON productivity assistant.

Generate a concise professional summary of today's work.

Use:

1. Current Tasks
2. Meeting Notes
3. Recent Conversations
4. Relevant Long-Term Memory

Return:

TODAY'S WORK
------------
Completed Work:
- ...

Topics Worked On:
- ...

Meetings:
- ...

Pending Work:
- ...

Recommended Next Steps:
- ...

Current Tasks:
{task_context}

Meeting Notes:
{meeting_context}

Recent Conversations:
{chat_text}

Relevant Memory:
{memory_context}
"""

    messages = [

        {
            "role": "system",
            "content":
                (
                    "You are an expert "
                    "productivity assistant."
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