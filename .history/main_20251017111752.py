print('jai shree ram')
# main.py
"""
main.py
- Entry point for the voice assistant.
- It imports speak and take_command from speech_utils and execute_task from commands.
- Run this file to start the full assistant (listening loop).
"""

from speech_utils import speak, take_command
from commands import execute_task

def main():
    speak("Hey Rishabh, I am ready. Say a command when you are ready.")
    # Main loop: continuously listen then execute
    while True:
        command = take_command()
        if not command:
            # nothing recognized; continue listening
            continue
        # Pass speak function so commands can give voice feedback
        execute_task(command, speak)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Safe exit on CTRL+C
        print("\nAssistant stopped by user.")
        speak("Goodbye! See you soon.")
