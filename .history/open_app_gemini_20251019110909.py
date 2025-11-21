import os
from ai_sense import ask_gemini
from voice_utils import speak

# 🎯 Define app paths
app_paths = {
    "notepad": "notepad.exe",
    "vs code": r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "visual studio code": r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "powerpoint": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Office PowerPoint 2007.lnk"
}

def open_app_with_gemini(user_input):
    prompt = (
        f"User said: '{user_input}'. "
        f"Which app should be opened? Options: Notepad, VS Code, Chrome, Word, PowerPoint. "
        f"Give answer in English with only the app name."
    )

    print("\n🧠 Prompt to Gemini →", prompt)
    app_name = ask_gemini(prompt).lower().strip()
    print("🤖 Gemini replied →", app_name)

    # ✅ Try to find best match
    matched_app = None
    for name in app_paths.keys():
        if name in app_name or app_name in name:
            matched_app = name
            break

    if matched_app:
        path = app_paths[matched_app]
        if not os.path.exists(path):
            speak(f"सर, लगता है {matched_app} का path गलत है।")
            print(f"⚠️ File not found: {path}")
            return f"Path not found: {path}"

        try:
            speak(f"{matched_app} खोल रहा हूँ सर, कृपया एक क्षण प्रतीक्षा करें।")
            os.startfile(path)
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
