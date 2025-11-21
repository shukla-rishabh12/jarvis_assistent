# voice_utils.py

import speech_recognition as sr
import pyttsx3

print("Ram Ram! Voice module loaded.")

# Initialize TTS engine
engine = pyttsx3.init()

# Set Hindi-friendly voice
voices = engine.getProperty('voices')
hindi_voice_found = False

for voice in voices:
    # Check for Hindi-compatible voice
    if "hindi" in voice.name.lower() or "male" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        hindi_voice_found = True
        break

if not hindi_voice_found:
    print("⚠️ Hindi voice not found, default voice will be used.")

# Set speaking rate and volume
engine.setProperty('rate', 150)   # Speech speed (words per minute)
engine.setProperty('volume', 1)   # Max volume

# Function to make assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen from mic
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (Hindi/English supported)")
        r.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
        try:
            audio = r.listen(source, phrase_time_limit=7)  # Listen max 7 seconds
        except:
            return "Listening failed"

    try:
        # Recognize speech in English (Hinglish supported)
        command = r.recognize_google(audio, language="en-IN")
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        return "Could not recognize your voice, please repeat."
    except sr.RequestError:
        return "Speech service not available."
