# Voice recognition & text-to-speech functions
# speech_utils.py
"""
speech_utils.py
- Functions:
    - speak(text): convert text to speech using pyttsx3
    - take_command(): listen from default microphone and return recognized text (lowercased)
- At bottom: a small test block to verify TTS and STT.
"""

import speech_recognition as sr
import pyttsx3
import sys

# Initialize TTS engine once (do not re-init multiple times)
_engine = pyttsx3.init()

def speak(text: str):
    """
    Speak the given text out loud and also print to console.
    - Uses pyttsx3 (offline TTS).
    - Keep this function lightweight.
    """
    try:
        print(f"[Assistant]: {text}")
        _engine.say(text)
        _engine.runAndWait()
    except Exception as e:
        # If TTS fails, at least print the text
        print("[TTS error]:", e)
        print(f"[Assistant]: {text}")

def take_command(timeout: int = 5, phrase_time_limit: int = 6) -> str:
    """
    Listen from the microphone and return recognized speech as lowercase string.
    - timeout: seconds to wait for phrase to start
    - phrase_time_limit: max seconds for the phrase
    - Uses Google's free speech-to-text via speech_recognition (requires internet).
    - Returns empty string on failure.
    """
    recognizer = sr.Recognizer()
    mic = None
    try:
        mic = sr.Microphone()  # default system microphone
    except Exception as e:
        print("Microphone not found or accessible:", e)
        return ""

    with mic as source:
        # reduce ambient noise for a short time (adjustable)
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print("Listening... (speak now)")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected (timeout).")
            return ""

    try:
        # recognize using Google Web Speech API (free, needs internet)
        text = recognizer.recognize_google(audio, language="en-in")  # en-in fits Hindi-English mix too
        print(f"[You]: {text}")
        return text.lower()
    except sr.UnknownValueError:
        # speech was unintelligible
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        # API was unreachable or unresponsive
        print("Could not request results from Google Speech Recognition service; check internet.", e)
        return ""
    except Exception as e:
        print("Unexpected STT error:", e)
        return ""

# Small test when run directly
if __name__ == "__main__":
    speak("Hello Rishabh. This is a test of the voice system. Please say something after the beep.")
    print("Now testing speech recognition. Please say: open youtube")
    result = take_command()
    if result:
        print("Recognized:", result)
    else:
        print("No speech recognized. Check microphone or internet.")
