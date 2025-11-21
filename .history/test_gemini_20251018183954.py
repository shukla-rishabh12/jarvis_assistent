import asyncio
import edge_tts

async def main():
    communicate = edge_tts.Communicate("नमस्ते, यह नई हिंदी वॉइस काम कर रही है!", "hi-IN-SwaraNeural")
    await communicate.save("output.mp3")

asyncio.run(main())
