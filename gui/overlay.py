import customtkinter as ctk


class AURONOverlay(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.parent = parent

        # ==========================================
        # OVERLAY STATE
        # ==========================================

        self.ai_mode = "General"
        self.focus_text = "OFF"
        self.focus_active = False
        self.meeting_active = False
        self.task_count = 0
        self.status = "IDLE"

        # ==========================================
        # WINDOW CONFIG
        # ==========================================

        self.geometry("320x82+1030+55")
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Whole overlay slight transparency
        self.attributes("-alpha", 0.88)

        # Transparent outer background
        self.transparent_color = "#010203"
        self.configure(fg_color=self.transparent_color)

        try:
            self.attributes(
                "-transparentcolor",
                self.transparent_color
            )
        except:
            pass

        # Drag variables
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.window_start_x = 0
        self.window_start_y = 0

        # ==========================================
        # MAIN FRAME
        # ==========================================

        self.outer_frame = ctk.CTkFrame(
            self,
            width=310,
            height=72,
            fg_color="#07101f",
            corner_radius=22,
            border_width=2,
            border_color="#00d9ff"
        )

        self.outer_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.outer_frame.pack_propagate(False)

        # ==========================================
        # TOP ROW
        # ==========================================

        self.top_frame = ctk.CTkFrame(
            self.outer_frame,
            fg_color="transparent"
        )

        self.top_frame.pack(
            fill="x",
            padx=18,
            pady=(10, 0)
        )

        self.title_label = ctk.CTkLabel(
            self.top_frame,
            text="AURON",
            font=("Segoe UI", 18, "bold"),
            text_color="#00e5ff"
        )

        self.title_label.pack(
            side="left"
        )

        self.status_label = ctk.CTkLabel(
            self.top_frame,
            text="● IDLE",
            font=("Segoe UI", 15, "bold"),
            text_color="#7dd3fc"
        )

        self.status_label.pack(
            side="right"
        )

        # ==========================================
        # INFO ROW
        # ==========================================

        self.info_label = ctk.CTkLabel(
            self.outer_frame,
            text="General • 0 Tasks • Focus OFF",
            font=("Segoe UI", 13),
            text_color="#cbd5e1"
        )

        self.info_label.pack(
            pady=(6, 0)
        )

        # ==========================================
        # BINDINGS
        # ==========================================

        bind_widgets = [
            self,
            self.outer_frame,
            self.top_frame,
            self.title_label,
            self.status_label,
            self.info_label
        ]

        for widget in bind_widgets:

            widget.bind(
                "<Button-1>",
                self.start_move
            )

            widget.bind(
                "<B1-Motion>",
                self.do_move
            )

            widget.bind(
                "<Double-Button-1>",
                self.open_auron
            )

    # =====================================================
    # STATUS
    # =====================================================

    def set_status(self, status):

        self.status = status.upper()

        color_map = {
            "IDLE": "#7dd3fc",
            "LISTENING": "#00ffff",
            "THINKING": "#facc15",
            "SPEAKING": "#22c55e"
        }

        color = color_map.get(
            self.status,
            "#7dd3fc"
        )

        self.status_label.configure(
            text=f"● {self.status}",
            text_color=color
        )

    # =====================================================
    # AI MODE
    # =====================================================

    def set_ai_mode(self, mode):

        self.ai_mode = mode

        self.refresh_info()

    # =====================================================
    # FOCUS TIMER
    # =====================================================

    def set_focus_timer(self, text, active=False):

        self.focus_active = active

        if not active:
            self.focus_text = "Focus OFF"

        else:

            cleaned = (
                text.replace("Focus:", "")
                .replace("Pomodoro:", "")
                .strip()
            )

            cleaned = (
                cleaned.replace(" min", "m")
            )

            self.focus_text = cleaned

        self.refresh_info()

    # =====================================================
    # MEETING STATUS
    # =====================================================

    def set_meeting_status(self, active=False):

        self.meeting_active = active

        self.refresh_info()

    # =====================================================
    # TASK COUNT
    # =====================================================

    def set_task_count(self, count):

        self.task_count = count

        self.refresh_info()

    # =====================================================
    # REFRESH INFO ROW
    # =====================================================

    def refresh_info(self):

        parts = [
            self.ai_mode,
            f"{self.task_count} Tasks",
            self.focus_text
        ]

        if self.meeting_active:
            parts.append("MEETING")

        self.info_label.configure(
            text=" • ".join(parts)
        )

    # =====================================================
    # OPEN MAIN WINDOW
    # =====================================================

    def open_auron(self, event=None):

        self.parent.deiconify()
        self.parent.lift()
        self.parent.focus_force()

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