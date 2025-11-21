from google import genai
from config import API_KEY, GEMINI_MODEL

# Initialize client with API key
client = genai.Client(api_key=API_KEY)

# Generate content using Gemini
prompt = "Explain how AI works in a few words"

response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents=prompt
)

# Print the response
print("✅ Gemini API response:")
print(response.text)
