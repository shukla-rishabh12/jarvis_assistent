import os
from ai_sense import ask_gemini

app_paths = {
    "notepad": "notepad.exe",
    "vs code": r"C:\\Users\\dell\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "chrome": "chrome.exe",
    "msexel":r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Excel 2007.lnk",
    "word": r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Word 2007.lnk",
    "powerpoint": r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office PowerPoint 2007.lnk",
    "powerbi": r"C:\\Users\\Public\\Desktop\\Power BI Desktop.lnk"
}

def open_app_with_gemini(user_input):
    prompt = f"User said: '{user_input}'. Which app to open? Choose among Notepad, VS Code, Chrome, Word,powerbi, PowerPoint. Return app name only."
    app_name = ask_gemini(prompt).lower().strip()

    if app_name in app_paths:
        try:
            os.startfile(app_paths[app_name])
            return f"{app_name} opened successfully via Gemini"
        except Exception as e:
            return f"Error opening {app_name}: {e}"
    else:
        return f"Could not identify app from input: '{user_input}'"
