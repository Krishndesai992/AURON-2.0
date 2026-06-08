import json
import os
from datetime import datetime


TASK_FILE = "data/tasks.json"


# =====================================================
# LOAD TASKS
# =====================================================

def load_tasks():

    if not os.path.exists(
        TASK_FILE
    ):

        return []

    try:

        with open(

            TASK_FILE,
            "r",
            encoding="utf-8"

        ) as file:

            return json.load(
                file
            )

    except:

        return []


# =====================================================
# SAVE TASKS
# =====================================================

def save_tasks(tasks):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(

        TASK_FILE,
        "w",
        encoding="utf-8"

    ) as file:

        json.dump(

            tasks,
            file,
            indent=4

        )


# =====================================================
# ADD TASK
# =====================================================

def add_task(task_text):

    task_text = (
        task_text.strip()
    )

    if not task_text:

        return (
            "Please provide "
            "a task."
        )

    tasks = load_tasks()

    new_task = {

        "task": task_text,
        "completed": False,
        "created_at":
            str(
                datetime.now()
            )
    }

    tasks.append(
        new_task
    )

    save_tasks(
        tasks
    )

    return (
        f"Task added:\n"
        f"{task_text}"
    )


# =====================================================
# SHOW TASKS
# =====================================================

def show_tasks():

    tasks = load_tasks()

    if not tasks:

        return (
            "No tasks found."
        )

    output = (
        "Your Tasks:\n\n"
    )

    for i, task in enumerate(
        tasks,
        start=1
    ):

        status = (
            "✅"
            if task[
                "completed"
            ]
            else "❌"
        )

        output += (

            f"{i}. "
            f"{status} "
            f"{task['task']}\n"

        )

    return output


# =====================================================
# COMPLETE TASK
# =====================================================

def complete_task(task_name):

    tasks = load_tasks()

    found = False

    for task in tasks:

        if (

            task_name.lower()
            in task["task"]
            .lower()

        ):

            task[
                "completed"
            ] = True

            found = True

    save_tasks(
        tasks
    )

    if found:

        return (
            f"Completed:\n"
            f"{task_name}"
        )

    return (
        "Task not found."
    )


# =====================================================
# DELETE TASK
# =====================================================

def delete_task(task_name):

    tasks = load_tasks()

    updated_tasks = [

        task
        for task in tasks

        if task_name.lower()
        not in task["task"]
        .lower()

    ]

    if len(
        updated_tasks
    ) == len(tasks):

        return (
            "Task not found."
        )

    save_tasks(
        updated_tasks
    )

    return (
        f"Deleted:\n"
        f"{task_name}"
    )


# =====================================================
# GET TASK CONTEXT
# =====================================================

def get_task_context():

    tasks = load_tasks()

    if not tasks:
        return ""

    context = (
        "Current Tasks:\n"
    )

    for task in tasks:

        status = (
            "Completed"
            if task[
                "completed"
            ]
            else "Pending"
        )

        context += (

            f"- "
            f"{task['task']} "
            f"({status})\n"

        )

    return context