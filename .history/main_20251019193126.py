#main.py
from voice_utils import listen, speak


from intent_recognizer import recognize_intent

def split_commands(command_text):
    keywords = ["and then", "aur phir", "phir"]
    command_text = command_text.lower()
    for kw in keywords:
        command_text = command_text.replace(kw, "||")
    return [cmd.strip() for cmd in command_text.split("||") if cmd.strip()]

def main():
    speak("नमस्ते सर, मैं आपका एआई असिस्टेंट तैयार हूँ।")
   
    print("🧠 Jarvis online and ready for commands...\n")

    context_history = []

    while True:
        user_command = listen()



        
        if user_command.lower() in ["exit", "quit", "बाय"]:
            speak("अलविदा सर। आपका दिन शुभ हो।")
            break

        commands = split_commands(user_command)
        for cmd in commands:
            print(f"\n🎯 Command detected: {cmd}")
            result = recognize_intent(cmd, context_history)
            print(f"✅ Jarvis Result: {result}\n")
            speak(result)
            context_history.append({"user": cmd, "assistant": result})

if __name__ == "__main__":
    main()

















# from voice_utils import listen, speak
# from intent_recognizer import recognize_intent

# def split_commands(command_text):
#     keywords = ["and then", "aur phir", "phir"]
#     command_text = command_text.lower()
#     for kw in keywords:
#         command_text = command_text.replace(kw, "||")
#     return [cmd.strip() for cmd in command_text.split("||") if cmd.strip()]

# def main():
#     speak("hello sir mai apki kya madad kr sakta hu.")
#     context_history = []

#     while True:
#         user_command = listen()
#         if user_command.lower() in ["exit", "quit", "bye"]:
#             speak("Bye! Aapka din shubh ho.")
#             break

#         commands = split_commands(user_command)
#         for cmd in commands:
#             result = recognize_intent(cmd, context_history)
#             print(result)
#             speak(result)
#             context_history.append({"user": cmd, "assistant": result})

# if __name__ == "__main__":
#     main()
