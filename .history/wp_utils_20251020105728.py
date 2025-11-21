import json
import re
import time
import pyautogui
import pyperclip
import subprocess
from ai_sense import ask_gemini
from voice_utils import speak

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


def send_whatsapp_desktop_via_gemini(user_command):
    try:
        prompt = (
            f"User said: '{user_command}'. Extract WhatsApp info in JSON format: "
            "{contact, message}. Only reply with JSON, no explanation."
        )
        gemini_response = ask_gemini(prompt)
        print("🧠 Gemini Response:", gemini_response)

        cleaned = re.sub(r"^```json\s*|\s*```$", "", gemini_response.strip(), flags=re.DOTALL)
        data = json.loads(cleaned)

        contact_name = data.get("contact", "").strip()
        message_text = data.get("message", "").strip()

        if not contact_name or not message_text:
            speak("सॉरी सर, Gemini से पूरा डेटा नहीं मिला।")
            return "Incomplete data from Gemini."

        if contact_name not in contacts:
            speak(f"सॉरी सर, मुझे {contact_name} नाम का contact नहीं मिला।")
            return f"Contact '{contact_name}' not found."

        contact = contacts[contact_name]
        speak(f"WhatsApp Desktop खोल रहा हूँ और {contact_name} को message भेज रहा हूँ...")

        subprocess.Popen(["cmd", "/c", "start", "whatsapp://"])
        time.sleep(5)

        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyperclip.copy(contact)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")

        time.sleep(2)
        pyperclip.copy(message_text)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")

        speak(f"{contact_name} को message भेज दिया गया है सर।")
        return f"✅ WhatsApp message sent to {contact_name}"

    except Exception as e:
        speak("सॉरी सर, WhatsApp message भेजने में दिक्कत आ गई।")
        print(f"❌ Error: {e}")
        return f"❌ Error: {e}"
