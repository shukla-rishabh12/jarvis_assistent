from gtts import gTTS
from playsound import playsound
import tempfile
import os

def speak(text, lang="hi"):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts = gTTS(text=text, lang=lang)
        tts.save(fp.name)
        playsound(fp.name)

if __name__ == "__main__":
    speak("नमस्ते रिषभ भाई, आपका AI असिस्टेंट तैयार है।")
    speak("अब आप मुझसे हिंदी में बात कर सकते हैं।")
