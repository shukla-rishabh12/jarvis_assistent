# test_voice_edge.py
import asyncio
import edge_tts

async def speak_async(text):
    """Speak text using Edge TTS hi-IN-HeeraNeural voice."""
    communicate = edge_tts.Communicate(text, voice="hi-IN-HeeraNeural")
    print("🗣️ Speaking:", text)
    await communicate.stream_async()

def speak(text):
    """Sync wrapper for async speak"""
    asyncio.run(speak_async(text))

if __name__ == "__main__":
    # Test Hindi voice
    speak("नमस्ते रिषभ भाई, आपका AI असिस्टेंट तैयार है।")
    speak("अब आप मुझसे हिंदी या इंग्लिश में बात कर सकते हैं।")
    speak("बक्सर का युद्ध 1764 में ब्रिटिश ईस्ट इंडिया कंपनी और बंगाल के नवाब मीर कासिम के बीच लड़ा गया था।")
