from close_utils import close_app
from voice_utils import speak

def recognize_intent(cmd, context_history=None):
    print('🔹 Recognizing intent...')
    command = cmd.lower()
    if context_history is None:
        context_history = []

    # ✅ Close App commands (local)
    if "बंद" in command or "close" in command:
        # Check for specific app
        possible_apps = ["notepad", "chrome", "word", "excel", "powerpoint", "vs code", "spotify", "edge", "सभी", "all"]
        for app in possible_apps:
            if app in command:
                if app in ["सभी", "all"]:
                    result = close_app("all")
                else:
                    result = close_app(app)
                speak(result)
                print(f"✅ Jarvis Result: {result}")
                return result  # stop further processing

    # ✅ Other intents...
    # Open app, YouTube, Google, WhatsApp, Gemini fallback
    # ... existing code continues
