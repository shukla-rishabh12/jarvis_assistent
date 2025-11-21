from gtts import gTTS
from playsound import playsound
import tempfile
import os

def speak(text, lang="hi"):
    # Temporary file, delete=False for Windows
    fp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    fp.close()  # Close immediately so gTTS can write
    tts = gTTS(text=text, lang=lang)
    tts.save(fp.name)
    playsound(fp.name)
    os.remove(fp.name)  # Delete after playing

if __name__ == "__main__":
    speak("नमस्ते रिषभ भाई, आपका AI असिस्टेंट तैयार है।")
    speak("अब आप मुझसे हिंदी में बात कर सकते हैं।")
