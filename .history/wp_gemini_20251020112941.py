import re
import json
from voice_utils import speak
from ai_sense import ask_gemini
from wp_utils import send_whatsapp_desktop

def send_whatsapp_via_gemini(user_command):
    """
    Process voice command via Gemini, get exact contact name in English,
    then send message via WhatsApp Desktop
    """
    try:
        speak("WhatsApp command detect hui, thoda wait kijiye...")

        prompt = (
            f"User said: '{user_command}'. Extract WhatsApp info in JSON format: "
            "{contact (return in English exactly as in contacts), message}. "
            "Only reply with JSON, no extra text or explanation."
        )
        gemini_response = ask_gemini(prompt)
        print("🧠 Gemini response (raw):", gemini_response)

        # Clean JSON response
        cleaned = re.sub(r"^```json\s*|\s*```$", "", gemini_response, flags=re.DOTALL).strip()
        print("🧠 Cleaned JSON:", cleaned)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            speak("सॉरी सर, Gemini से सही JSON format response नहीं आया।")
            print(f"❌ JSON parse error: {e}")
            return "Invalid Gemini response."

        contact_name = data.get("contact", "").strip()
        message_text = data.get("message", "").strip()

        # Send via WhatsApp Desktop
        result = send_whatsapp_desktop(contact_name, message_text)
        speak(result)
        print("✅ WhatsApp Desktop Result:", result)
        return result

    except Exception as e:
        speak("सॉरी सर, WhatsApp भेजने में समस्या आ गई।")
        print(f"❌ Error: {e}")
        return f"Error: {e}"
