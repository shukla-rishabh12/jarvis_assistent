import re
import json
from voice_utils import speak
from ai_sense import ask_gemini
from wp_utils import send_whatsapp_desktop

def send_whatsapp_via_gemini(user_command):
    """
    Voice command -> Gemini -> exact contact in English -> send WhatsApp Desktop message
    """
    try:
        speak("WhatsApp command detect hui, Gemini se exact contact nikal raha hoon...")

        # Gemini prompt for JSON output
        prompt = (
            f"User said: '{user_command}'. Extract WhatsApp info in JSON format: "
            "{contact (exact English name as in contacts), message}. Only reply with JSON."
        )
        gemini_response = ask_gemini(prompt)
        print("🧠 Gemini response (raw):", gemini_response)

        # Clean JSON
        cleaned = re.sub(r"^```json\s*|\s*```$", "", gemini_response, flags=re.DOTALL).strip()
        print("🧠 Cleaned JSON:", cleaned)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            speak("सॉरी सर, Gemini se valid JSON response nahi aaya.")
            print(f"❌ JSON parse error: {e}")
            return "Invalid Gemini response."

        contact_name = data.get("contact", "").strip()
        message_text = data.get("message", "").strip()

        # Send via WhatsApp Desktop
        contact_name = data.get("contact", "").strip().lower()
        result = send_whatsapp_desktop(contact_name, message_text)
        speak(result)
        print("✅ WhatsApp Desktop Result:", result)
        return result

    except Exception as e:
        speak("सॉरी सर, WhatsApp bhejne mein problem aa gayi.")
        print(f"❌ Error: {e}")
        return f"Error: {e}"
