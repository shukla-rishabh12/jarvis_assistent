import pywhatkit as kit
from ai_sense import ask_gemini
from voice_utils import speak

def perform_web_action(user_input):
    prompt = f"""
    User said: '{user_input}'.
    Decide the action type and target.
    Options:
      1. Play a YouTube video
      2. Perform a Google search
      3. Send a WhatsApp message
    Reply in one of these formats only:
      - "youtube: <video name>"
      - "google: <search query>"
      - "whatsapp: <number>, <message>, <hour>, <minute>"
    """

    action = ask_gemini(prompt).lower().strip()
    print("Gemini Response:", action)

    try:
        if action.startswith("youtube:"):
            video_name = action.split("youtube:")[1].strip() or "latest trending"
            speak(f"{video_name} YouTube पर चलाया जा रहा है...")
            kit.playonyt(video_name)
            speak(f"{video_name} YouTube पर खुल गया।")
            return f"🎬 Playing {video_name} on YouTube"

        elif action.startswith("google:"):
            query = action.split("google:")[1].strip() or "latest news"
            speak(f"{query} के लिए Google पर खोज की जा रही है...")
            kit.search(query)
            speak(f"{query} के लिए परिणाम Google पर खुल गए हैं।")
            return f"🔍 Searching for '{query}' on Google"

        elif action.startswith("whatsapp:"):
            parts = action.replace("whatsapp:", "").strip().split(",")
            if len(parts) < 4:
                speak("WhatsApp संदेश के लिए समय या नंबर पूरा नहीं है।")
                return "❌ Incomplete WhatsApp message details."

            number = parts[0].strip()
            message = parts[1].strip()
            hour = int(parts[2].strip())
            minute = int(parts[3].strip())

            speak(f"WhatsApp पर {number} को संदेश भेजा जा रहा है...")
            kit.sendwhatmsg(number, message, hour, minute)
            speak(f"{number} को संदेश भेज दिया गया है।")
            return f"💬 WhatsApp message sent to {number}"

        else:
            speak("मुझे यह समझ नहीं आया कि क्या करना है।")
            return f"🤔 Could not determine action from: {user_input}"

    except Exception as e:
        speak("किसी कारणवश यह कार्य नहीं हो सका।")
        return f"⚠️ Error performing action: {e}"
