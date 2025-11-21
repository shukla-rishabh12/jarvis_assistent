import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Select Hindi-friendly voice if available
for voice in voices:
    if "hindi" in voice.name.lower() or "male" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (Hindi/English supported)")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, phrase_time_limit=7)
        except:
            return "Listening failed"

    try:
        command = r.recognize_google(audio, language="en-IN")
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        return "Could not recognize your voice, please repeat."
    except sr.RequestError:
        return "Speech service not available."
