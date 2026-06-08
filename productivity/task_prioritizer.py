from ai.ollama_client import ask_ai

from productivity.task_manager import (
    get_task_context
)

from productivity.calendar_manager import (
    get_calendar_context
)

from core.vector_memory import (
    get_memory_context
)

from core.meeting_mode import (
    read_latest_meeting
)


# =====================================================
# PRIORITIZE TASKS
# =====================================================

def prioritize_tasks():

    task_context = get_task_context()

    calendar_context = get_calendar_context()

    memory_context = get_memory_context(
        "urgent work deadlines internship study pending tasks calendar meetings"
    )

    meeting_context = read_latest_meeting()

    if not task_context.strip():

        return (
            "You currently have no saved tasks.\n"
            "Add tasks using:\n"
            "add task <your task>"
        )

    prompt = f"""
You are AURON Task Prioritization Engine.

Analyze the user's current work and rank what they should do next.

Use:
1. Pending tasks
2. Calendar events
3. Meeting notes
4. Deadlines
5. Internship/study context
6. Long-term memory

Return output in this format:

WHAT YOU SHOULD WORK ON NEXT
----------------------------
1. <Top priority task>
   Reason: <short reason>
   Suggested time: <time estimate>

2. <Second priority task>
   Reason: <short reason>
   Suggested time: <time estimate>

3. <Third priority task>
   Reason: <short reason>
   Suggested time: <time estimate>

FINAL RECOMMENDATION
--------------------
Start with: <one task>

Current Tasks:
{task_context}

Calendar Events:
{calendar_context}

Latest Meeting Notes:
{meeting_context}

Relevant Memory:
{memory_context}
"""

    messages = [

        {
            "role": "system",
            "content":
                "You are an expert productivity and task prioritization assistant."
        },

        {
            "role": "user",
            "content": prompt
        }

    ]

    return ask_ai(
        messages
    )