import subprocess


# =====================================================
# BLOCKED COMMANDS
# =====================================================

BLOCKED_COMMANDS = [

    "del",
    "format",
    "shutdown",
    "rd",
    "rmdir",
    "taskkill",
    "reg",
    "powershell remove",
    "remove-item",
    "diskpart"
]


# =====================================================
# SAFE TERMINAL EXECUTION
# =====================================================

def execute_command(command):

    command_lower = command.lower()

    # ==========================================
    # BLOCK DANGEROUS COMMANDS
    # ==========================================

    for blocked in BLOCKED_COMMANDS:

        if blocked in command_lower:

            return (
                "Blocked potentially dangerous command."
            )

    try:

        result = subprocess.check_output(

            command,

            shell=True,

            stderr=subprocess.STDOUT,

            text=True,

            timeout=15
        )

        if not result.strip():

            result = "Command executed successfully."

        return result

    except subprocess.CalledProcessError as e:

        return f"Command failed:\n{e.output}"

    except Exception as e:

        return f"Execution error:\n{e}"