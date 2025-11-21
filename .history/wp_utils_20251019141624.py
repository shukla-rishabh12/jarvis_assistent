
Python `json.loads()` ko ye extra \`\`\` aur "json" word samajh nahi aate. Solution: **Gemini response ko clean karo**, sirf `{ ... }` part hi `json.loads()` me bhejna.  

`wp_utils.py` me modify karein:

```python
import pywhatkit as kit
from voice_utils import speak
from ai_sense import ask_gemini
import datetime
import json
import re  # ✅ For cleaning Gemini response

contacts = {
    "ऋषभ": "+91XXXXXXXXXX",
    "mom": "+91XXXXXXXXXX",
    "dad": "+91XXXXXXXXXX",
    "friend": "+91XXXXXXXXXX"
}

def send_whatsapp_via_gemini(user_command):
    try:
        prompt = (
            f"User said: '{user_command}'. Extract WhatsApp info in JSON format: "
            "{contact, message, schedule (True/False), hour (if scheduled), minute (if scheduled)}. "
            "Only reply with JSON, no extra text or backticks."
        )
        gemini_response = ask_gemini(prompt)
        print("🧠 Gemini response (raw):", gemini_response)

        # ---------------- Clean Gemini output ----------------
        # Remove backticks, code blocks, "json" word, etc.
        cleaned = re.search(r'\{.*\}', gemini_response, re.DOTALL)
        if not cleaned:
            speak("सॉरी सर, Gemini से JSON response सही नहीं आया।")
            return "Invalid Gemini response."
        data = json.loads(cleaned.group())
        print("🧠 Cleaned JSON:", data)

        contact_name = data.get("contact", "").strip()
        message_text = data.get("message", "")
        schedule = data.get("schedule", False)
        hour = data.get("hour", None)
        minute = data.get("minute", None)

        if contact_name not in contacts:
            speak(f"सॉरी सर, मुझे {contact_name} नाम का contact नहीं मिला।")
            return f"Contact '{contact_name}' not found."

        number = contacts[contact_name]

        if schedule:
            if hour is None or minute is None:
                speak("सॉरी सर, schedule time सही नहीं दिया गया।")
                return "Invalid schedule time."
            speak(f"{contact_name} को आपका message {hour}:{minute} बजे भेजा जाएगा।")
            print(f"📱 Scheduling WhatsApp message to {number} at {hour}:{minute}...")
            kit.sendwhatmsg(number, message_text, hour, minute)
            speak(f"{contact_name} को आपका message schedule कर दिया गया।")
            return f"WhatsApp message scheduled to {contact_name} at {hour}:{minute}"
        else:
            now = datetime.datetime.now()
            hr = now.hour
            mn = now.minute + 1
            speak(f"{contact_name} को आपका message turant भेजा जा रहा है...")
            print(f"📱 Sending WhatsApp message to {number} at {hr}:{mn} (real-time)...")
            kit.sendwhatmsg(number, message_text, hr, mn)
            speak(f"{contact_name} को आपका message भेज दिया गया।")
            return f"WhatsApp message sent to {contact_name} in real-time"

    except Exception as e:
        speak("सॉरी सर, WhatsApp भेजने में समस्या आ गई।")
        print(f"❌ Error sending WhatsApp message: {e}")
        return f"Error sending WhatsApp message: {e}"
