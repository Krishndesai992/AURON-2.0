import ollama


SYSTEM_PROMPT = """
You are AURON 2.0,
an advanced offline AI desktop assistant created by Krish Desai.

Your personality:
- Intelligent
- Professional
- Friendly
- Concise
- Helpful
- Futuristic

Rules:
- Give clean answers
- Avoid unnecessary long paragraphs
- Behave like a premium desktop AI assistant
"""


def ask_ai(memory):

    try:

        response = ollama.chat(
            model="llama3.2:3b",
            messages=memory
        )

        return response["message"]["content"]

    except Exception as e:

        return f"Ollama Error: {e}"