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

import pyautogui
import pyperclip
import time

def send_whatsapp_desktop(contact_number, message):
    """
    WhatsApp Desktop ke search bar aur chat window ke through message bheje
    """
    try:
        # 1️⃣ WhatsApp Desktop open aur focused hona chahiye
        # Alt+Tab ya manually switch kar sakte ho

        # 2️⃣ Search bar focus
        pyautogui.hotkey('ctrl', 'f')  # search bar
        time.sleep(0.5)

        # 3️⃣ Contact number type karna via clipboard (taaki special chars safe rahe)
        pyperclip.copy(contact_number)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')  # chat open

        # 4️⃣ Message type
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')  # send

        return f"✅ Message sent to {contact_number}"

    except Exception as e:
        return f"⚠️ Error: {e}"
