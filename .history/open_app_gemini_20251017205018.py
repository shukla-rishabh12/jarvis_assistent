import os
from ai_sense import ask_gemini

app_paths = {
    "notepad": "notepad.exe",
    "vs code": r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": "chrome.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"
}

def open_app_with_gemini(user_input):
    prompt = f"User said: '{user_input}'. Which app to open? Choose among Notepad, VS Code, Chrome, Word, PowerPoint. Return app name only."
    app_name = ask_gemini(prompt).lower().strip()

    if app_name in app_paths:
        try:
            os.startfile(app_paths[app_name])
            return f"{app_name} opened successfully via Gemini"
        except Exception as e:
            return f"Error opening {app_name}: {e}"
    else:
        return f"Could not identify app from input: '{user_input}'"
