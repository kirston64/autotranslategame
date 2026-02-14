import time
import keyboard
import pyperclip

from translator import translate_text

# Delays between simulated keystrokes (seconds)
_STEP_DELAY = 0.05
_COPY_DELAY = 0.10


def _select_all_and_copy() -> str:
    """Select all text in the active input and copy it to clipboard."""
    old_clip = pyperclip.paste()
    pyperclip.copy("")

    keyboard.send("ctrl+a")
    time.sleep(_STEP_DELAY)
    keyboard.send("ctrl+c")
    time.sleep(_COPY_DELAY)

    text = pyperclip.paste()

    # Restore old clipboard if we got nothing
    if not text.strip():
        pyperclip.copy(old_clip)

    return text.strip()


def _paste_and_send(text: str):
    """Paste translated text and press Enter to send."""
    pyperclip.copy(text)
    time.sleep(_STEP_DELAY)
    keyboard.send("ctrl+v")
    time.sleep(_STEP_DELAY)
    keyboard.send("enter")


def handle_translate_hotkey(config: dict, on_translation=None):
    """
    Called when the translate hotkey is pressed.
    1. Selects all text in chat input
    2. Copies it
    3. Translates
    4. Pastes translation and sends

    on_translation: optional callback(original, translated) for overlay
    """
    if not config.get("enabled", True):
        keyboard.send("enter")
        return

    original = _select_all_and_copy()
    if not original:
        keyboard.send("enter")
        return

    translated = translate_text(
        original,
        source_lang=config.get("source_lang", "auto"),
        target_lang=config.get("target_lang", "en"),
    )

    if translated is None:
        # Already in target language — just send as-is
        keyboard.send("enter")
        return

    # Clear current text, paste translation, send
    keyboard.send("ctrl+a")
    time.sleep(_STEP_DELAY)
    _paste_and_send(translated)

    if on_translation:
        on_translation(original, translated)
