@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building CS2 Chat Translator...
pyinstaller ^
    --onefile ^
    --noconsole ^
    --name CS2ChatTranslator ^
    --add-data "config.json;." ^
    --collect-all customtkinter ^
    --hidden-import pynput ^
    --hidden-import pyperclip ^
    --hidden-import deep_translator ^
    main.py

echo.
if exist "dist\CS2ChatTranslator.exe" (
    echo SUCCESS! File: dist\CS2ChatTranslator.exe
) else (
    echo BUILD FAILED. Check errors above.
)
pause
