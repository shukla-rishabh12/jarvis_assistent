print('Jai Shree Ram')

"""
main.py
- Entry point for the intelligent voice assistant (Jarvis v2).
- Uses fuzzy meaning-based matching instead of just keywords.
- Imports 'speak' and 'take_command' from speech_utils, and 'execute_task' from commands.
"""

from speech_utils import speak, take_command
from commands import execute_task
from fuzzywuzzy import fuzz

def meaning_match(user_input, keywords):
    """
    Checks if user_input semantically matches any keyword (Hindi + English).
    """
    for key in keywords:
        if fuzz.partial_ratio(user_input.lower(), key.lower()) > 70:
            return True
    return False


def main():
    speak("Hey Rishabh, I am ready. Say your command.")
    while True:
        command = take_command()

        if not command:
            continue  # nothing recognized

        # Exit conditions
        if meaning_match(command, [
            "exit", "stop", "goodbye", "band ho jao", "close yourself", "bye jarvis", "nikal jao"
        ]):
            speak("Goodbye Rishabh! Have a great day.")
            break

        # Otherwise, pass command for execution
        execute_task(command, speak)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAssistant stopped by user.")
        speak("Goodbye! See you soon.")
