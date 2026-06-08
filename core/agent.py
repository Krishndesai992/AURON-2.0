import os

from system.app_launcher import open_application


# =====================================================
# AGENT TASK EXECUTION
# =====================================================

def execute_agent_task(task):

    task = task.lower()

    # =====================================================
    # PYTHON PROJECT CREATOR
    # =====================================================

    if "python project" in task:

        project_path = r"D:\Krish Things\AI_Project"

        try:

            # ======================================
            # CREATE PROJECT FOLDER
            # ======================================

            os.makedirs(
                project_path,
                exist_ok=True
            )

            # ======================================
            # CREATE MAIN FILE
            # ======================================

            main_file = os.path.join(
                project_path,
                "main.py"
            )

            with open(
                main_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "# AI Project\n\n"
                    "print('Hello from AURON Agent')"
                )

            # ======================================
            # OPEN VSCODE
            # ======================================

            open_application("vscode")

            return (
                "Agent completed task.\n\n"
                "Created Python project:\n"
                f"{project_path}"
            )

        except Exception as e:

            return f"Agent execution failed:\n{e}"

    # =====================================================
    # UNKNOWN TASK
    # =====================================================

    return (
        "Agent does not yet know "
        "how to perform this task."
    )