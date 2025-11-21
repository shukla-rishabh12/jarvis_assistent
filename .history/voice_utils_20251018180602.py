import speech_recognition as sr
import pyttsx3
import asyncio
import edge_tts
from playsound import playsound
import os

# -----------------------------#
#  🔊 INITIALIZATION
# -----------------------------#
print("🟢 Voice engine initializing...")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
hindi_voice_found = False

for voice in voices:
    if any(keyword in voice.name.lower() for keyword in ["hindi", "india", "indian", "heera", "ravi", "male"]):
        engine.setProperty('voice', voice.id)
        hindi_voice_found = True
        print(f"✅ Selected voice: {voice.name}")
        break

engine.setProperty('rate', 160)
engine.setProperty('volume', 1)

if not hindi_voice_found:
    print("⚠️ Hindi voice not found in pyttsx3. Using Edge-TTS fallback (hi-IN-HeeraNeural).")


# -----------------------------#
#  🔉 SPEAK FUNCTION
# -----------------------------#
async def speak_edge(text: str):
    """Use Edge-TTS for natural Hindi speech"""
    try:
        voice = "hi-IN-HeeraNeural"
        output_path = "temp_hindi_voice.mp3"
        communicate = edge_tts.Communicate(text, voice=voice)
        await communicate.save(output_path)
        playsound(output_path)  # Play audio reliably
        os.remove(output_path)  # Delete temporary file
    except Exception as e:
        print(f"❌ Edge-TTS error: {e}")


def speak(text: str):
    """Speak text using pyttsx3 or Edge-TTS fallback"""
    print(f"🗣️ Speaking: {text}")
    try:
        if hindi_voice_found:
            engine.say(text)
            engine.runAndWait()
        else:
            asyncio.run(speak_edge(text))
    except Exception as e:
        print(f"⚠️ pyttsx3 error: {e}. Switching to Edge-TTS...")
        asyncio.run(speak_edge(text))


# -----------------------------#
#  🎤 LISTEN FUNCTION
# -----------------------------#
def listen() -> str:
    """Listen for a voice command (Hindi/English mix)"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening... (Hindi/English supported)")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, phrase_time_limit=7)
        except Exception as e:
            print("❌ Listening error:", e)
            return "Listening failed"

    try:
        # Hindi/Hinglish understanding
        command = r.recognize_google(audio, language="hi-IN")
        print("🗣️ You said:", command)
        return command

    except sr.UnknownValueError:
        speak("माफ कीजिए, मैं समझ नहीं पाया। कृपया दोबारा बोलें।")
        return "Could not recognize your voice."
    except sr.RequestError:
        speak("Speech service इस समय उपलब्ध नहीं है।")
        return "Speech service not available."
