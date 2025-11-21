# speech_utils.py
import speech_recognition as sr
import pyttsx3

# TTS engine
engine = pyttsx3.init()

def speak(text):
    """Text to speech"""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen to user's voice and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError:
        print("Service error.")
        return ""
