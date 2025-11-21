import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import tempfile
import os
import time

# 🎤 Jarvis-style Hindi+English speaking system
def speak(text, lang="hi"):
    """Speak text naturally in Hindi (Jarvis-style)."""
    if not text:
        return
    print(f"\n🧠 Jarvis: {text}\n")
    
    # Break long text into smaller parts for natural pauses
    parts = text.split(". ")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        try:
            # Temporary mp3 file for gTTS
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            fp.close()
            tts = gTTS(text=part, lang=lang)
            tts.save(fp.name)
            playsound(fp.name)
            os.remove(fp.name)
        except Exception as e:
            print(f"[Error speaking]: {e}")
        
        time.sleep(0.3)  # Small pause between lines

# 🎧 Voice recognition (Hindi + English)
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening... (Hindi/English supported)")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, phrase_time_limit=7)
        except Exception as e:
            print(f"[Listen Error]: {e}")
            return "Listening failed"

    try:
        command = r.recognize_google(audio, language="hi-IN")
        print("🗣️ You said:", command)
        return command
    except sr.UnknownValueError:
        speak("कृपया दोबारा बोलिए सर।")
        return "Could not recognize"
    except sr.RequestError:
        speak("सर्वर से कनेक्शन नहीं हो पा रहा।")
        return "Speech service not available."





# import speech_recognition as sr
# import pyttsx3

# print("🔊 Voice engine loading...")

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')

# # ✅ Set Hindi/Indian male voice
# for voice in voices:
#     if "heera" in voice.name.lower() or "ravi" in voice.name.lower() or "india" in voice.name.lower():
#         engine.setProperty('voice', voice.id)
#         break

# engine.setProperty('rate', 160)   # Slightly faster
# engine.setProperty('volume', 1)

# def speak(text):
#     """Speaks text in chunks for smoother delivery."""
#     if not text:
#         return
#     print("🗣️ Speaking:", text)
#     # Long text ko 2-2 lines me bolne ke liye
#     parts = text.split(". ")
#     for part in parts:
#         engine.say(part.strip())
#         engine.runAndWait()

# def listen():
#     """Listens Hindi + English commands"""
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("🎧 Listening... (Hindi/English supported)")
#         r.adjust_for_ambient_noise(source, duration=1)
#         try:
#             audio = r.listen(source, phrase_time_limit=7)
#         except Exception as e:
#             return "Listening failed"

#     try:
#         command = r.recognize_google(audio, language="hi-IN")  # 👈 Hindi-optimized
#         print("🗣️ You said:", command)
#         return command
#     except sr.UnknownValueError:
#         speak("pls say again।")
#         return "Could not recognize"
#     except sr.RequestError:
#         speak("server connection na ho paya।")
#         return "Speech service not available."
