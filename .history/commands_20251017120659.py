import speech_recognition as sr
import pyttsx3
import wikipediaapi
import os
import webbrowser
from fuzzywuzzy import fuzz

# Initialize main components
engine = pyttsx3.init()
recognizer = sr.Recognizer()
wiki = wikipediaapi.Wikipedia('en')

def speak(text):
    print(f"[Assistant]: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="en-IN")
        print(f"[You]: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your internet.")
        return ""

def meaning_match(text, keywords):
    """Returns True if user's text means the same as the intent (approx)."""
    for keyword in keywords:
        if fuzz.partial_ratio(keyword.lower(), text.lower()) > 70:
            return True
    return False

# Main loop
while True:
    query = listen()

    if query == "":
        continue

    # Exit / Stop
    if meaning_match(query, ["exit", "stop", "goodbye", "band ho jao", "close yourself"]):
        speak("Goodbye Rishabh! Have a great day.")
        break

    # Open Notepad
    elif meaning_match(query, ["open notepad", "notepad kholo", "mujhe notepad chahiye", "start notepad"]):
        speak("Opening Notepad for you.")
        os.system("notepad")

    # Open YouTube
    elif meaning_match(query, ["open youtube", "youtube kholo", "start youtube", "play videos"]):
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    # Open Google
    elif meaning_match(query, ["open google", "google kholo", "search on google"]):
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    # Wikipedia Search
    elif meaning_match(query, ["who is", "what is", "tell me about", "ke bare me batao", "information about"]):
        topic = query.replace("who is", "").replace("what is", "").replace("tell me about", "").replace("ke bare me batao", "").strip()
        if topic:
            speak(f"Searching Wikipedia for {topic}")
            page = wiki.page(topic)
            if page.exists():
                speak(page.summary[:500])
            else:
                speak("Sorry, I couldn't find information on that.")
        else:
            speak("Please say the topic name clearly.")

    # Play Music
    elif meaning_match(query, ["play music", "gaana chalao", "music kholo"]):
        music_dir = "C:\\Users\\Public\\Music"
        songs = os.listdir(music_dir)
        if songs:
            speak("Playing music.")
            os.startfile(os.path.join(music_dir, songs[0]))
        else:
            speak("No songs found in your music directory.")

    # Fallback
    else:
        speak("Sorry, I didn't understand that. Try saying it differently.")
