import customtkinter as ctk
import threading
import os

from datetime import datetime
from tkinter import messagebox

from core.assisstant import generate_response

from voice.speech_to_text import listen_to_voice
from voice.text_to_speech import speak_text

from voice.wakeword_manager import (
    start_hotkey_listener,
    stop_hotkey_listener
)

from core.memory import clear_memory
from core.meeting_mode import is_meeting_active

from system.monitor import get_system_info
from system.tray_manager import minimize_to_tray

from productivity.focus_mode import get_focus_overlay_data
from productivity.task_manager import load_tasks
from productivity.sticky_notes import add_sticky_note

from gui.overlay import AURONOverlay

from gui.widgets import (
    NotesWindow,
    RemindersWindow
)

import core.config as config
from gui.sticky_note_window import StickyNoteWindow


CHAT_HISTORY_FILE = "data/chat_history/chat_history.txt"


class AURONApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # ==========================================
        # WINDOW
        # ==========================================

        self.title("AURON 2.0")

        self.geometry("1400x850")

        self.minsize(1200, 700)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ==========================================
        # WAKEWORD STATE
        # ==========================================

        self.wakeword_enabled = False

        # ==========================================
        # UI
        # ==========================================

        self.setup_ui()

        # ==========================================
        # OVERLAY
        # ==========================================

        self.overlay = AURONOverlay(self)
        self.overlay.set_status("IDLE")

        # ==========================================
        # LOAD HISTORY
        # ==========================================

        self.load_chat_history()

        # ==========================================
        # SYSTEM MONITOR
        # ==========================================

        self.update_system_monitor()

        # ==========================================
        # OVERLAY LIVE INFO
        # ==========================================

        self.update_overlay_info()

        # ==========================================
        # WINDOW CLOSE
        # ==========================================

        self.protocol(
            "WM_DELETE_WINDOW",
            self.hide_window
        )

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=260,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="AURON 2.0",
            font=("Segoe UI", 30, "bold")
        )

        self.logo_label.pack(
            pady=(35, 40)
        )

        self.mode_label = ctk.CTkLabel(
            self.sidebar,
            text="Mode: General",
            font=("Segoe UI", 15, "bold"),
            text_color="#60a5fa"
        )

        self.mode_label.pack(
            pady=(0, 20)
        )

        self.system_monitor = ctk.CTkTextbox(
            self.sidebar,
            width=220,
            height=140,
            font=("Consolas", 14)
        )

        self.system_monitor.pack(
            padx=15,
            pady=(0, 20)
        )

        self.new_chat_button = ctk.CTkButton(
            self.sidebar,
            text="New Chat",
            height=42,
            command=self.new_chat
        )

        self.new_chat_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        self.clear_button = ctk.CTkButton(
            self.sidebar,
            text="Clear History",
            height=42,
            fg_color="#b91c1c",
            hover_color="#991b1b",
            command=self.clear_chat_history
        )

        self.clear_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        self.memory_button = ctk.CTkButton(
            self.sidebar,
            text="Clear Memory",
            height=42,
            command=self.clear_ai_memory
        )

        self.memory_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        self.notes_button = ctk.CTkButton(
            self.sidebar,
            text="View Notes",
            height=42,
            command=self.open_notes
        )

        self.notes_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        self.sticky_note_button = ctk.CTkButton(
            self.sidebar,
            text="Create Sticky Note",
            height=42,
            command=self.open_sticky_note_creator
        )

        self.sticky_note_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        self.open_history_button = ctk.CTkButton(
            self.sidebar,
            text="Open History",
            height=42,
            command=self.open_history
        )

        self.open_history_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        self.reminders_button = ctk.CTkButton(
            self.sidebar,
            text="View Reminders",
            height=42,
            command=self.open_reminders
        )

        self.reminders_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        self.wakeword_button = ctk.CTkButton(
            self.sidebar,
            text="Enable Wake Word",
            height=42,
            command=self.toggle_wakeword
        )

        self.wakeword_button.pack(
            padx=15,
            pady=8,
            fill="x"
        )

        self.theme_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Dark", "Light"],
            command=self.change_theme
        )

        self.theme_menu.pack(
            padx=15,
            pady=20,
            fill="x"
        )

        # ==========================================
        # MAIN FRAME
        # ==========================================

        self.main_frame = ctk.CTkFrame(self)

        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.chat_display = ctk.CTkTextbox(
            self.main_frame,
            font=("Consolas", 15),
            wrap="word"
        )

        self.chat_display.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        self.input_frame = ctk.CTkFrame(
            self.main_frame,
            height=90
        )

        self.input_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.input_box = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ask AURON anything...",
            height=50,
            font=("Segoe UI", 15)
        )

        self.input_box.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 10),
            pady=15
        )

        self.input_box.bind(
            "<Return>",
            self.enter_pressed
        )

        self.mic_button = ctk.CTkButton(
            self.input_frame,
            text="🎤",
            width=60,
            height=50,
            font=("Segoe UI", 20),
            command=self.voice_input
        )

        self.mic_button.pack(
            side="left",
            padx=5,
            pady=15
        )

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Ask AURON",
            width=160,
            height=50,
            font=("Segoe UI", 15, "bold"),
            command=self.send_message
        )

        self.send_button.pack(
            side="right",
            padx=(10, 15),
            pady=15
        )

    # =====================================================
    # SEND MESSAGE
    # =====================================================

    def send_message(self):

        user_message = self.input_box.get().strip()

        if not user_message:
            return

        self.display_user_message(
            user_message
        )

        self.input_box.delete(
            0,
            "end"
        )

        threading.Thread(
            target=self.process_ai_response,
            args=(user_message,),
            daemon=True
        ).start()

    # =====================================================
    # AI RESPONSE
    # =====================================================

    def process_ai_response(self, user_message):

        self.overlay.set_status(
            "THINKING"
        )

        self.chat_display.insert(
            "end",
            "\nAURON: Thinking...\n\n"
        )

        self.chat_display.see(
            "end"
        )

        response = generate_response(
            user_message
        )

        self.mode_label.configure(
            text=f"Mode: {config.CURRENT_MODE}"
        )

        self.chat_display.delete(
            "end-3l",
            "end"
        )

        current_time = datetime.now().strftime(
            "%H:%M"
        )

        ai_text = (
            f"[{current_time}] "
            f"AURON: {response}\n\n"
        )

        self.chat_display.insert(
            "end",
            ai_text
        )

        self.save_chat_message(
            ai_text
        )

        self.chat_display.see(
            "end"
        )

        self.overlay.set_status(
            "SPEAKING"
        )

        speak_text(response)

        self.overlay.set_status(
            "IDLE"
        )

    # =====================================================
    # USER MESSAGE
    # =====================================================

    def display_user_message(self, message):

        current_time = datetime.now().strftime(
            "%H:%M"
        )

        user_text = (
            f"[{current_time}] "
            f"You: {message}\n\n"
        )

        self.chat_display.insert(
            "end",
            user_text
        )

        self.save_chat_message(
            user_text
        )

        self.chat_display.see(
            "end"
        )

    # =====================================================
    # VOICE INPUT
    # =====================================================

    def voice_input(self):

        self.overlay.set_status(
            "LISTENING"
        )

        self.chat_display.insert(
            "end",
            "\nAURON: Listening...\n\n"
        )

        self.chat_display.see(
            "end"
        )

        threading.Thread(
            target=self.process_voice,
            daemon=True
        ).start()

    def process_voice(self):

        voice_text = listen_to_voice()

        if voice_text:

            self.input_box.delete(
                0,
                "end"
            )

            self.input_box.insert(
                0,
                voice_text
            )

            self.send_message()

        else:

            self.overlay.set_status(
                "IDLE"
            )

    # =====================================================
    # WAKEWORD / HOTKEY
    # =====================================================

    def toggle_wakeword(self):

        if not self.wakeword_enabled:

            start_hotkey_listener(
                self.voice_input
            )

            self.wakeword_enabled = True

            self.wakeword_button.configure(
                text="Disable Wake Word",
                fg_color="green"
            )

            self.chat_display.insert(
                "end",
                "\nAURON: Wake-word engine activated.\n\n"
            )

        else:

            stop_hotkey_listener()

            self.wakeword_enabled = False

            self.wakeword_button.configure(
                text="Enable Wake Word",
                fg_color="#1f6aa5"
            )

            self.chat_display.insert(
                "end",
                "\nAURON: Wake-word engine disabled.\n\n"
            )

    # =====================================================
    # STORAGE
    # =====================================================

    def save_chat_message(self, message):

        os.makedirs(
            "data/chat_history",
            exist_ok=True
        )

        with open(
            CHAT_HISTORY_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(message)

    def load_chat_history(self):

        if os.path.exists(
            CHAT_HISTORY_FILE
        ):

            with open(
                CHAT_HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                history = file.read()

                self.chat_display.insert(
                    "end",
                    history
                )

        else:

            self.chat_display.insert(
                "end",
                "AURON: Welcome back, Krish.\n\n"
            )

    # =====================================================
    # BUTTON ACTIONS
    # =====================================================

    def new_chat(self):

        self.chat_display.delete(
            "1.0",
            "end"
        )

        self.chat_display.insert(
            "end",
            "AURON: New conversation started.\n\n"
        )

    def clear_chat_history(self):

        confirm = messagebox.askyesno(
            "Confirm",
            "Delete all chat history?"
        )

        if confirm:

            if os.path.exists(
                CHAT_HISTORY_FILE
            ):

                os.remove(
                    CHAT_HISTORY_FILE
                )

            self.chat_display.delete(
                "1.0",
                "end"
            )

            self.chat_display.insert(
                "end",
                "AURON: Chat history cleared.\n\n"
            )

    def clear_ai_memory(self):

        clear_memory()

        self.chat_display.insert(
            "end",
            "\nAURON: Memory cleared.\n\n"
        )

    def open_notes(self):

        NotesWindow(self)

    def open_reminders(self):

        RemindersWindow(self)

    def open_history(self):

        if os.path.exists(
            CHAT_HISTORY_FILE
        ):

            os.startfile(
                CHAT_HISTORY_FILE
            )

        else:

            messagebox.showinfo(
                "Info",
                "No chat history found."
            )

    # =====================================================
    # CREATE STICKY NOTE
    # =====================================================

    def open_sticky_note_creator(self):

        sticky_window = ctk.CTkToplevel(self)

        sticky_window.title("Create Sticky Note")

        sticky_window.geometry("420x320")

        sticky_window.resizable(
            False,
            False
        )

        sticky_window.attributes(
            "-topmost",
            True
        )

        title_label = ctk.CTkLabel(
            sticky_window,
            text="New Sticky Note",
            font=("Segoe UI", 22, "bold"),
            text_color="#60a5fa"
        )

        title_label.pack(
            pady=(25, 10)
        )

        note_box = ctk.CTkTextbox(
            sticky_window,
            width=340,
            height=140,
            font=("Segoe UI", 14),
            wrap="word"
        )

        note_box.pack(
            pady=10
        )

        def save_sticky_note_action():

            note_text = note_box.get(
                "1.0",
                "end"
            ).strip()

            if not note_text:

                messagebox.showerror(
                    "Error",
                    "Sticky note cannot be empty."
                )

                return

            result = add_sticky_note(
                note_text
            )

            StickyNoteWindow(
                self,
                note_text
            )

            current_time = datetime.now().strftime(
                "%H:%M"
            )

            ai_text = (
                f"[{current_time}] "
                f"AURON: {result}\n\n"
            )

            self.chat_display.insert(
                "end",
                ai_text
            )

            self.save_chat_message(
                ai_text
            )

            self.chat_display.see(
                "end"
            )

            sticky_window.destroy()

        save_button = ctk.CTkButton(
            sticky_window,
            text="Save Sticky Note",
            height=42,
            width=220,
            command=save_sticky_note_action
        )

        save_button.pack(
            pady=15
        )

    # =====================================================
    # THEME / ENTER
    # =====================================================

    def change_theme(self, mode):

        ctk.set_appearance_mode(
            mode.lower()
        )

    def enter_pressed(
        self,
        event
    ):

        self.send_message()

    # =====================================================
    # SYSTEM MONITOR
    # =====================================================

    def update_system_monitor(self):

        info = get_system_info()

        self.system_monitor.delete(
            "1.0",
            "end"
        )

        text = (
            f"CPU Usage : {info['cpu']}%\n\n"
            f"RAM Usage : {info['ram']}%\n\n"
            f"Battery : {info['battery']}%\n\n"
            f"Charging : {info['charging']}"
        )

        self.system_monitor.insert(
            "end",
            text
        )

        self.after(
            5000,
            self.update_system_monitor
        )

    # =====================================================
    # OVERLAY INFO UPDATE
    # =====================================================

    def update_overlay_info(self):

        try:

            self.overlay.set_ai_mode(
                config.CURRENT_MODE
            )

            focus_data = get_focus_overlay_data()

            self.overlay.set_focus_timer(
                focus_data["display"],
                focus_data["active"]
            )

            self.overlay.set_meeting_status(
                is_meeting_active()
            )

            tasks = load_tasks()

            active_tasks = len(
                [
                    task
                    for task in tasks
                    if not task.get(
                        "completed",
                        False
                    )
                ]
            )

            self.overlay.set_task_count(
                active_tasks
            )

        except Exception as e:

            print(
                "Overlay Update Error:",
                e
            )

        self.after(
            1000,
            self.update_overlay_info
        )

    # =====================================================
    # TRAY
    # =====================================================

    def hide_window(self):

        self.withdraw()

        minimize_to_tray(self)