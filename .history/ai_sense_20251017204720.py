from google import genai
from config import API_KEY, GEMINI_MODEL

client = genai.Client(api_key=API_KEY)

def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini API Error: {e}"
