#intent_recognizer

from open_app_gemini import open_app_with_gemini
from web_utils import play_youtube, google_search#, send_whatsapp_msg
# from wp_gemini import send_whatsapp_via_gemini
from wp_utils import send_whatsapp_desktop
from wp_gemini import send_whatsapp_via_gemini
from close_utils import close_app
from ai_sense import ask_gemini
from voice_utils import speak
from shutdown_handler import handle_shutdown_command_from_gemini
from close_utils import close_app
from voice_utils import speak
# ... बाकी imports

def recognize_intent(cmd, context_history=None):
    command = cmd.lower()
    if context_history is None:
        context_history = []


    
# Add near top of intent checks (before fallback)

    system_keywords = [
        "shutdown", "shut down", "power off", "restart", "reboot", 
        "hibernate", "हाइबरनेट", "बंद करो", "शटडाउन", "रीस्टार्ट"
    ]
    
    if any(word in command for word in system_keywords):
        # Step 1: Ask Gemini what action to take
        prompt = f"User said: {command}\nReturn only system action: shutdown, restart, sleep, or lock in English."
        gemini_command = ask_gemini(prompt).strip().lower()
        
        # Step 2: Print and speak Gemini's response
        print(f"💡 Gemini interpreted command: {gemini_command}")
        speak(f"Gemini says: {gemini_command}")

        # Step 3: Execute the system action
        result = handle_shutdown_command_from_gemini(gemini_command)

        # Step 4: Print & speak final result
        print("✅ Jarvis Result:", result)
        speak(result)
        return result
# ... existing code ...




    # ✅ Close App commands (सबसे पहले)
    if any(word in command for word in ["close", "बंद", "क्लोज"]):
        result = ""
        if any(word in command for word in ["सभी","ऑल", "all"]):
            result = close_app("all")
        else:
            # try to match specific apps
            apps_list = [
    "नोटपैड","क्रोम","वर्ड","एक्सेल",
    "पावरपॉइंट",
    "वीएस कोड",
    "स्पॉटीफाई",
    "एज"
]
            matched = False
            for app in apps_list:
                if app in command:
                    result = close_app(app)
                    matched = True
                    break
            if not matched:
                result = "❌ Unknown app"

        speak(result)
        print(f"✅ Jarvis Result: {result}")
        return result  # Gemini को न भेजें

    # ✅ बाकी intents...
    # Open app, YouTube, Google, WhatsApp, Gemini fallback
    # ... existing code

  # **stop further processing**, Gemini को न भेजें

    # ✅ 2. Open App commands (local or Gemini-assisted)
    if any(word in command for word in ["open", "chalao", "launch", "khol", "खोल", "ओपन"]):
        speak("एक मिनट रुके सर, मैं एप्लिकेशन खोल रहा हूँ...")
        result = open_app_with_gemini(command)
        speak(result)
        return result

    # ✅ 3. YouTube commands
    if "यूट्यूब" in command or "वीडियो" in command:
        speak("यूट्यूब पर सर्च कर रहा हूँ सर...")
        video_name = command.replace("youtube", "").replace("वीडियो", "").strip()
        result = play_youtube(video_name)
        speak(result)
        return result

    # ✅ 4. Google search
    if "google" in command or "सर्च" in command or "क्या है" in command:
        speak("गूगल पर सर्च कर रहा हूँ सर...")
        query = command.replace("google", "").replace("search", "").replace("क्या है", "").strip()
        result = google_search(query)
        speak(result)
        return result

    # ✅ 5. WhatsApp commands
    # intent_recognizer.py

    # WhatsApp detection
    if any(word in command for word in ["whatsapp", "व्हाट्सएप", "message bhejo", "मैसेज भेजो"]):
        result = send_whatsapp_via_gemini(command)
        return result

    # बाकी intents...
    else:

        # ✅ 6. Fallback to Gemini
        speak("please wait")
        history_text = "\n".join([f"User: {x['user']}\nAssistant: {x['assistant']}" for x in context_history])
        prompt = f"Previous conversation:\n{history_text}\n\nCurrent command: {cmd}\nReturn short intelligent answer in English or Hindi."
        result = ask_gemini(prompt)
        return result
    
    
    

# return "I couldn't understand. Could you please elaborate?"


#     # ... बाकी intents जैसे open app, close app, google search
#     speak("थोड़ा सोचने दीजिए सर...")
#     return "I couldn't understand. Could you please elaborate?"

