import os

from ai.ollama_client import ask_ai


# =====================================================
# GENERATE CODE
# =====================================================

def generate_code(project_request):

    # ==========================================
    # AI PROMPT
    # ==========================================

    messages = [

        {
            "role": "system",

            "content":

            (
                "You are AURON AI Code Generator.\n"

                "Generate clean Python code only.\n"

                "Do not explain anything.\n"

                "Return only executable code."
            )
        },

        {
            "role": "user",
            "content": project_request
        }
    ]

    generated_code = ask_ai(messages)

    # ==========================================
    # SAVE LOCATION
    # ==========================================

    os.makedirs(
        "generated_code",
        exist_ok=True
    )

    filename = (
        project_request
        .replace(" ", "_")
        .lower()
    )

    filepath = (
        f"generated_code/{filename}.py"
    )

    # ==========================================
    # SAVE FILE
    # ==========================================

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(generated_code)

    return (
        f"Code generated successfully.\n\n"
        f"Saved at:\n{filepath}"
    )