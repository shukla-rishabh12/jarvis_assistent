
# Python `json.loads()` ko ye extra \`\`\` aur "json" word samajh nahi aate. Solution: **Gemini response ko clean karo**, sirf `{ ... }` part hi `json.loads()` me bhejna.  

# `wp_utils.py` me modify karein:

# ```python
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
    """
    Send WhatsApp message using voice command interpreted by Gemini.
    Gemini will return:
        {
            "contact": "Rishabh",
            "message": "Hello, kaise ho?",
            "schedule": True/False,
            "hour": 16,     # optional if schedule=True
            "minute": 30    # optional if schedule=True
        }
    """
    try:
        # 1️⃣ Gemini se structured response le lo
        prompt = (
            f"User said: '{user_command}'. Extract WhatsApp info in JSON format: "
            "{contact, message, schedule (True/False), hour (if scheduled), minute (if scheduled)}. "
            "Only reply with JSON."
        )
        gemini_response = ask_gemini(prompt)
        print("🧠 Gemini response (raw):", gemini_response)

        # 2️⃣ Convert response to dictionary safely
        import json
        try:
            data = json.loads(gemini_response)
        except:
            speak("सॉरी सर, Gemini से सही format response नहीं आया।")
            return "Invalid Gemini response."

        contact_name = data.get("contact", "").lower().strip()
        message_text = data.get("message", "")
        schedule = data.get("schedule", False)
        hour = data.get("hour", None)
        minute = data.get("minute", None)

        print("🧠 Cleaned JSON:", data)

        # 3️⃣ Check contact
        if contact_name not in contacts:
            speak(f"सॉरी सर, मुझे {contact_name} नाम का contact नहीं मिला।")
            return f"Contact '{contact_name}' not found."

        number = contacts[contact_name]

        # 4️⃣ Send WhatsApp
        if schedule:
            if hour is None or minute is None:
                speak("सॉरी सर, schedule time सही नहीं दिया गया।")
                return "Invalid schedule time."
            speak(f"{contact_name} को आपका message {hour}:{minute} बजे भेजा जाएगा।")
            print(f"📱 Scheduling WhatsApp message to {number} at {hour}:{minute}...")
            kit.sendwhatmsg(number, message_text, hour, minute, wait_time=15, tab_close=True)
            speak(f"{contact_name} को आपका message schedule कर दिया गया।")
            return f"WhatsApp message scheduled to {contact_name} at {hour}:{minute}"
        else:
            # ✅ Send in real-time (after 2 minute delay to avoid pywhatkit error)
            now = datetime.datetime.now()
            hr = now.hour
            mn = now.minute + 2
            if mn >= 60:
                mn -= 60
                hr = (hr + 1) % 24

            speak(f"{contact_name} को आपका message turant bheja ja raha hai...")
            print(f"📱 Sending WhatsApp message to {number} at {hr}:{mn} (real-time)...")
            kit.sendwhatmsg(number, message_text, hr, mn, wait_time=15, tab_close=True)
            speak(f"{contact_name} को आपका message भेज दिया गया।")
            return f"WhatsApp message sent to {contact_name} in real-time"

    except Exception as e:
        speak("सॉरी सर, WhatsApp भेजने में समस्या आ गई।")
        print(f"❌ Error sending WhatsApp message: {e}")
        return f"Error sending WhatsApp message: {e}"
