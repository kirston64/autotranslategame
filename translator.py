from deep_translator import GoogleTranslator


def translate_text(text: str, source_lang: str = "auto", target_lang: str = "en") -> str | None:
    """Translate text. Returns None if translation is unnecessary or fails."""
    text = text.strip()
    if not text:
        return None

    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        result = translator.translate(text)
    except Exception as e:
        print(f"[translator] error: {e}")
        return None

    if result and result.strip().lower() != text.strip().lower():
        return result.strip()

    # Text is already in target language or translation is identical
    return None
