import requests
from config import API_KEY, GEMINI_API_URL, GEMINI_MODEL

# endpoint बनाओ
url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateText"

# headers में API key
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# request payload
data = {
    "prompt": "Hello! Please introduce yourself briefly.",
    "temperature": 0.7,
    "maxOutputTokens": 100
}

# request भेजो
response = requests.post(url, headers=headers, json=data)

# response check करो
if response.status_code == 200:
    print("✅ API काम कर रहा है!")
    print("Response:")
    print(response.json())
else:
    print("❌ कुछ गड़बड़ है!")
    print("Status code:", response.status_code)
    print("Response:", response.text)
