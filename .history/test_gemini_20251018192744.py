import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Check available voices
voices = engine.getProperty('voices')
for idx, voice in enumerate(voices):
    print(f"{idx}: {voice.name} - {voice.id}")

# Set voice to Microsoft Ravi (Hindi)
for voice in voices:
    if "Hemant" in voice.name:  # Windows Hindi male voice
        engine.setProperty('voice', voice.id)
        break

# Optional: Adjust speed and volume
engine.setProperty('rate', 150)   # Speed
engine.setProperty('volume', 1)   # Volume (0.0 to 1.0)

# Test Hindi text
engine.say("नमस्ते, यह Microsoft Ravi voice का परीक्षण है।")
engine.runAndWait()
