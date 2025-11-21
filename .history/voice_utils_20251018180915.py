import speech_recognition as sr
import pyttsx3

print("🔊 Voice engine loading...")

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# ✅ Set Hindi/Indian male voice
for voice in voices:
    if "heera" in voice.name.lower() or "ravi" in voice.name.lower() or "india" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 160)   # Slightly faster
engine.setProperty('volume', 1)

def speak(text):
    """Speaks text in chunks for smoother delivery."""
    if not text:
        return
    print("🗣️ Speaking:", text)
    # Long text ko 2-2 lines me bolne ke liye
    parts = text.split(". ")
    for part in parts:
        engine.say(part.strip())
        engine.runAndWait()

def listen():
    """Listens Hindi + English commands"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening... (Hindi/English supported)")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, phrase_time_limit=7)
        except Exception as e:
            return "Listening failed"

    try:
        command = r.recognize_google(audio, language="hi-IN")  # 👈 Hindi-optimized
        print("🗣️ You said:", command)
        return command
    except sr.UnknownValueError:
        speak("माफ कीजिए, मैं समझ नहीं पाया। कृपया दोबारा बोलें।")
        return "Could not recognize"
    except sr.RequestError:
        speak("सर्वर से कनेक्शन नहीं हो पाया।")
        return "Speech service not available."
