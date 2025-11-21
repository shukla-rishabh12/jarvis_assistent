import pywhatkit as kit
from voice_utils import speak
import datetime

# 📇 Contacts dictionary (Name → Number)
contacts = {
    "rishabh": "+918127972296",
    "mom": "+91XXXXXXXXXX",
    "dad": "+91XXXXXXXXXX",
    "friend": "+91XXXXXXXXXX"
}

# ------------------- YouTube -------------------
def play_youtube(video_name):
    """Play YouTube video (Hindi/English input supported)."""
    try:
        if not video_name:
            video_name = "latest trending"
        speak(f"ठीक है सर, YouTube पर '{video_name}' चलाया जा रहा है।")
        print(f"🎬 Playing '{video_name}' on YouTube...")
        kit.playonyt(video_name)
        return f"Playing '{video_name}' on YouTube"
    except Exception as e:
        speak("सॉरी सर, YouTube खोलने में समस्या आ गई।")
        print(f"❌ Error opening YouTube: {e}")
        return f"Error opening YouTube: {e}"

# ------------------- Google Search -------------------
def google_search(query):
    """Search on Google (Hindi/English input supported)."""
    try:
        if not query:
            query = "latest news"
        speak(f"ठीक है सर, Google पर '{query}' खोजा जा रहा है।")
        print(f"🔍 Searching '{query}' on Google...")
        kit.search(query)
        return f"Searching for '{query}' on Google"
    except Exception as e:
        speak("सॉरी सर, Google search करने में समस्या आ गई।")
        print(f"❌ Error searching Google: {e}")
        return f"Error searching Google: {e}"

# ------------------- WhatsApp -------------------
def send_whatsapp_msg(name, message, schedule=False, hour=None, minute=None):
    """
    Send WhatsApp message using contact name.
    - name: contact name (str)
    - message: message text (str)
    - schedule: if True, use provided hour & minute, else send in real-time
    - hour, minute: schedule time (int)
    """
    try:
        name = name.lower().strip()
        if name not in contacts:
            speak(f"सॉरी सर, मुझे {name} नाम का contact नहीं मिला।")
            return f"Contact '{name}' not found."

        number = contacts[name]

        if schedule:
            if hour is None or minute is None:
                speak("सॉरी सर, schedule time सही नहीं दिया गया।")
                return "Invalid schedule time."
            speak(f"{name} को आपका मैसेज {hour}:{minute} बजे भेजा जाएगा।")
            print(f"📱 Scheduling WhatsApp message to {number} at {hour}:{minute}...")
            kit.sendwhatmsg(number, message, hour, minute)
            speak(f"{name} को आपका मैसेज schedule कर दिया गया।")
            return f"WhatsApp message scheduled to {name} at {hour}:{minute}"
        else:
            # Send in real-time (after 1 minute delay)
            now = datetime.datetime.now()
            hr = now.hour
            mn = now.minute + 1  # pywhatkit requires at least 1 minute later
            speak(f"{name} को आपका मैसेज turant भेजा जा रहा है...")
            print(f"📱 Sending WhatsApp message to {number} at {hr}:{mn} (real-time)...")
            kit.sendwhatmsg(number, message, hr, mn)
            speak(f"{name} को आपका मैसेज भेज दिया गया।")
            return f"WhatsApp message sent to {name} in real-time"
    except Exception as e:
        speak("सॉरी सर, WhatsApp message भेजने में समस्या आ गई।")
        print(f"❌ Error sending WhatsApp message: {e}")
        return f"Error sending WhatsApp message: {e}"
