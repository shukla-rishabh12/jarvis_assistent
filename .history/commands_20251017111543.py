# Sare commands aur task execution functions
# commands.py
"""
commands.py
- Contains execute_task(command, speak) which:
    - matches user command using fuzzy matching AND keywords
    - executes appropriate action (open websites, apps, take screenshot, play song, notes etc.)
- At bottom: a small interactive test if run directly.
"""

import webbrowser
import os
import subprocess
from fuzzywuzzy import fuzz
import datetime
import wikipedia
import pyautogui
import psutil
import random
from playsound import playsound

# ---------- CONFIGURATION ----------
# If your songs/screenshot folders are in different location, update these paths.
# Use raw string r"..." on Windows paths to avoid backslash problems.
SONGS_FOLDER = "songs"           # relative to project folder (or set absolute path)
SCREENSHOT_FOLDER = "screenshots"  # relative folder for saving screenshots
POWERPOINT_PATH = r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"  # common path for Office 365
# -----------------------------------

def _ensure_folder(path):
    """Create folder if not exists (helper)."""
    if not os.path.exists(path):
        os.makedirs(path)

def execute_task(command: str, speak):
    """
    Main dispatcher function.
    - command: lowercased input string
    - speak: function to give voice feedback (e.g., speech_utils.speak)
    """
    if not command:
        return

    # ---------- WEBSITE COMMANDS (fuzzy keyword matching) ----------
    if fuzz.partial_ratio(command, "youtube") > 65 or "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
        return

    if fuzz.partial_ratio(command, "chatgpt") > 65 or "open chatgpt" in command:
        speak("Opening ChatGPT.")
        webbrowser.open("https://chat.openai.com")
        return

    if fuzz.partial_ratio(command, "whatsapp") > 65 or "open whatsapp" in command:
        speak("Opening WhatsApp Web.")
        webbrowser.open("https://web.whatsapp.com")
        return

    # Google search: "search data science"
    if command.startswith("search ") or " search " in command:
        # robustly extract query
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching Google for {query}.")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What should I search for?")
        return

    # ---------- WIKIPEDIA ----------
    if command.startswith("who is") or command.startswith("what is") or " wikipedia " in command or command.startswith("tell me about"):
        # try to extract topic
        topic = command.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
        if not topic:
            speak("Tell me the topic you want information about.")
            return
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except Exception as e:
            print("Wikipedia error:", e)
            speak("Sorry, I couldn't find information on that.")
        return

    # ---------- LOCAL APPS ----------
    # PowerPoint (path may differ on your PC). Try to open; if fail, inform user.
    if "powerpoint" in command or "open powerpoint" in command:
        speak("Opening PowerPoint.")
        try:
            subprocess.Popen(POWERPOINT_PATH)
        except Exception as e:
            print("Error opening PowerPoint:", e)
            speak("Couldn't open PowerPoint automatically. Please check the path in commands.py.")
        return

    if "notepad" in command:
        speak("Opening Notepad.")
        os.system("notepad")
        return

    if "calculator" in command or "calc" in command:
        speak("Opening Calculator.")
        try:
            subprocess.Popen("calc.exe")
        except Exception as e:
            print("Calculator error:", e)
            speak("Cannot open calculator on this system.")
        return

    if "command prompt" in command or "cmd" == command.strip():
        speak("Opening Command Prompt.")
        os.system("start cmd")
        return

    # ---------- TIME & DATE ----------
    if "time" in command and ("what" in command or "tell" in command or command.strip() == "time"):
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_str}.")
        return

    if "date" in command and ("what" in command or "tell" in command or command.strip() == "date"):
        date_str = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {date_str}.")
        return

    # ---------- SCREENSHOT ----------
    if "screenshot" in command or "take screenshot" in command:
        _ensure_folder(SCREENSHOT_FOLDER)
        filename = os.path.join(SCREENSHOT_FOLDER, f"screenshot_{int(datetime.datetime.now().timestamp())}.png")
        try:
            img = pyautogui.screenshot()
            img.save(filename)
            speak(f"Screenshot saved as {filename}")
        except Exception as e:
            print("Screenshot error:", e)
            speak("Could not take a screenshot.")
        return

    # ---------- PLAY SONG (first mp3 in folder) ----------
    if "play song" in command or "play music" in command or "music" in command:
        if not os.path.exists(SONGS_FOLDER):
            speak("Songs folder not found.")
            return
        songs = [f for f in os.listdir(SONGS_FOLDER) if f.lower().endswith(".mp3")]
        if not songs:
            speak("No mp3 files found in the songs folder.")
            return
        song_path = os.path.join(SONGS_FOLDER, songs[0])
        speak(f"Playing {songs[0]}")
        try:
            playsound(song_path)
        except Exception as e:
            print("Playsound error:", e)
            speak("Could not play the song. Check the file or player.")
        return

    # ---------- NOTES (simple save & read) ----------
    if "make a note" in command or "take a note" in command:
        speak("What should I write in the note?")
        # lazy import here to avoid circular import when testing
        from speech_utils import take_command
        note_text = take_command()
        if note_text:
            with open("notes.txt", "a", encoding="utf-8") as f:
                f.write(note_text + "\n")
            speak("Note saved.")
        else:
            speak("No note was taken.")
        return

    if "read note" in command or "read my notes" in command or "show notes" in command:
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r", encoding="utf-8") as f:
                content = f.read()
            if content.strip():
                speak("Reading your notes.")
                speak(content)
            else:
                speak("Your notes file is empty.")
        else:
            speak("You don't have any notes yet.")
        return

    # ---------- SYSTEM INFO ----------
    if "battery" in command:
        try:
            battery = psutil.sensors_battery()
            if battery:
                speak(f"Battery is at {battery.percent} percent.")
            else:
                speak("Battery information not available.")
        except Exception as e:
            print("Battery error:", e)
            speak("Could not fetch battery information.")
        return

    if "cpu" in command or "cpu usage" in command or "usage" in command:
        try:
            usage = psutil.cpu_percent(interval=1)
            speak(f"CPU usage is {usage} percent.")
        except Exception as e:
            print("CPU error:", e)
            speak("Could not fetch CPU usage.")
        return

    # ---------- JOKES / FUN ----------
    if "joke" in command or "tell me a joke" in command:
        jokes = [
            "Why did the computer go to therapy? Because it had a hard drive.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "I would tell you a UDP joke, but you might not get it."
        ]
        speak(random.choice(jokes))
        return

    # ---------- EXIT (with confirmation to avoid accidental stop) ----------
    if "exit" in command or "stop" in command or "shutdown assistant" in command:
        speak("Are you sure you want me to stop? Say yes to confirm.")
        from speech_utils import take_command
        confirmation = take_command()
        if "yes" in confirmation or "han" in confirmation or "haan" in confirmation:
            speak("Okay, shutting down. Goodbye!")
            # exit the whole program
            os._exit(0)
        else:
            speak("Continuing operation.")
        return

    # ---------- DEFAULT ----------
    speak("Sorry, I didn't understand that. Try a different command.")
    return

# small test when running this file directly:
if __name__ == "__main__":
    def local_speak(t): 
        print("[local_speak]", t)

    print("Test command dispatcher. Type a command (text) to simulate speech.")
    while True:
        try:
            cmd = input("Type command (or 'quit'): ").strip().lower()
            if cmd == "quit":
                break
            execute_task(cmd, local_speak)
        except KeyboardInterrupt:
            break
    print("Test ended.")
