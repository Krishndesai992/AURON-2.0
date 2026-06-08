import customtkinter as ctk
import os


# =====================================================
# NOTES WINDOW
# =====================================================

class NotesWindow(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("AURON Notes")
        self.geometry("700x500")

        self.notes_box = ctk.CTkTextbox(
            self,
            font=("Consolas", 14)
        )

        self.notes_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_notes()

    def load_notes(self):

        notes_folder = "data/notes"

        os.makedirs(
            notes_folder,
            exist_ok=True
        )

        all_notes = ""

        for filename in os.listdir(notes_folder):

            filepath = os.path.join(
                notes_folder,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

                all_notes += (
                    f"\n{'='*60}\n"
                    f"{filename}\n"
                    f"{'='*60}\n\n"
                    f"{content}\n"
                )

        if not all_notes:

            all_notes = "No notes found."

        self.notes_box.insert(
            "end",
            all_notes
        )


# =====================================================
# REMINDERS WINDOW
# =====================================================

class RemindersWindow(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("AURON Reminders")
        self.geometry("700x500")

        self.reminders_box = ctk.CTkTextbox(
            self,
            font=("Consolas", 14)
        )

        self.reminders_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_reminders()

    def load_reminders(self):

        reminders_folder = "data/reminders"

        os.makedirs(
            reminders_folder,
            exist_ok=True
        )

        all_reminders = ""

        for filename in os.listdir(reminders_folder):

            filepath = os.path.join(
                reminders_folder,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

                all_reminders += (
                    f"\n{'='*60}\n"
                    f"{filename}\n"
                    f"{'='*60}\n\n"
                    f"{content}\n"
                )

        if not all_reminders:

            all_reminders = "No reminders found."

        self.reminders_box.insert(
            "end",
            all_reminders
        )