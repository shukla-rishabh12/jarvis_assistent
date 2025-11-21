import pyautogui
import pyperclip
import time
from voice_utils import speak

# Contacts dictionary (Hindi + English)
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
    """Return contact number from English/Hindi name"""
    name = name.strip().lower()
    for key in contacts.keys():
        if name == key.lower() or name in key.lower():
            return contacts[key]
    return None

def send_whatsapp_desktop(contact_name, message_text):
    """Send message to WhatsApp Desktop"""
    try:
        number = get_contact_number(contact_name)
        if not number:
            return f"❌ Contact '{contact_name}' not found."

        if not message_text:
            return "❌ Message is empty."

        speak(f"{contact_name} को WhatsApp Desktop पर message भेजा जा रहा है...")

        # Focus WhatsApp Desktop search bar
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'f')  # Search bar
        time.sleep(0.5)

        # Type contact number via clipboard
        pyperclip.copy(number)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')  # Open chat

        # Type message via clipboard
        pyperclip.copy(message_text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')  # Send message

        return f"✅ Message sent to {contact_name}: '{message_text}'"

    except Exception as e:
        return f"⚠️ Error sending WhatsApp message: {str(e)}"
