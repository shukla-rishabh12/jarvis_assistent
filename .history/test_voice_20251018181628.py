# test_voice_edge_sync.py
import edge_tts
import asyncio

def speak(text):
    """Speak text using Edge TTS hi-IN-HeeraNeural voice (synchronous)."""
    print("🗣️ Speaking:", text)
    communicate = edge_tts.Communicate(text, voice="hi-IN-HeeraNeural")
    # stream_sync directly bol deta hai
    communicate.stream_sync()

if __name__ == "__main__":
    speak("नमस्ते रिषभ भाई, आपका AI असिस्टेंट तैयार है।")
    speak("अब आप मुझसे हिंदी या इंग्लिश में बात कर सकते हैं।")
    speak("बक्सर का युद्ध 1764 में ब्रिटिश ईस्ट इंडिया कंपनी और बंगाल के नवाब मीर कासिम के बीच लड़ा गया था।")
