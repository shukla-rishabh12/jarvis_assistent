import speech_recognition as sr
import pyttsx3
import asyncio
import edge_tts

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
hindi_voice_found = False

# Try to find Hindi/Indian voices in pyttsx3
for voice in voices:
    if "hindi" in voice.name.lower() or "india" in voice.name.lower() or "indian" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        hindi_voice_found = True
        print(f"✅ Hindi voice found: {voice.name}")
        break

if not hindi_voice_found:
    print("⚠️ Hindi voice not found in pyttsx3. Edge-TTS fallback enabled.")

engine.setProperty('rate', 160)
engine.setProperty('volume', 1)

# ---------- SPEAK FUNCTION ----------
async def speak_edge(text):
    """Use Edge TTS for natural Hindi speech"""
    try:
        communicate = edge_tts.Communicate(text, voice="hi-IN-HeeraNeural")
        await communicate.stream_async()
    except Exception as e:
        print("⚠️ Edge TTS error:", e)

def speak(text):
    """Speak using pyttsx3 or fallback to Edge TTS"""
    print("🗣️ Speaking:", text)
    if hindi_voice_found:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("⚠️ pyttsx3 error:", e)
            asyncio.run(speak_edge(text))
    else:
        asyncio.run(speak_edge(text))

# ---------- LISTEN FUNCTION ----------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening... (Hindi/English supported)")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, phrase_time_limit=7)
        except:
            return "Listening failed"

    try:
        command = r.recognize_google(audio, language="hi-IN")  # Hindi preferred
        print("🗣️ You said:", command)
        return command
    except sr.UnknownValueError:
        return "मुझे आपकी आवाज़ समझ नहीं आई, कृपया फिर से बोलें।"
    except sr.RequestError:
        return "Speech service उपलब्ध नहीं है।"
