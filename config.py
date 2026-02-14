import json
import os
import sys


def _get_base_dir():
    """Get the directory where the exe (or script) is located."""
    if getattr(sys, "frozen", False):
        # Running as PyInstaller .exe
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


CONFIG_PATH = os.path.join(_get_base_dir(), "config.json")

DEFAULT_CONFIG = {
    "hotkey": "ctrl+enter",
    "source_lang": "auto",
    "target_lang": "en",
    "overlay_enabled": True,
    "overlay_duration": 2.0,
    "enabled": True,
}


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        merged = {**DEFAULT_CONFIG, **cfg}
        return merged
    # First run — create default config
    save_config(DEFAULT_CONFIG)
    return dict(DEFAULT_CONFIG)


def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)
