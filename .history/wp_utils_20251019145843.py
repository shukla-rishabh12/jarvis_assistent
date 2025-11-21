import pywhatkit as kit
from voice_utils import speak
from ai_sense import ask_gemini
import datetime
import json
import re

# 📇 Contacts dictionary
contacts = {
    "ऋषभ": "+918127972296",
    "mom": "+91XXXXXXXXXX",
    "dad": "+91XXXXXXXXXX",
    "friend": "+91XXXXXXXXXX"
}

def send_whatsapp_via_gemini(user_command):
    try:
        speak("WhatsApp command detect hui, thoda wait kijiye...")

        # 1️⃣ Gemini se structured response le lo
        prompt = (
            f"User said: '{user_command}'. Extract WhatsApp info in JSON format: "
            "{contact, message, schedule (True/False), hour (if scheduled), minute (if scheduled)}. "
            "Only reply with JSON, no extra text or explanation."
        )
        gemini_response = ask_gemini(prompt)
        print("🧠 Gemini response (raw):", gemini_response)

        # 2️⃣ Clean response: remove ```json ... ``` etc.
        cleaned = re.sub(r"```.*?```", "", gemini_response, flags=re.DOTALL).strip()
        print("🧠 Cleaned JSON:", cleaned)

        # 3️⃣ Parse JSON
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            speak("सॉरी सर, Gemini से सही JSON format response नहीं आया।")
            print(f"❌ JSON parse error: {e}")
            return "Invalid Gemini response."

        contact_name = data.get("contact", "").strip()
        message_text = data.get("message", "").strip()
        schedule = data.get("schedule", False)
        hour = data.get("hour", None)
        minute = data.get("minute", None)

        # 4️⃣ Check contact
        if contact_name not in contacts:
            speak(f"सॉरी सर, मुझे {contact_name} नाम का contact नहीं मिला।")
            return f"Contact '{contact_name}' not found."

        number = contacts[contact_name]

        # 5️⃣ Send WhatsApp
        if schedule and hour is not None and minute is not None:
            speak(f"{contact_name} को आपका message {hour}:{minute} बजे भेजा जाएगा।")
            kit.sendwhatmsg(number, message_text, hour, minute, wait_time=15, tab_close=True)
            speak(f"{contact_name} को आपका message schedule कर दिया गया।")
            return f"WhatsApp message scheduled to {contact_name} at {hour}:{minute}"
        else:
            # Send in real-time (2 min delay)
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
