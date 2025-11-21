import pyautogui
import pyperclip
import time
from voice_utils import speak

# Contacts (Hindi + English)
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

def get_contact_number(name):
    """Return number from contacts dict (Hindi/English)."""
    name = name.strip().lower()
    for key in contacts.keys():
        if name in key or key == name:
            return contacts[key]
    return None

def send_whatsapp_desktop(command):
    """
    Send message using WhatsApp Desktop app.
    command example: "ऋषभ को मैसेज भेजो कैसा है भाई"
    """
    try:
        import re

        # Extract contact and message
        pattern = r"(?:to|को)\s*([a-zA-Zअ-ह]+)\s*(?:message bhejo|मैसेज भेजो)?\s*(.*)"
        match = re.search(pattern, command.lower())
        if not match:
            return "❌ नाम या मैसेज सही से समझ नहीं आया।"

        name = match.group(1).strip()
        message = match.group(2).strip()
        number = get_contact_number(name)
        if not number:
            return f"❌ संपर्क '{name}' नहीं मिला।"
        if not message:
            return "❌ मैसेज खाली है।"

        speak(f"{name} को WhatsApp Desktop पर message भेजा जा रहा है...")

        # Open WhatsApp Desktop (user should keep it open)
        # Focus search bar
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'f')   # search bar
        time.sleep(0.5)

        # Type number via clipboard
        pyperclip.copy(number)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')  # Open chat

        # Type message via clipboard
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')  # Send message

        return f"✅ Message sent to {name}: '{message}'"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
