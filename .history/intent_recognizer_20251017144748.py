from jarvis_local import take_screenshot, open_notepad, open_app
from web_utils import google_search, play_youtube, send_whatsapp_msg

def recognize_intent(command):
    command = command.lower()

    # LOCAL ACTIONS
    if any(word in command for word in ["screenshot", "screen shot", "photo"]):
        return take_screenshot()
    elif any(word in command for word in ["notepad", "text editor", "note"]):
        return open_notepad()
    elif any(word in command for word in ["open", "chalao"]):
        app_name = command.replace("open", "").replace("chalao", "").strip()
        if app_name:
            return open_app(app_name)
        return "App name not recognized"

    # WEB ACTIONS
    elif any(word in command for word in ["youtube", "video"]):
        video_name = command.replace("youtube", "").replace("video", "").strip()
        return play_youtube(video_name)
    elif any(word in command for word in ["google", "search", "kya hai"]):
        query = command.replace("google", "").replace("search", "").strip()
        return google_search(query)
    
    # WHATSAPP
    elif "whatsapp" in command:
        # Example: "whatsapp +911234567890 Hello at 15 30"
        try:
            parts = command.split()
            number = parts[1]
            message = " ".join(parts[2:-2])
            hour = int(parts[-2])
            minute = int(parts[-1])
            return send_whatsapp_msg(number, message, hour, minute)
        except:
            return "Whatsapp command format incorrect"

    else:
        return "Command not recognized, please try again"
