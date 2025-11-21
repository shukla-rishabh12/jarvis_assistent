#intent_recognizer

from open_app_gemini import open_app_with_gemini
from web_utils import play_youtube, google_search#, send_whatsapp_msg
from wp_utils import send_whatsapp_via_gemini
from close_utils import close_app
from ai_sense import ask_gemini
from voice_utils import speak


def recognize_intent(cmd, context_history=None):
    print('🔹 Recognizing intent...')
    command = cmd.lower()
    if context_history is None:
        context_history = []





        # ✅ App close command (Local)
    if "बंद" in command or "close" in command:
        possible_apps = ["notepad", "chrome", "word", "excel", "powerpoint", "vs code", "spotify", "edge"]
        for app in possible_apps:
            if app in command:
                speak(f"ठीक है सर, {app} बंद कर रहा हूँ...")
                result = close_app(app)
                speak(result)
                print(f"✅ Jarvis Result: {result}")
                return result  # Stop further processing
    

    # ✅ Local Apps (Expanded Hindi detection)
    if any(word in command for word in [
        "open", "chalao", "launch", "khol", "kholo", "खोल", "ओपन", "चालू", "चलाओ"
    ]):
        speak("एक मिनट रुके सर, मैं एप्लिकेशन खोल रहा हूँ...")
        result = open_app_with_gemini(command)
        speak(result)
        return result

    # ✅ YouTube
    elif "यूट्यूब" in command or "वीडियो" in command:
        speak("यूट्यूब पर सर्च कर रहा हूँ सर...")
        video_name = command.replace("youtube", "").replace("वीडियो", "").strip()
        result = play_youtube(video_name)
        speak(result)
        return result

    # ✅ Google Search
    elif "google" in command or "सर्च" in command or "कया है" in command or "क्या है" in command:
        speak("गूगल पर सर्च कर रहा हूँ सर...")
        query = command.replace("google", "").replace("search", "").replace("क्या है", "").strip()
        result = google_search(query)
        speak(result)
        return result

    # ✅ WhatsApp Message (Gemini-based)
    elif any(word in command for word in ["whatsapp", "व्हाट्सएप", "message bhejo", "मैसेज भेजो"]):
        speak("WhatsApp command detect hui, thoda wait kijiye...")
        result = send_whatsapp_via_gemini(cmd)
        print("✅ Jarvis Result:", result)
        speak(result)
        return result


    
        
    # ✅ Fallback (Gemini)
    else:
        speak("थोड़ा सोचने दीजिए सर...")
        history_text = "\n".join([f"User: {x['user']}\nAssistant: {x['assistant']}" for x in context_history])
        prompt = f"Previous conversation:\n{history_text}\n\nCurrent command: {cmd}\nReturn short intelligent answer in English or Hindi."
        result = ask_gemini(prompt)
        # speak(result)
        return result



# from open_app_gemini import open_app_with_gemini
# from web_utils import play_youtube, google_search, send_whatsapp_msg

# from ai_sense import ask_gemini
# from voice_utils import speak

# def recognize_intent(cmd, context_history=None):
#     print('recognise intent')
#     command = cmd.lower()
#     if context_history is None:
#         context_history = []

#     # ✅ Local Apps (Expanded Hindi detection)
#     if any(word in command for word in [
#         "open", "chalao", "launch", "khol", "kholo", "खोल", "ओपन", "चालू", "चलाओ"
#     ]):
#         speak("एक मिनट रुके सर, मैं एप्लिकेशन खोल रहा हूँ...")
#         result = open_app_with_gemini(command)
#         speak(result)
#         return result

#     # ✅ YouTube
#     elif "यूट्यूब" in command or "वीडियो" in command:
#         speak("यूट्यूब पर सर्च कर रहा हूँ सर...")
#         video_name = command.replace("youtube", "").replace("वीडियो", "").strip()
#         result = play_youtube(video_name)
#         speak(result)
#         return result

#     # ✅ Google Search
#     elif "google" in command or "सर्च" in command or "कया है" in command or "क्या है" in command:
#         speak("गूगल पर सर्च कर रहा हूँ सर...")
#         query = command.replace("google", "").replace("search", "").replace("क्या है", "").strip()
#         result = google_search(query)
#         speak(result)
#         return result

#     # ✅ WhatsApp Message
#     elif "व्हाट्सएप" in command:
#         speak("व्हाट्सएप मैसेज भेजने की कोशिश कर रहा हूँ सर...")
#         try:

#             parts = command.split()
#             number = parts[1]
#             message = " ".join(parts[2:-2])
#             hour = int(parts[-2])
#             minute = int(parts[-1])
#             result = send_whatsapp_msg(number, message, hour, minute)
#             speak(f"मैसेज शेड्यूल कर दिया गया है सर।")
#             return result
#         except:
#             msg = "व्हाट्सएप कमांड का फॉर्मेट सही नहीं है।"
#             speak(msg)
#             return msg

#     # ✅ Fallback (Gemini)
#     else:
#         speak("थोड़ा सोचने दीजिए सर...")
#         history_text = "\n".join([f"User: {x['user']}\nAssistant: {x['assistant']}" for x in context_history])
#         prompt = f"Previous conversation:\n{history_text}\n\nCurrent command: {cmd}\nReturn short intelligent answer in English or Hindi."
#         result = ask_gemini(prompt)
#         speak(result)
#         return result
