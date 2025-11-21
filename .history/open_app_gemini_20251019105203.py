import os
from ai_sense import ask_gemini
from voice_utils import speak

# 🎯 Common app paths
app_paths = {
    "notepad": "notepad.exe",
    "vs code": r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "visual studio code": r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"
}

def open_app_with_gemini(user_input):
    """Uses Gemini to decide which app to open from user's spoken command."""
    prompt = (
        f"User said: '{user_input}'. "
        f"Which app should be opened? Options: Notepad, VS Code, Chrome, Word, PowerPoint. "
        f"Give answer in English with only the app name."
    )

    print("\n🧠 Prompt to Gemini →", prompt)
    app_name = ask_gemini(prompt).lower().strip()
    print("🤖 Gemini replied →", app_name)

    # Match the response with available app paths
    matched_app = None
    for name in app_paths.keys():
        if name in app_name:
            matched_app = name
            break

    if matched_app:
        try:
            speak(f"{matched_app} खोल रहा हूँ सर, कृपया एक क्षण प्रतीक्षा करें।")
            os.startfile(app_paths[matched_app])
            speak(f"{matched_app} सफलतापूर्वक खुल गया सर।")
            print(f"✅ {matched_app} opened successfully.")
            return f"{matched_app} opened successfully via Gemini."
        except Exception as e:
            speak(f"{matched_app} खोलने में समस्या आई सर।")
            print(f"❌ Error opening {matched_app}: {e}")
            return f"Error opening {matched_app}: {e}"
    else:
        speak("माफ़ कीजिए सर, मुझे यह ऐप नहीं मिली।")
        print(f"⚠️ Could not identify app from input: {user_input}")
        return f"Could not identify app from input: '{user_input}'"
