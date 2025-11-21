# test_voice_hindi.py
import pythoncom
import win32com.client

def speak(text):
    pythoncom.CoInitialize()  # Required for multithreaded apps
    speaker = win32com.client.Dispatch("SAPI.SpVoice")

    # List available voices
    voices = speaker.GetVoices()
    found = False
    for i in range(voices.Count):
        v = voices.Item(i)
        print(f"Voice {i}: {v.GetDescription()}")
        # Select Heera / Ravi (Hindi) if available
        if "Heera" in v.GetDescription() or "Ravi" in v.GetDescription():
            speaker.Voice = v
            found = True
            break

    if not found:
        print("⚠️ Hindi voice not found, using default voice")

    speaker.Rate = 0   # Speed (-10 slow, 10 fast)
    speaker.Volume = 100  # 0-100
    print("🗣️ Speaking:", text)
    speaker.Speak(text)

if __name__ == "__main__":
    speak("नमस्ते रिषभ भाई, आपका AI असिस्टेंट तैयार है।")
    speak("अब आप मुझसे हिंदी या इंग्लिश में बात कर सकते हैं।")
    speak("बक्सर का युद्ध 1764 में ब्रिटिश ईस्ट इंडिया कंपनी और बंगाल के नवाब मीर कासिम के बीच लड़ा गया था।")
