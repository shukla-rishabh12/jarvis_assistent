from open_app_gemini import open_app_with_gemini
from web_utils import play_youtube, google_search, send_whatsapp_msg
from ai_sense import ask_gemini
from voice_utils import speak

def recognize_intent(cmd, context_history=None):
    command = cmd.lower()
    if context_history is None:
        context_history = []

    # ✅ Local Apps
    if any(word in command for word in ["open", "chalao", "launch", "khol"]):
        speak("Ek minute ruk jaiye, main app khol raha hoon...")
        result = open_app_with_gemini(command)
        speak(result)
        return result

    # ✅ YouTube
    elif "youtube" in command or "video" in command:
        speak("YouTube par search kar raha hoon...")
        video_name = command.replace("youtube", "").replace("video", "").strip()
        result = play_youtube(video_name)
        speak(result)
        return result

    # ✅ Google Search
    elif "google" in command or "search" in command or "kya hai" in command:
        speak("Google par search kar raha hoon...")
        query = command.replace("google", "").replace("search", "").strip()
        result = google_search(query)
        speak(result)
        return result

    # ✅ WhatsApp Message
    elif "whatsapp" in command:
        speak("WhatsApp message bhej raha hoon...")
        try:
            parts = command.split()
            number = parts[1]
            message = " ".join(parts[2:-2])
            hour = int(parts[-2])
            minute = int(parts[-1])
            result = send_whatsapp_msg(number, message, hour, minute)
            speak(result)
            return result
        except:
            msg = "WhatsApp command format sahi nahi hai."
            speak(msg)
            return msg

    # ✅ Fallback Gemini Response (AI)
    else:
        speak("Soch raha hoon... thoda wait kijiye.")
        history_text = "\n".join([f"User: {x['user']}\nAssistant: {x['assistant']}" for x in context_history])
        prompt = f"Previous conversation:\n{history_text}\n\nCurrent command: {cmd}\nReturn meaningful short answer in Hindi if possible."
        result = ask_gemini(prompt)
        speak(result)
        return result
