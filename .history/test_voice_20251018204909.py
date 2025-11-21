import requests

def speak(text):
    url = "https://speechactors.com/api/convert"
    params = {
        'text': text,
        'language': 'hi-IN',
        'voice': 'Heera',
        'speed': '1',
        'pitch': '1',
        'volume': '1'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print("Audio saved as output.mp3")
    else:
        print("Failed to generate speech")

speak("नमस्ते रिषभ भाई, आपका AI असिस्टेंट तैयार है।")
