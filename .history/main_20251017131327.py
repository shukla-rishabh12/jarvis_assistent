# main.py
from speech_utils import listen, speak
from commands import execute_command

def main():
    speak("Jarvis tayaar hai. Kuch bhi boliye.")
    while True:
        text = listen()
        if not text:
            continue
        try:
            execute_command(text)
        except SystemExit:
            break
        except Exception as e:
            print("Error executing command:", e)
            speak("Kuch error ho gaya. Dobara boliye.")

if __name__ == "__main__":
    main()
