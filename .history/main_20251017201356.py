from voice_utils import listen, speak
from intent_recognizer import recognize_intent
from context_manager import add_to_history

def main():
    speak("Namaste! Main Saksham hoon. Aap mujhe koi bhi command de sakte hain.")

    while True:
        user_command = listen()
        if user_command.lower() in ["exit", "quit", "bye"]:
            speak("Bye! Have a nice day.")
            break

        result = recognize_intent(user_command)
        add_to_history(user_command, result)
        print(result)
        speak(result)

if __name__ == "__main__":
    main()
