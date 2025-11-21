import os
from ai_sense import ask_gemini
from voice_utils import speak

app_paths = {
    "notepad": "notepad.exe",
    "vs code": r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": "chrome.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"
}

def open_app_with_gemini(user_input):
    prompt = f"User said: '{user_input}'. Which app should be opened? Options: Notepad, VS Code, Chrome, Word, PowerPoint. Reply with app name only."
    app_name = ask_gemini(prompt).lower().strip()

    if app_name in app_paths:
        try:
            speak(f"{app_name} khola ja raha hai...")
            os.startfile(app_paths[app_name])
            speak(f"{app_name} safalta purvak khul gaya.")
            return f"{app_name} opened successfully via Gemini"
        except Exception as e:
            speak(f"{app_name} kholne mein dikkat aayi.")
            return f"Error opening {app_name}: {e}"
    else:
        speak("मुझे यह ऐप नहीं मिली।")
        return f"Could not identify app from input: '{user_input}'"
