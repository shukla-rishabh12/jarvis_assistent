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

import pyautogui
import pyperclip
import time
import subprocess
from voice_utils import speak
from ai_sense import ask_gemini
import re, json
import os

# Contacts dictionary (English + Hindi keys)
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

def send_whatsapp_desktop(contact_name, message_text):
    try:
        speak("WhatsApp Desktop खोल रहा हूँ सर...")
        
        # 1️⃣ Open WhatsApp Desktop
        # Windows में path check करो, default usually:
        # wp_path = False
        # if not os.path.exists(wp_path):
            # अगर path गलत है, सिर्फ start menu से try करो
        subprocess.Popen(["cmd", "/c", "start", "whatsapp://"])
        # else:
        #     subprocess.Popen([wp_path])
        # time.sleep(5)  # wait for WhatsApp to open

        speak(f"{contact_name} को आपका message भेज रहा हूँ...")

        # 2️⃣ Search contact
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        pyperclip.copy(contact_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(0.5)

        # 3️⃣ Paste message
        pyperclip.copy(message_text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')

        speak(f"{contact_name} को आपका message भेज दिया गया।")
        return f"Message sent to {contact_name}"

    except Exception as e:
        speak("सॉरी सर, WhatsApp Desktop पर भेजने में समस्या आ गई।")
        print(f"❌ Error: {e}")
        return f"Error sending WhatsApp message: {e}"

def send_whatsapp_via_gemini(user_command):
    try:
        speak("WhatsApp command detect hui, Gemini से exact contact निकाल रहा हूँ...")

        # Gemini prompt
        prompt = (
            f"User said: '{user_command}'. Extract WhatsApp info in JSON format: "
            "{contact (exact English name as in contacts), message}. Only reply with JSON."
        )
        gemini_response = ask_gemini(prompt)
        print("🧠 Gemini response (raw):", gemini_response)

        # Clean JSON
        cleaned = re.sub(r"^```json\s*|\s*```$", "", gemini_response, flags=re.DOTALL).strip()
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            speak("सॉरी सर, Gemini से सही JSON response नहीं आया।")
            print(f"❌ JSON parse error: {e}")
            return "Invalid Gemini response."

        contact_name = data.get("contact", "").strip()
        message_text = data.get("message", "").strip()

        # Send via Desktop
        result = send_whatsapp_desktop(contact_name, message_text)
        print("✅ WhatsApp Result:", result)
        return result

    except Exception as e:
        speak("सॉरी सर, WhatsApp भेजने में समस्या आ गई।")
        print(f"❌ Error: {e}")
        return f"Error: {e}"
