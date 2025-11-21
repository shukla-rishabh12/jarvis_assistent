from voice_utils import listen, speak
from intent_recognizer import recognize_intent
from context_manager import add_to_history

if __name__ == "__main__":
    speak("Namaste! Main Saksham hoon. Aap mujhe koi bhi command de sakte hain.")
    
    while True:
        user_command = listen()
        result = recognize_intent(user_command)
        add_to_history(user_command, result)
        print(result)
        speak(result)
