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
        speak("एक मिनट रुके सर, मैं एप्लिकेशन खोल रहा हूँ...")
        result = open_app_with_gemini(command)
        speak(f"लो जी, {result}")
        return result

    # ✅ YouTube
    elif "youtube" in command or "video" in command:
        speak("यूट्यूब पर सर्च कर रहा हूँ सर...")
        video_name = command.replace("youtube", "").replace("video", "").strip()
        result = play_youtube(video_name)
        speak(f"ये रहा आपका वीडियो: {result}")
        return result

    # ✅ Google Search
    elif "google" in command or "search" in command or "kya hai" in command:
        speak("गूगल पर सर्च कर रहा हूँ सर...")
        query = command.replace("google", "").replace("search", "").strip()
        result = google_search(query)
        speak(f"मुझे ये मिला: {result}")
        return result

    # ✅ WhatsApp Message
    elif "whatsapp" in command:
        speak("व्हाट्सएप मैसेज भेजने की कोशिश कर रहा हूँ सर...")
        try:
            parts = command.split()
            number = parts[1]
            message = " ".join(parts[2:-2])
            hour = int(parts[-2])
            minute = int(parts[-1])
            result = send_whatsapp_msg(number, message, hour, minute)
            speak(f"मैसेज शेड्यूल कर दिया गया है सर।")
            return result
        except:
            msg = "व्हाट्सएप कमांड का फॉर्मेट सही नहीं है।"
            speak(msg)
            return msg

    # ✅ AI fallback (Gemini)
    else:
        speak("थोड़ा सोचने दीजिए सर...")
        history_text = "\n".join([f"User: {x['user']}\nAssistant: {x['assistant']}" for x in context_history])
        prompt = f"Previous conversation:\n{history_text}\n\nCurrent command: {cmd}\nReturn short intelligent answer in English or Hindi."
        result = ask_gemini(prompt)
        speak(result)
        return result





# from open_app_gemini import open_app_with_gemini
# from web_utils import play_youtube, google_search, send_whatsapp_msg
# from ai_sense import ask_gemini
# from voice_utils import speak

# def recognize_intent(cmd, context_history=None):
#     command = cmd.lower()
#     if context_history is None:
#         context_history = []

#     # ✅ Local Apps
#     if any(word in command for word in ["open", "chalao", "launch", "khol"]):
#         speak("Ek minute ruk jaiye, main app khol raha hoon...")
#         result = open_app_with_gemini(command)
#         speak(result)
#         return result

#     # ✅ YouTube
#     elif "youtube" in command or "video" in command:
#         speak("YouTube par search kar raha hoon...")
#         video_name = command.replace("youtube", "").replace("video", "").strip()
#         result = play_youtube(video_name)
#         speak(result)
#         return result

#     # ✅ Google Search
#     elif "google" in command or "search" in command or "kya hai" in command:
#         speak("Google par search kar raha hoon...")
#         query = command.replace("google", "").replace("search", "").strip()
#         result = google_search(query)
#         speak(result)
#         return result

#     # ✅ WhatsApp Message
#     elif "whatsapp" in command:
#         speak("WhatsApp message bhej raha hoon...")
#         try:
#             parts = command.split()
#             number = parts[1]
#             message = " ".join(parts[2:-2])
#             hour = int(parts[-2])
#             minute = int(parts[-1])
#             result = send_whatsapp_msg(number, message, hour, minute)
#             speak(result)
#             return result
#         except:
#             msg = "WhatsApp command format sahi nahi hai."
#             speak(msg)
#             return msg

#     # ✅ Fallback Gemini Response (AI)
#     else:
#         speak("Soch raha hoon... thoda wait kijiye.")
#         history_text = "\n".join([f"User: {x['user']}\nAssistant: {x['assistant']}" for x in context_history])
#         prompt = f"Previous conversation:\n{history_text}\n\nCurrent command: {cmd}\nReturn meaningful short answer in english if possible."
#         result = ask_gemini(prompt)
#         speak((result))
#         return result
