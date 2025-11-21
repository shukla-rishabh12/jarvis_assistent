from jarvis_local import take_screenshot, open_notepad, open_app
from web_utils import play_youtube, google_search, send_whatsapp_msg
from ai_sense import ask_gemini  # New import

def recognize_intent(command):
    command = command.lower()

    # Local actions
    if any(word in command for word in ["screenshot", "screen shot", "photo", "screen"]):
        return take_screenshot()
    elif any(word in command for word in ["notepad", "note", "text editor"]):
        return open_notepad()
    elif "open" in command or "chalao" in command:
        app_name = command.replace("open", "").replace("chalao", "").strip()
        if app_name:
            return open_app(app_name)
        return "App name not recognized"

    # Web actions
    elif any(word in command for word in ["youtube", "video"]):
        video_name = command.replace("youtube", "").replace("video", "").strip()
        return play_youtube(video_name)
    elif any(word in command for word in ["google", "search", "kya hai"]):
        query = command.replace("google", "").replace("search", "").strip()
        return google_search(query)

    # WhatsApp
    elif "whatsapp" in command:
        try:
            parts = command.split()
            number = parts[1]
            message = " ".join(parts[2:-2])
            hour = int(parts[-2])
            minute = int(parts[-1])
            return send_whatsapp_msg(number, message, hour, minute)
        except:
            return "WhatsApp command format incorrect"

    else:
        # AI Fallback using Gemini
        return ask_gemini(command)
