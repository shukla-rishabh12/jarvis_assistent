# wp_utils.py
import pywhatkit as kit
import datetime
import re
from voice_utils import speak

# Contacts dictionary (Hindi + English names map to same number)
contacts = {
    "rishabh": "+919696028302",
    "ऋषभ": "+919696028302",
    "harsh": "+918957198775",
    "हर्ष": "+918957198775",
    "rohan": "+916306704304",
    "रोहन": "+916306704304",
    "sakshi": "+919214218707",
    "साक्षी": "+919214218707"
}

def get_contact_number_smart(name):
    """Return phone number for a given contact name (Hindi/English)."""
    name = name.strip().lower()
    for key in contacts.keys():
        if name in key or key in name:
            return contacts[key]
    return None

def send_whatsapp_message(command):
    """
    Send WhatsApp Desktop message using pywhatkit.
    Command examples:
    - 'ऋषभ को मैसेज भेजो कैसा है भाई'
    - 'send message to Rishabh how are you'
    """
    try:
        # Extract contact name and message using regex
        pattern = r"(?:to|को)\s*([a-zA-Zअ-ह]+)\s*(?:message bhejo|मैसेज भेजो)?\s*(.*)"
        match = re.search(pattern, command.lower())
        if not match:
            return "❌ नाम या मैसेज सही से समझ नहीं आया।"

        name = match.group(1).strip()
        message = match.group(2).strip()

        phone = get_contact_number_smart(name)
        if not phone:
            return f"❌ संपर्क '{name}' नहीं मिला।"

        if not message:
            return "❌ कृपया मैसेज बताइए क्या भेजना है।"

        # Schedule message 1 min ahead
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute + 1
        if minute >= 60:
            minute -= 60
            hour = (hour + 1) % 24

        speak(f"{name} को WhatsApp संदेश भेजा जा रहा है: '{message}'")
        kit.sendwhatmsg(phone, message, hour, minute, wait_time=10, tab_close=True)

        return f"✅ '{name}' को WhatsApp संदेश भेजा जा रहा है: '{message}'"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
