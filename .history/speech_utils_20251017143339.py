import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    """Convert assistant text response to voice."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's voice and convert to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="hi-IN")
        return command
    except Exception:
        return "Sorry, I did not understand."
