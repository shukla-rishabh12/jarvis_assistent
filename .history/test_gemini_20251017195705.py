import requests
from config import API_KEY, GEMINI_MODEL

# सही endpoint for text generation
url = f"https://generativeai.googleapis.com/v1beta2/models/{GEMINI_MODEL}:generateText"

# headers with API key
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# request payload
data = {
    "prompt": "Hello! Introduce yourself briefly.",
    "temperature": 0.7,
    "maxOutputTokens": 100
}

# POST request
response = requests.post(url, headers=headers, json=data)

# check response
if response.status_code == 200:
    print("✅ API काम कर रहा है!")
    result = response.json()
    # response का main text print करो
    print(result.get("candidates", [{}])[0].get("content", "No content"))
else:
    print("❌ कुछ गड़बड़ है!")
    print("Status code:", response.status_code)
    print("Response:", response.text)
