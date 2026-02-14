import threading
import tkinter as tk


class TranslationOverlay:
    """Transparent topmost overlay that briefly shows the translation."""

    def __init__(self, duration: float = 2.0):
        self.duration = duration
        self._root = None
        self._label = None
        self._lock = threading.Lock()

    def show(self, original: str, translated: str):
        """Show overlay in a separate thread (non-blocking)."""
        t = threading.Thread(target=self._display, args=(original, translated), daemon=True)
        t.start()

    def _display(self, original: str, translated: str):
        with self._lock:
            root = tk.Tk()
            root.overrideredirect(True)
            root.attributes("-topmost", True)
            root.attributes("-alpha", 0.85)
            root.configure(bg="#1a1a2e")

            frame = tk.Frame(root, bg="#1a1a2e", padx=16, pady=10)
            frame.pack()

            tk.Label(
                frame,
                text=original,
                font=("Segoe UI", 12),
                fg="#888888",
                bg="#1a1a2e",
                wraplength=500,
                justify="left",
            ).pack(anchor="w")

            tk.Label(
                frame,
                text=f"-> {translated}",
                font=("Segoe UI", 13, "bold"),
                fg="#00ff88",
                bg="#1a1a2e",
                wraplength=500,
                justify="left",
            ).pack(anchor="w", pady=(4, 0))

            # Position: bottom-center of screen
            root.update_idletasks()
            w = root.winfo_reqwidth()
            h = root.winfo_reqheight()
            sw = root.winfo_screenwidth()
            sh = root.winfo_screenheight()
            x = (sw - w) // 2
            y = sh - h - 80
            root.geometry(f"+{x}+{y}")

            root.after(int(self.duration * 1000), root.destroy)
            root.mainloop()
