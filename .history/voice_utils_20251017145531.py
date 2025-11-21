import speech_recognition as sr
import pyttsx3
print('ram ram')
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)  # Reduce noise
        try:
            audio = r.listen(source, phrase_time_limit=7)  # Listen up to 7 sec
        except:
            return "Listening failed"

    try:
        command = r.recognize_google(audio, language="hi-IN")  # Hindi / Hinglish
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        return "Could not recognize your voice, please repeat."
    except sr.RequestError:
        return "Speech service not available."
