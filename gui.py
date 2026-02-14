import threading
import tkinter as tk
import customtkinter as ctk

from config import load_config, save_config

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class TranslatorGUI(ctk.CTk):
    """Main settings window for CS2 Chat Translator."""

    def __init__(self, on_start=None, on_stop=None, on_exit=None):
        super().__init__()

        self.on_start = on_start
        self.on_stop = on_stop
        self.on_exit = on_exit
        self._running = False

        self.title("CS2 Chat Translator")
        self.geometry("520x560")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.config_data = load_config()
        self._build_ui()

    def _build_ui(self):
        # --- Settings frame ---
        settings = ctk.CTkFrame(self, corner_radius=10)
        settings.pack(fill="x", padx=16, pady=(16, 8))

        ctk.CTkLabel(settings, text="Settings", font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", padx=12, pady=(10, 6)
        )

        row1 = ctk.CTkFrame(settings, fg_color="transparent")
        row1.pack(fill="x", padx=12, pady=4)
        ctk.CTkLabel(row1, text="Hotkey:").pack(side="left")
        self.hotkey_var = ctk.StringVar(value=self.config_data.get("hotkey", "ctrl+enter"))
        ctk.CTkEntry(row1, textvariable=self.hotkey_var, width=180).pack(side="right")

        row2 = ctk.CTkFrame(settings, fg_color="transparent")
        row2.pack(fill="x", padx=12, pady=4)
        ctk.CTkLabel(row2, text="Translate to:").pack(side="left")
        self.lang_var = ctk.StringVar(value=self.config_data.get("target_lang", "en"))
        ctk.CTkOptionMenu(
            row2,
            variable=self.lang_var,
            values=["en", "ru", "de", "fr", "es", "pt", "zh-CN", "ja", "ko", "uk"],
            width=180,
        ).pack(side="right")

        row3 = ctk.CTkFrame(settings, fg_color="transparent")
        row3.pack(fill="x", padx=12, pady=4)
        ctk.CTkLabel(row3, text="Overlay:").pack(side="left")
        self.overlay_var = ctk.BooleanVar(value=self.config_data.get("overlay_enabled", True))
        ctk.CTkSwitch(row3, text="", variable=self.overlay_var, onvalue=True, offvalue=False).pack(
            side="right"
        )

        row4 = ctk.CTkFrame(settings, fg_color="transparent")
        row4.pack(fill="x", padx=12, pady=(4, 10))
        ctk.CTkLabel(row4, text="Overlay duration (s):").pack(side="left")
        self.duration_var = ctk.StringVar(
            value=str(self.config_data.get("overlay_duration", 2.0))
        )
        ctk.CTkEntry(row4, textvariable=self.duration_var, width=180).pack(side="right")

        # --- Control buttons ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=8)

        self.start_btn = ctk.CTkButton(
            btn_frame, text="Start", command=self._toggle, width=200, height=38
        )
        self.start_btn.pack(side="left", expand=True)

        ctk.CTkButton(
            btn_frame, text="Save Settings", command=self._save, width=200, height=38,
            fg_color="#555555", hover_color="#666666"
        ).pack(side="right", expand=True)

        # --- Log ---
        log_label = ctk.CTkLabel(self, text="Translation Log", font=ctk.CTkFont(size=14, weight="bold"))
        log_label.pack(anchor="w", padx=16, pady=(8, 2))

        self.log_box = ctk.CTkTextbox(self, height=220, state="disabled", font=ctk.CTkFont(size=12))
        self.log_box.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        # --- Status bar ---
        self.status_var = ctk.StringVar(value="Inactive")
        status_bar = ctk.CTkLabel(
            self, textvariable=self.status_var, font=ctk.CTkFont(size=12),
            fg_color="#2b2b2b", corner_radius=0, height=28
        )
        status_bar.pack(fill="x", side="bottom")

    def _save(self):
        self.config_data["hotkey"] = self.hotkey_var.get().strip()
        self.config_data["target_lang"] = self.lang_var.get()
        self.config_data["overlay_enabled"] = self.overlay_var.get()
        try:
            self.config_data["overlay_duration"] = float(self.duration_var.get())
        except ValueError:
            self.config_data["overlay_duration"] = 2.0
        save_config(self.config_data)
        self.log("Settings saved.")

    def _toggle(self):
        if self._running:
            self._running = False
            self.start_btn.configure(text="Start", fg_color=["#2CC985", "#2FA572"])
            self.status_var.set("Inactive")
            self.config_data["enabled"] = False
            save_config(self.config_data)
            if self.on_stop:
                self.on_stop()
            self.log("Translator stopped.")
        else:
            self._save()
            self._running = True
            self.start_btn.configure(text="Stop", fg_color="#e04040")
            self.status_var.set(f"Active  |  Hotkey: {self.config_data['hotkey']}  |  Lang: {self.config_data['target_lang']}")
            self.config_data["enabled"] = True
            save_config(self.config_data)
            if self.on_start:
                self.on_start(self.config_data)
            self.log("Translator started.")

    def log(self, text: str):
        """Append a line to the log (thread-safe)."""
        def _append():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", text + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")

        if threading.current_thread() is threading.main_thread():
            _append()
        else:
            self.after(0, _append)

    def _on_close(self):
        if self.on_exit:
            self.on_exit()
        self.destroy()


def run_gui(on_start=None, on_stop=None, on_exit=None) -> TranslatorGUI:
    """Create and run the GUI. Blocks until window is closed."""
    app = TranslatorGUI(on_start=on_start, on_stop=on_stop, on_exit=on_exit)
    app.mainloop()
    return app
