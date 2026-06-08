from ai.ollama_client import ask_ai

from ai.prompts import (
    GENERAL_PROMPT,
    CODING_PROMPT,
    STUDY_PROMPT,
    SYSTEM_PROMPT
)

from system.system_controls import (
    process_system_command
)

from productivity.notes import (
    save_note
)

from productivity.reminders import (
    save_reminder
)

from productivity.task_manager import (
    add_task,
    show_tasks,
    complete_task,
    delete_task,
    get_task_context
)

from productivity.day_planner import (
    generate_day_plan
)

from productivity.day_summary import (
    generate_day_summary
)

from productivity.focus_mode import (
    start_focus_mode,
    stop_focus_mode,
    get_focus_status,
    show_focus_history
)

from productivity.task_prioritizer import (
    prioritize_tasks
)

from productivity.standup_generator import (
    generate_standup_report
)

from core.memory import (
    add_message,
    load_memory,
    clear_memory
)

from core.vector_memory import (
    get_memory_context
)

from core.agent import (
    execute_agent_task
)

from core.planner import (
    generate_plan
)

from core.code_generator import (
    generate_code
)

from core.meeting_commands import (
    process_meeting_command,
    handle_meeting_note
)

import core.config as config

from productivity.email_assistant import (
    generate_email_draft,
    generate_leave_email,
    generate_progress_email,
    generate_meeting_followup
)

from productivity.email_commands import (
    process_email_command
)

from productivity.calendar_commands import (
    process_calendar_command
)


from productivity.sticky_notes import (
    add_sticky_note,
    show_sticky_notes,
    delete_sticky_note,
    clear_sticky_notes,
    get_sticky_notes_context
)
# =====================================================
# GET MODE PROMPT
# =====================================================

def get_mode_prompt():

    if config.CURRENT_MODE == "Coding":
        return CODING_PROMPT

    elif config.CURRENT_MODE == "Study":
        return STUDY_PROMPT

    elif config.CURRENT_MODE == "System":
        return SYSTEM_PROMPT

    return GENERAL_PROMPT


# =====================================================
# GENERATE RESPONSE
# =====================================================

