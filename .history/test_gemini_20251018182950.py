import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
print(f"Total voices: {len(voices)}\n")

for i, voice in enumerate(voices):
    print(f"{i+1}. Name: {voice.name}, ID: {voice.id}")
