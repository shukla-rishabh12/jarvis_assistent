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
import pyautogui
import pyperclip
import time
from voice_utils import speak
from ai_sense import ask_gemini

import json, re

def send_whatsapp_via_gemini(user_command):
    try:
        speak("WhatsApp command detect hui, thoda wait kijiye...")

        # 1️⃣ Gemini se structured response le lo
        prompt = (
            f"User said: '{user_command}'. Extract WhatsApp info in JSON format: "
            "{contact, message}. Only reply with JSON, no extra text."
        )
        gemini_response = ask_gemini(prompt)
        print("🧠 Gemini response (raw):", gemini_response)

        # 2️⃣ Clean JSON
        cleaned = re.sub(r"^```json\s*|\s*```$", "", gemini_response, flags=re.DOTALL).strip()
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            speak("सॉरी सर, Gemini से सही JSON format response नहीं आया।")
            return "Invalid Gemini response."

        contact_name = data.get("contact", "").strip()
        message_text = data.get("message", "").strip()

        # 3️⃣ Lookup number
        number = contacts.get(contact_name)
        if not number:
            speak(f"सॉरी सर, मुझे {contact_name} नाम का contact नहीं मिला।")
            return f"Contact '{contact_name}' not found."

        speak(f"{contact_name} को आपका message भेजा जा रहा है...")

        # 4️⃣ PyAutoGUI send (WhatsApp Desktop)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        pyperclip.copy(number)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        pyperclip.copy(message_text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')

        speak(f"{contact_name} को आपका message भेज दिया गया।")
        return f"Message sent to {contact_name} ({number})"

    except Exception as e:
        speak("सॉरी सर, WhatsApp भेजने में समस्या आ गई।")
        print(f"❌ Error: {e}")
        return f"Error sending WhatsApp message: {e}"