def generate_response(user_message):

    user_message_lower = (
        user_message.lower()
    )

    # =====================================================
    # MEETING MODE COMMANDS
    # =====================================================

    meeting_response = (
        process_meeting_command(
            user_message
        )
    )

    if meeting_response:
        return meeting_response

    # =====================================================
    # AUTO MEETING NOTES
    # =====================================================

    handle_meeting_note(
        user_message
    )

    # =====================================================
    # EMAIL ASSISTANT
    # =====================================================

    email_response = process_email_command(
        user_message
    )

    if email_response:
        return email_response
    
    # =====================================================
    # CALENDAR ASSISTANT
    # =====================================================

    calendar_response = process_calendar_command(
        user_message
    )

    if calendar_response:
        return calendar_response
    
    
    # =====================================================
    # DAILY WORK SUMMARY
    # =====================================================

    if (
        user_message_lower == "what did i work on today"
        or user_message_lower == "summarize my day"
        or user_message_lower == "internship summary"
        or user_message_lower == "daily summary"
    ):

        return generate_day_summary()

    # =====================================================
    # DAILY STANDUP GENERATOR
    # =====================================================

    if (
        user_message_lower == "generate standup report"
        or user_message_lower == "daily standup"
        or user_message_lower == "standup update"
        or user_message_lower == "generate daily standup"
        or user_message_lower == "create standup report"
    ):

        return generate_standup_report()
    
    # =====================================================
    # EMAIL ASSISTANT
    # =====================================================

    if user_message_lower.startswith(
        "draft email"
    ):

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

    if (
        user_message_lower
        == "leave email"
    ):

        return generate_leave_email()

    if (
        user_message_lower
        == "progress email"
    ):

        return generate_progress_email()

    if (
        user_message_lower
        == "meeting followup email"
    ):

        return generate_meeting_followup()

    # =====================================================
    # TASK PRIORITIZATION ENGINE
    # =====================================================

    if (
        user_message_lower == "what should i work on next"
        or user_message_lower == "what should i do next"
        or user_message_lower == "prioritize my tasks"
        or user_message_lower == "rank my tasks"
    ):

        return prioritize_tasks()

    # =====================================================
    # FOCUS MODE
    # =====================================================

    if (
        user_message_lower == "start focus mode"
        or user_message_lower == "start focus"
    ):

        return start_focus_mode(
            "Focus"
        )

    if (
        user_message_lower == "start pomodoro"
        or user_message_lower == "start pomodoro mode"
    ):

        return start_focus_mode(
            "Pomodoro"
        )

    if (
        user_message_lower == "stop focus mode"
        or user_message_lower == "stop focus"
        or user_message_lower == "stop pomodoro"
    ):

        return stop_focus_mode()

    if (
        user_message_lower == "focus status"
        or user_message_lower == "show focus status"
        or user_message_lower == "pomodoro status"
    ):

        return get_focus_status()

    if (
        user_message_lower == "focus history"
        or user_message_lower == "show focus history"
    ):

        return show_focus_history()

    # =====================================================
    # SMART DAY PLANNER
    # =====================================================

    if (
        user_message_lower
        == "plan my day"
    ):

        return generate_day_plan(
            "general"
        )

    if (
        user_message_lower
        == "plan my internship day"
    ):

        return generate_day_plan(
            "internship"
        )

    if (
        user_message_lower
        == "plan my study day"
    ):

        return generate_day_plan(
            "study"
        )

        # =====================================================
    # STICKY NOTES
    # =====================================================

    if user_message_lower.startswith("add sticky note"):

        note_text = user_message.replace(
            "add sticky note",
            ""
        ).strip()

        return add_sticky_note(note_text)

    if (
        user_message_lower == "show sticky notes"
        or user_message_lower == "sticky notes"
    ):

        return show_sticky_notes()

    if user_message_lower.startswith("delete sticky note"):

        note_keyword = user_message.replace(
            "delete sticky note",
            ""
        ).strip()

        return delete_sticky_note(note_keyword)

    if user_message_lower == "clear sticky notes":

        return clear_sticky_notes()
    

    # =====================================================
    # TASK MANAGER
    # =====================================================

    if user_message_lower.startswith(
        "add task"
    ):

        task_text = (
            user_message[8:]
            .strip()
        )

        return add_task(
            task_text
        )

    if (
        user_message_lower
        == "show tasks"
    ):

        return show_tasks()

    if user_message_lower.startswith(
        "mark task complete"
    ):

        task_name = (
            user_message
            .replace(
                "mark task complete",
                ""
            )
            .strip()
        )

        return complete_task(
            task_name
        )

    if user_message_lower.startswith(
        "delete task"
    ):

        task_name = (
            user_message
            .replace(
                "delete task",
                ""
            )
            .strip()
        )

        return delete_task(
            task_name
        )

    # =====================================================
    # CODE GENERATION
    # =====================================================

    if user_message_lower.startswith(
        "generate code"
    ):

        project_request = (
            user_message.replace(
                "generate code",
                ""
            ).strip()
        )

        if project_request:

            return generate_code(
                project_request
            )

        return (
            "Please provide a "
            "project description."
        )

    # =====================================================
    # AI PLANNER
    # =====================================================

    if user_message_lower.startswith(
        "plan "
    ):

        task = (
            user_message[5:]
            .strip()
        )

        return generate_plan(
            task
        )

    # =====================================================
    # AGENT MODE
    # =====================================================

    if user_message_lower.startswith(
        "agent mode"
    ):

        task = (
            user_message_lower
            .replace(
                "agent mode",
                ""
            )
            .strip()
        )

        return execute_agent_task(
            task
        )

    # =====================================================
    # MODE SWITCHING
    # =====================================================

    if (
        user_message_lower
        == "switch to coding mode"
    ):

        config.CURRENT_MODE = (
            "Coding"
        )

        return (
            "AURON switched "
            "to Coding Mode."
        )

    if (
        user_message_lower
        == "switch to study mode"
    ):

        config.CURRENT_MODE = (
            "Study"
        )

        return (
            "AURON switched "
            "to Study Mode."
        )

    if (
        user_message_lower
        == "switch to system mode"
    ):

        config.CURRENT_MODE = (
            "System"
        )

        return (
            "AURON switched to "
            "System Admin Mode."
        )

    if (
        user_message_lower
        == "switch to general mode"
    ):

        config.CURRENT_MODE = (
            "General"
        )

        return (
            "AURON switched "
            "to General Mode."
        )

    # =====================================================
    # CLEAR MEMORY
    # =====================================================

    if (
        user_message_lower
        == "clear memory"
    ):

        clear_memory()

        return (
            "Conversation memory "
            "cleared."
        )

    # =====================================================
    # SYSTEM COMMANDS
    # =====================================================

    system_response = (
        process_system_command(
            user_message_lower
        )
    )

    if system_response:
        return system_response

    # =====================================================
    # SAVE NOTE
    # =====================================================

    if user_message_lower.startswith(
        "save note"
    ):

        note_text = (
            user_message[9:]
            .strip()
        )

        if note_text:

            filepath = save_note(
                note_text
            )

            return (
                "Note saved "
                "successfully.\n"
                f"{filepath}"
            )

        return (
            "Please provide "
            "note content."
        )

    # =====================================================
    # SAVE REMINDER
    # =====================================================

    if user_message_lower.startswith(
        "remind me"
    ):

        reminder_text = (
            user_message[9:]
            .strip()
        )

        if reminder_text:

            save_reminder(
                reminder_text
            )

            return (
                "Reminder saved "
                "successfully."
            )

        return (
            "Please provide "
            "reminder text."
        )

    # =====================================================
    # MEMORY
    # =====================================================

    add_message(
        "user",
        user_message
    )

    memory = load_memory()

    memory_context = (
        get_memory_context(
            user_message
        )
    )

    task_context = (
        get_task_context()
    )

    sticky_context = (
        get_sticky_notes_context()
    )
    final_memory = [

        {
            "role": "system",
            "content":
                get_mode_prompt()
        }

    ]

    # =====================================================
    # LONG TERM MEMORY
    # =====================================================

    if memory_context:

        final_memory.append({

            "role": "system",

            "content":
                (
                    "Relevant memory:\n\n"
                    f"{memory_context}"
                )
        })

    # =====================================================
    # TASK CONTEXT
    # =====================================================

    if task_context:

        final_memory.append({

            "role": "system",

            "content":
                task_context
        })
    
    
    if sticky_context:

        final_memory.append({

            "role": "system",

            "content":
                sticky_context
        })

    final_memory += memory

    
    # =====================================================
    # AI RESPONSE
    # =====================================================

    ai_response = ask_ai(
        final_memory
    )

    add_message(
        "assistant",
        ai_response
    )

    return ai_response