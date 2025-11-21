# import pyttsx3

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')

# print("🔍 Available Voices:")
# for i, v in enumerate(voices):
#     print(f"{i}. {v.name} - {v.id}")
from voice_utils import speak, listen

speak("नमस्ते, मैं आपकी क्या सहायता कर सकता हूँ?")
cmd = listen()
speak(f"आपने कहा: {cmd}")
