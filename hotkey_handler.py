import time
import threading
import keyboard
import pyperclip

from translator import translate_text

# Delays between simulated keystrokes (seconds)
_STEP_DELAY = 0.08
_COPY_DELAY = 0.15
_BUSY = False


def _release_modifiers():
    """Release all modifier keys to prevent them from getting stuck."""
    for key in ("ctrl", "shift", "alt"):
        try:
            keyboard.release(key)
        except Exception:
            pass


def _select_all_and_copy() -> str:
    """Select all text in the active input and copy it to clipboard."""
    old_clip = pyperclip.paste()
    pyperclip.copy("")

    _release_modifiers()
    time.sleep(_STEP_DELAY)

    keyboard.press_and_release("ctrl+a")
    time.sleep(_STEP_DELAY)
    keyboard.press_and_release("ctrl+c")
    time.sleep(_COPY_DELAY)

    text = pyperclip.paste()

    if not text.strip():
        pyperclip.copy(old_clip)

    return text.strip()


def _paste_and_send(text: str):
    """Paste translated text and press Enter to send."""
    pyperclip.copy(text)
    time.sleep(_STEP_DELAY)
    keyboard.press_and_release("ctrl+v")
    time.sleep(_STEP_DELAY)
    keyboard.press_and_release("enter")


def _do_translate(config, on_translation):
    """Actual translation logic, runs in a separate thread."""
    global _BUSY
    try:
        if not config.get("enabled", True):
            time.sleep(_STEP_DELAY)
            _release_modifiers()
            keyboard.press_and_release("enter")
            return

        original = _select_all_and_copy()
        if not original:
            _release_modifiers()
            keyboard.press_and_release("enter")
            return

        translated = translate_text(
            original,
            source_lang=config.get("source_lang", "auto"),
            target_lang=config.get("target_lang", "en"),
        )

        if translated is None:
            _release_modifiers()
            keyboard.press_and_release("enter")
            return

        # Clear current text, paste translation, send
        _release_modifiers()
        keyboard.press_and_release("ctrl+a")
        time.sleep(_STEP_DELAY)
        _paste_and_send(translated)

        if on_translation:
            on_translation(original, translated)
    except Exception as e:
        print(f"[hotkey_handler] error: {e}")
        _release_modifiers()
    finally:
        _BUSY = False


def handle_translate_hotkey(config: dict, on_translation=None):
    """
    Called when the translate hotkey is pressed.
    Spawns a worker thread to avoid blocking the keyboard hook.
    """
    global _BUSY
    if _BUSY:
        return
    _BUSY = True
    t = threading.Thread(target=_do_translate, args=(config, on_translation), daemon=True)
    t.start()
