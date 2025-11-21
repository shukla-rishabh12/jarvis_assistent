import comtypes.client

speaker = comtypes.client.CreateObject("SAPI.SpVoice")
for i in range(speaker.GetVoices().Count):
    voice = speaker.GetVoices().Item(i)
    print(voice.GetDescription())
