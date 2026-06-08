import customtkinter as ctk


class StickyNoteWindow(ctk.CTkToplevel):

    def __init__(self, parent, note_text):

        super().__init__(parent)

        self.parent = parent
        self.note_text = note_text

        self.drag_start_x = 0
        self.drag_start_y = 0
        self.window_start_x = 0
        self.window_start_y = 0

        self.title("Sticky Note")

        self.geometry("260x220+900+200")

        self.overrideredirect(True)

        self.attributes(
            "-topmost",
            True
        )

        self.configure(
            fg_color="#facc15"
        )

        self.note_frame = ctk.CTkFrame(
            self,
            fg_color="#facc15",
            corner_radius=12,
            border_width=2,
            border_color="#ca8a04"
        )

        self.note_frame.pack(
            fill="both",
            expand=True,
            padx=3,
            pady=3
        )

        self.header_frame = ctk.CTkFrame(
            self.note_frame,
            fg_color="#eab308",
            height=34,
            corner_radius=10
        )

        self.header_frame.pack(
            fill="x",
            padx=6,
            pady=(6, 4)
        )

        self.header_frame.pack_propagate(
            False
        )

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Sticky Note",
            font=("Segoe UI", 13, "bold"),
            text_color="#1f2937"
        )

        self.title_label.pack(
            side="left",
            padx=10
        )

        self.close_button = ctk.CTkButton(
            self.header_frame,
            text="×",
            width=28,
            height=24,
            fg_color="#dc2626",
            hover_color="#991b1b",
            text_color="white",
            font=("Segoe UI", 16, "bold"),
            command=self.destroy
        )

        self.close_button.pack(
            side="right",
            padx=6
        )

        self.note_label = ctk.CTkLabel(
            self.note_frame,
            text=self.note_text,
            font=("Segoe UI", 15),
            text_color="#111827",
            wraplength=220,
            justify="left"
        )

        self.note_label.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(8, 14)
        )

        draggable_widgets = [
            self,
            self.note_frame,
            self.header_frame,
            self.title_label,
            self.note_label
        ]

        for widget in draggable_widgets:

            widget.bind(
                "<Button-1>",
                self.start_move
            )

            widget.bind(
                "<B1-Motion>",
                self.do_move
            )

    # =====================================================
    # DRAG START
    # =====================================================

    def start_move(self, event):

        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root

        self.window_start_x = self.winfo_x()
        self.window_start_y = self.winfo_y()

    # =====================================================
    # DRAG MOVE
    # =====================================================

    def do_move(self, event):

        delta_x = event.x_root - self.drag_start_x
        delta_y = event.y_root - self.drag_start_y

        new_x = self.window_start_x + delta_x
        new_y = self.window_start_y + delta_y

        self.geometry(
            f"+{new_x}+{new_y}"
        )