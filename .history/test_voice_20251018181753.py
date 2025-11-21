# test_voice_edge_play.py
import asyncio
import edge_tts
from playsound import playsound
import os

async def speak_async(text, filename="temp_voice.mp3"):
    """Speak text using Edge TTS (hi-IN-HeeraNeural) and play audio."""
    communicate = edge_tts.Communicate(text, voice="hi-IN-HeeraNeural")
    await communicate.save(filename)
    playsound(filename)
    os.remove(filename)

def speak(text):
    """Sync wrapper"""
    asyncio.run(speak_async(text))

if __name__ == "__main__":
    speak("नमस्ते रिषभ भाई, आपका AI असिस्टेंट तैयार है।")
    speak("अब आप मुझसे हिंदी या इंग्लिश में बात कर सकते हैं।")
    speak("बक्सर का युद्ध 1764 में ब्रिटिश ईस्ट इंडिया कंपनी और बंगाल के नवाब मीर कासिम के बीच लड़ा गया था।")
