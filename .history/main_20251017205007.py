from voice_utils import listen, speak
from intent_recognizer import recognize_intent

def split_commands(command_text):
    keywords = ["and then", "aur phir", "phir"]
    command_text = command_text.lower()
    for kw in keywords:
        command_text = command_text.replace(kw, "||")
    return [cmd.strip() for cmd in command_text.split("||") if cmd.strip()]

def main():
    speak("Namaste! Main Saksham hoon. Aap mujhe command de sakte hain.")
    context_history = []

    while True:
        user_command = listen()
        if user_command.lower() in ["exit", "quit", "bye"]:
            speak("Bye! Aapka din shubh ho.")
            break

        commands = split_commands(user_command)
        for cmd in commands:
            result = recognize_intent(cmd, context_history)
            print(result)
            speak(result)
            context_history.append({"user": cmd, "assistant": result})

if __name__ == "__main__":
    main()
