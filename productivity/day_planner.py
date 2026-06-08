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


# =====================================================
# GENERATE DAILY PLAN
# =====================================================

def generate_day_plan(plan_type="general"):

    task_context = get_task_context()

    calendar_context = get_calendar_context()

    memory_context = get_memory_context(
        "recent work internship study tasks calendar meetings deadlines"
    )

    if plan_type == "internship":

        goal = (
            "Create a practical internship-focused day plan."
        )

    elif plan_type == "study":

        goal = (
            "Create a study-focused day plan with breaks."
        )

    else:

        goal = (
            "Create a balanced productive daily schedule."
        )

    prompt = f"""
You are AURON productivity assistant.

{goal}

Generate a realistic day schedule.

Requirements:
- Include time slots
- Consider calendar events first
- Prioritize pending tasks around calendar events
- Add short breaks
- Be realistic
- Keep concise
- Prefer internship/study context when useful

Current Tasks:
{task_context}

Calendar Events:
{calendar_context}

Relevant Memory:
{memory_context}

Return a clean structured schedule.
"""

    messages = [

        {
            "role": "system",
            "content":
                "You are an expert productivity planner."
        },

        {
            "role": "user",
            "content": prompt
        }
    ]

    response = ask_ai(
        messages
    )

    return response