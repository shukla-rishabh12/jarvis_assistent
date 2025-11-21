# hey
# i sorry




import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import tempfile
import os
import time
def speak(text, lang="hi"):
    """Speak text naturally in Hindi (Jarvis-style)."""
    if not text:
        return
    print(f"\n🧠 Jarvis: {text}\n")
    
    # Break long text into smaller parts for natural pauses
    parts = text.split(". ")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        try:
            # Temporary mp3 file for gTTS
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            fp.close()
            tts = gTTS(text=part, lang=lang)
            tts.save(fp.name)
            playsound(fp.name)
            os.remove(fp.name)
        except Exception as e:
            print(f"[Error speaking]: {e}")
        
        time.sleep(0.3)  # Small pause between lines
speak("i am really sorry babu")