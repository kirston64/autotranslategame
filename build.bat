@echo off
echo Building CS2 Chat Translator...
pyinstaller --onefile --noconsole --name CS2ChatTranslator --add-data "config.json;." main.py
echo.
echo Done! Check dist\CS2ChatTranslator.exe
pause
