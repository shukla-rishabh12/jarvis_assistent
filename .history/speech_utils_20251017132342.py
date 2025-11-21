# speech_utils.py
import speech_recognition as sr
import pyttsx3
import threading

engine = pyttsx3.init()
lock = threading.Lock()  # Prevent pyttsx3 runtime error

def speak(text):
    """Speak text safely with lock to prevent runtime errors."""
    with lock:
        engine.say(text)
        engine.runAndWait()

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
        text = r.recognize_google(audio, language="en-IN")  # Hindi/English mix
        print("Heard:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Speech service error:", e)
        return ""
