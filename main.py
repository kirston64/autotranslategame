"""
CS2 Chat Translator
Automatically translates game chat messages to English.

Usage:
    1. Run: python main.py
    2. Open CS2 and enter chat (Y / U)
    3. Type your message in any language
    4. Press Ctrl+Enter instead of Enter
    5. Message is translated and sent automatically
"""

import sys
import keyboard

from config import load_config
from hotkey_handler import handle_translate_hotkey
from overlay import TranslationOverlay
from gui import run_gui

_overlay = None
_gui = None


def _on_start(config):
    global _overlay
    _overlay = TranslationOverlay(duration=config.get("overlay_duration", 2.0))

    def on_translation(original, translated):
        if config.get("overlay_enabled", True):
            _overlay.show(original, translated)
        if _gui:
            _gui.log(f'"{original}" -> "{translated}"')

    keyboard.unhook_all()
    hotkey = config.get("hotkey", "ctrl+enter")
    keyboard.add_hotkey(
        hotkey,
        lambda: handle_translate_hotkey(config, on_translation=on_translation),
    )
    print(f"[CS2 Translator] Active — hotkey: {hotkey}")


def _on_stop():
    keyboard.unhook_all()
    print("[CS2 Translator] Stopped.")


def _on_exit():
    keyboard.unhook_all()
    print("[CS2 Translator] Exiting...")
    sys.exit(0)


def main():
    global _gui
    print("[CS2 Chat Translator] Starting GUI...")
    from gui import TranslatorGUI

    _gui = TranslatorGUI(on_start=_on_start, on_stop=_on_stop, on_exit=_on_exit)
    _gui.mainloop()


if __name__ == "__main__":
    main()
