# speech_utils.py
import speech_recognition as sr
import pyttsx3
import threading

engine = pyttsx3.init()

def speak(text):
    """Speak text (non-blocking)."""
    def _s():
        engine.say(text)
        engine.runAndWait()
    t = threading.Thread(target=_s, daemon=True)
    t.start()

def listen(timeout=6, phrase_time_limit=8):
    """Listen from default microphone. Returns recognized text or ''."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except Exception as e:
            print("Listening timeout/failed:", e)
            return ""
    try:
        # Use language="en-IN" for bilingual accuracy; recognizer will still capture Hindi+English
        text = r.recognize_google(audio, language="en-IN")
        print("Heard:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Speech service error:", e)
        return ""
