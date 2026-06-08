import customtkinter as ctk
import threading

from tkinter import messagebox

from security.auth_manager import (
    auth_exists,
    setup_passkey,
    verify_passkey
)

from security.voice_auth import (
    voice_auth_exists,
    setup_voice_phrase,
    verify_voice_phrase
)

from voice.speech_to_text import (
    listen_to_voice
)


class LoginWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.authenticated = False

        self.title("AURON Security")

        self.geometry("560x480")

        self.resizable(
            False,
            False
        )

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.setup_ui()

    # =====================================================
    # UI SETUP
    # =====================================================

    def setup_ui(self):

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=25
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="AURON SECURITY",
            font=("Segoe UI", 28, "bold"),
            text_color="#60a5fa"
        )

        self.title_label.pack(
            pady=(35, 10)
        )

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Authenticate to continue",
            font=("Segoe UI", 15),
            text_color="#cbd5e1"
        )

        self.subtitle_label.pack(
            pady=(0, 25)
        )

        if auth_exists():

            self.show_login_ui()

        else:

            self.show_setup_ui()

    # =====================================================
    # CLEAR FRAME
    # =====================================================

    def clear_frame(self):

        for widget in self.main_frame.winfo_children():

            if widget not in [
                self.title_label,
                self.subtitle_label
            ]:

                widget.destroy()

    # =====================================================
    # PASSKEY SETUP UI
    # =====================================================

    def show_setup_ui(self):

        self.clear_frame()

        self.subtitle_label.configure(
            text="Create your AURON passkey"
        )

        self.passkey_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Create PIN / Password",
            show="*",
            height=45,
            width=340,
            font=("Segoe UI", 15)
        )

        self.passkey_entry.pack(
            pady=10
        )

        self.confirm_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Confirm PIN / Password",
            show="*",
            height=45,
            width=340,
            font=("Segoe UI", 15)
        )

        self.confirm_entry.pack(
            pady=10
        )

        self.setup_button = ctk.CTkButton(
            self.main_frame,
            text="Setup Passkey",
            height=45,
            width=240,
            command=self.setup_passkey_action
        )

        self.setup_button.pack(
            pady=25
        )

    # =====================================================
    # LOGIN UI
    # =====================================================

    def show_login_ui(self):

        self.clear_frame()

        self.subtitle_label.configure(
            text="Unlock AURON"
        )

        self.passkey_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter Passkey",
            show="*",
            height=45,
            width=340,
            font=("Segoe UI", 15)
        )

        self.passkey_entry.pack(
            pady=12
        )

        self.passkey_entry.bind(
            "<Return>",
            lambda event: self.login_action()
        )

        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="Unlock with Passkey",
            height=45,
            width=260,
            command=self.login_action
        )

        self.login_button.pack(
            pady=8
        )

        self.voice_unlock_button = ctk.CTkButton(
            self.main_frame,
            text="🎙 Unlock with Voice Phrase",
            height=45,
            width=260,
            command=self.voice_unlock_action
        )

        self.voice_unlock_button.pack(
            pady=8
        )

        self.voice_setup_button = ctk.CTkButton(
            self.main_frame,
            text="Set / Change Voice Phrase",
            height=42,
            width=260,
            fg_color="#334155",
            hover_color="#475569",
            command=self.show_voice_setup_ui
        )

        self.voice_setup_button.pack(
            pady=8
        )

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text=(
                "Voice phrase configured"
                if voice_auth_exists()
                else "Voice phrase not configured"
            ),
            font=("Segoe UI", 13),
            text_color="#94a3b8"
        )

        self.status_label.pack(
            pady=(10, 0)
        )

    # =====================================================
    # VOICE SETUP UI
    # =====================================================

    def show_voice_setup_ui(self):

        self.clear_frame()

        self.subtitle_label.configure(
            text="Set your voice unlock phrase"
        )

        self.voice_phrase_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Example: AURON authorize Krish",
            height=45,
            width=360,
            font=("Segoe UI", 15)
        )

        self.voice_phrase_entry.pack(
            pady=12
        )

        self.voice_phrase_confirm_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Confirm voice phrase",
            height=45,
            width=360,
            font=("Segoe UI", 15)
        )

        self.voice_phrase_confirm_entry.pack(
            pady=12
        )

        self.save_voice_button = ctk.CTkButton(
            self.main_frame,
            text="Save Voice Phrase",
            height=45,
            width=260,
            command=self.save_voice_phrase_action
        )

        self.save_voice_button.pack(
            pady=12
        )

        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="Back to Login",
            height=42,
            width=260,
            fg_color="#334155",
            hover_color="#475569",
            command=self.show_login_ui
        )

        self.back_button.pack(
            pady=8
        )

    # =====================================================
    # PASSKEY SETUP ACTION
    # =====================================================

    def setup_passkey_action(self):

        passkey = self.passkey_entry.get().strip()

        confirm = self.confirm_entry.get().strip()

        if passkey != confirm:

            messagebox.showerror(
                "Error",
                "Passkeys do not match."
            )

            return

        success, message = setup_passkey(
            passkey
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.show_login_ui()

        else:

            messagebox.showerror(
                "Error",
                message
            )

    # =====================================================
    # PASSKEY LOGIN ACTION
    # =====================================================

    def login_action(self):

        passkey = self.passkey_entry.get().strip()

        success, message = verify_passkey(
            passkey
        )

        if success:

            self.authenticated = True

            self.destroy()

        else:

            messagebox.showerror(
                "Access Denied",
                message
            )

    # =====================================================
    # SAVE VOICE PHRASE ACTION
    # =====================================================

    def save_voice_phrase_action(self):

        phrase = self.voice_phrase_entry.get().strip()

        confirm = self.voice_phrase_confirm_entry.get().strip()

        if phrase != confirm:

            messagebox.showerror(
                "Error",
                "Voice phrases do not match."
            )

            return

        success, message = setup_voice_phrase(
            phrase
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.show_login_ui()

        else:

            messagebox.showerror(
                "Error",
                message
            )

    # =====================================================
    # VOICE UNLOCK ACTION
    # =====================================================

    def voice_unlock_action(self):

        if not voice_auth_exists():

            messagebox.showerror(
                "Voice Unlock",
                "Voice phrase is not configured."
            )

            return

        self.voice_unlock_button.configure(
            text="Listening...",
            state="disabled"
        )

        threading.Thread(
            target=self.process_voice_unlock,
            daemon=True
        ).start()

    # =====================================================
    # PROCESS VOICE UNLOCK
    # =====================================================

    def process_voice_unlock(self):

        spoken_text = listen_to_voice()

        if not spoken_text:

            self.after(
                0,
                lambda: self.voice_unlock_button.configure(
                    text="🎙 Unlock with Voice Phrase",
                    state="normal"
                )
            )

            self.after(
                0,
                lambda: messagebox.showerror(
                    "Voice Unlock Failed",
                    "Could not detect voice phrase."
                )
            )

            return

        success, message = verify_voice_phrase(
            spoken_text
        )

        if success:

            self.authenticated = True

            self.after(
                0,
                self.destroy
            )

        else:

            self.after(
                0,
                lambda: self.voice_unlock_button.configure(
                    text="🎙 Unlock with Voice Phrase",
                    state="normal"
                )
            )

            self.after(
                0,
                lambda: messagebox.showerror(
                    "Access Denied",
                    message
                )
            )