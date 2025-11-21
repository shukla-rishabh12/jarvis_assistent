from open_app_gemini import open_app_with_gemini
from web_utils import play_youtube, google_search, send_whatsapp_msg
from ai_sense import ask_gemini

def recognize_intent(cmd, context_history=None):
    command = cmd.lower()
    if context_history is None:
        context_history = []

    # Local apps
    if any(word in command for word in ["open", "chalao", "launch"]):
        return open_app_with_gemini(command)

    # YouTube
    elif "youtube" in command or "video" in command:
        video_name = command.replace("youtube", "").replace("video", "").strip()
        return play_youtube(video_name)

    # Google search
    elif "google" in command or "search" in command or "kya hai" in command:
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

    # Fallback AI with context
    else:
        history_text = "\n".join([f"User: {x['user']}\nAssistant: {x['assistant']}" for x in context_history])
        prompt = f"Previous conversation:\n{history_text}\n\nCurrent command: {cmd}\nReturn appropriate action or response."
        return ask_gemini(prompt)
