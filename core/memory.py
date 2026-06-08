import json
import os

from core.vector_memory import (
    add_memory,
    clear_vector_memory
)


MEMORY_FILE = "data/memory.json"

MAX_MEMORY_MESSAGES = 20


# =====================================================
# LOAD MEMORY
# =====================================================

def load_memory():

    if not os.path.exists(
        MEMORY_FILE
    ):

        return []

    try:

        with open(

            MEMORY_FILE,
            "r",
            encoding="utf-8"

        ) as file:

            return json.load(
                file
            )

    except:

        return []


# =====================================================
# SAVE MEMORY
# =====================================================

def save_memory(memory):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(

        MEMORY_FILE,
        "w",
        encoding="utf-8"

    ) as file:

        json.dump(

            memory,
            file,
            indent=4

        )


# =====================================================
# ADD MESSAGE
# =====================================================

def add_message(
    role,
    content
):

    memory = load_memory()

    memory.append({

        "role": role,
        "content": content

    })

    # ==========================================
    # LIMIT MEMORY SIZE
    # ==========================================

    memory = memory[
        -MAX_MEMORY_MESSAGES:
    ]

    save_memory(
        memory
    )

    # ==========================================
    # VECTOR MEMORY
    # ==========================================

    if role == "user":

        try:

            add_memory(
                content
            )

        except Exception as e:

            print(
                "Vector Memory Error:",
                e
            )


# =====================================================
# CLEAR MEMORY
# =====================================================

def clear_memory():

    save_memory([])

    try:

        clear_vector_memory()

    except Exception as e:

        print(
            "Vector Memory Clear Error:",
            e
        )