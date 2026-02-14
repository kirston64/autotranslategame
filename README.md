# CS2 Chat Translator

Автоматический переводчик чата CS2. Набираешь сообщение на любом языке, нажимаешь хоткей — оно переводится и отправляется.

## Скачать

Скачай готовый **CS2ChatTranslator.exe** из [Releases](https://github.com/kirston64/autotranslategame/releases) и запусти. Установка не нужна.

> CS2 должна быть в режиме **Borderless Windowed** (безрамочный оконный), не Fullscreen.

## Как пользоваться

1. Запусти **CS2ChatTranslator.exe**
2. Настрой хоткей, язык перевода, оверлей
3. Нажми **Start**
4. Открой CS2, зайди в чат (Y / U)
5. Напиши сообщение на любом языке
6. Нажми **Ctrl+Enter** (или твой хоткей) вместо Enter
7. Сообщение автоматически переведётся и отправится

## Запуск из исходников

```bash
git clone https://github.com/kirston64/autotranslategame.git
cd autotranslategame
pip install -r requirements.txt
python main.py
```

## Сборка в .exe (Windows)

```bash
build.bat
```

Готовый файл будет в `dist\CS2ChatTranslator.exe`.

## Настройки

Всё сохраняется в `config.json` (создаётся автоматически рядом с .exe):

| Параметр | Описание | По умолчанию |
|---|---|---|
| `hotkey` | Горячая клавиша | `ctrl+enter` |
| `target_lang` | Язык перевода | `en` |
| `overlay_enabled` | Показывать оверлей | `true` |
| `overlay_duration` | Длительность оверлея (сек) | `2.0` |
