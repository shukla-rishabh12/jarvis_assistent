import pywhatkit as kit
from voice_utils import speak

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

def send_whatsapp_msg(number, message, hour, minute):
    """Send WhatsApp message (Hindi/English input supported)."""
    try:
        speak(f"ठीक है सर, {number} पर व्हाट्सएप मैसेज भेजा जा रहा है।")
        print(f"📱 Scheduling WhatsApp message to {number} at {hour}:{minute}...")
        kit.sendwhatmsg(number, message, hour, minute)
        speak(f"{number} पर आपका मैसेज schedule कर दिया गया है।")
        return f"WhatsApp message scheduled to {number}"
    except Exception as e:
        speak("सॉरी सर, WhatsApp message भेजने में समस्या आ गई।")
        print(f"❌ Error sending WhatsApp message: {e}")
        return f"Error sending WhatsApp message: {e}"
