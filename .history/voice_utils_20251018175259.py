import speech_recognition as sr
import pyttsx3

print("🟢 Voice engine initializing...")

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Find and set best Hindi/Indian voice
selected = False
for voice in voices:
    if "microsoft heera" in voice.name.lower() or "ravi" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

if not selected:
    print("⚠️ Hindi voice not found, using default voice.")
else:
    print("✅ Hindi/Indian voice selected successfully.")

# Adjust rate and volume
engine.setProperty('rate', 145)   # थोड़ा slow बोलने के लिए
engine.setProperty('volume', 1)

def speak(text: str):
    """
    बोलकर output दे
    """
    print(f"🗣️ Speaking: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

def listen():
    """
    माइक्रोफोन से user command सुने
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening... (Hindi/English supported)")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, phrase_time_limit=7)
        except Exception:
            speak("मुझे आपकी आवाज़ नहीं सुनाई दी।")
            return "Listening failed"

    try:
        command = r.recognize_google(audio, language="en-IN")  # Hinglish friendly
        print("🗣️ You said:", command)
        return command
    except sr.UnknownValueError:
        speak("माफ कीजिए, मैं समझ नहीं पाया। कृपया दोबारा बोलें।")
        return "Could not recognize your voice, please repeat."
    except sr.RequestError:
        speak("नेटवर्क की समस्या है, कृपया बाद में कोशिश करें।")
        return "Speech service not available."
