import pyttsx3

engine = pyttsx3.init()

# Available voices check karo
voices = engine.getProperty('voices')
for v in voices:
    print(v.id, v.name)  # Yaha Heera dikhegi

# Heera select karo
for v in voices:
    if "heera" in v.name.lower():
        engine.setProperty('voice', v.id)
        break

engine.say("नमस्ते, यह परीक्षण है")
engine.runAndWait()
