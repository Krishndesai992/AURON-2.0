from ai.ollama_client import ask_ai


# =====================================================
# GENERATE EXECUTION PLAN
# =====================================================

def generate_plan(task):

    planning_prompt = [

        {
            "role": "system",

            "content":

            (
                "You are AURON AI Planner.\n"

                "Break the user's task into clear, "
                "numbered execution steps.\n"

                "Be concise and practical."
            )
        },

        {
            "role": "user",
            "content": task
        }
    ]

    response = ask_ai(planning_prompt)

    return response